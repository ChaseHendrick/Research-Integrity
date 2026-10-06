#!/usr/bin/env python3
"""Release gate for this repository.

Fails (exit 1) if any of these does not hold:
  - The incident count in the skill and the README is the row count of
    incidents.csv, and the README's class table, AI-review share and
    agreement figures are what that file gives.
  - The README names the case-study version the manuscript carries.
  - The release version agrees across the plugin manifest, the citation file,
    the skill's Release line and the changelog, and the citation date is the
    changelog date. The skill release the case study names has a changelog
    heading and is not newer than this release.
  - The plugin ships no hook, server or script.
  - No shipped prose uses an overclaim phrase beyond the quotations listed in
    QUOTED, which are the places that quote a phrase in order to forbid it.
  - dist/research-integrity.zip, built in this run, holds exactly SKILL.md and
    LICENSE, byte for byte, and two builds are identical.

Failure control: before the real check, each fault in PLANTED is written into
a copy of the tree, and the check must reject it for its own reason. The clean
copy must pass. If either fails, this program exits 1.

  python3 scripts/gate.py                     run the gate and build the zip
  python3 scripts/gate.py --compare FILE.zip  also require a downloaded release
                                              asset to equal this build
"""
import csv
import io
import json
import re
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts/checks"))
sys.path.insert(0, str(ROOT / "docs/case-study/code"))
from phrases import scan  # noqa: E402
from check_numbers import detectors, kappa  # noqa: E402

SKILL = "plugins/research-integrity/skills/research-integrity/SKILL.md"
PLUGIN = "plugins/research-integrity"
CASE = "docs/case-study/ai-research-failure-modes.md"
ZIP_NAME = "dist/research-integrity.zip"
# A fixed timestamp, so that the same SKILL.md always gives the same zip.
ZIP_TIME = (1980, 1, 1, 0, 0, 0)

README_CLASSES = [
    ("N", "Unsupported novelty or priority"),
    ("L", "Literature misuse"),
    ("W", "Wrong numbers, overstated results"),
    ("V", "Verification that could not fail, or did not exist"),
    ("P", "Process and tooling"),
]
SHIPPED_PROSE = [
    "README.md", "CHANGELOG.md", "CONTRIBUTING.md", SKILL, f"{PLUGIN}/README.md",
    "docs/EVIDENCE.md", "docs/EXAMPLES.md", CASE,
]
# Places that quote an overclaim phrase in order to forbid it. A new use fails.
QUOTED = {
    ("README.md", "this is the first"): 2,  # the hero image text and the "Without" column
    ("README.md", "no prior work exists"): 2,
    ("README.md", "independently reviewed"): 1,
    (SKILL, "externally reviewed"): 1,  # "Never write that work was independently or externally reviewed"
    ("docs/EXAMPLES.md", "independently reviewed"): 1,  # a "Before" example
}


class GateError(Exception):
    pass


def semver(text):
    return tuple(int(part) for part in text.split("."))


def one(pattern, text, where):
    found = set(re.findall(pattern, text, re.M))
    if not found:
        raise GateError(f"{where}: nothing matches {pattern!r}")
    if len(found) > 1:
        raise GateError(f"{where}: values disagree {sorted(found)}")
    return found.pop()


def check(root):
    """Return a list of failures for the tree at root. Empty means the gate passes."""
    errors = []

    def read(path):
        return (root / path).read_text(encoding="utf-8")

    def need(text, fragment, where):
        if fragment not in text:
            errors.append(f"{where} does not say {fragment!r}")

    rows = list(csv.DictReader(io.StringIO(read("docs/case-study/incidents.csv"))))
    n = len(rows)
    skill, readme, case = read(SKILL), read("README.md"), read(CASE)

    # Counts stated in the skill and the README.
    try:
        for where, text, pattern in (
            ("SKILL.md", skill, r"(\d+) failures"),
            ("README.md", readme, r"(\d+) documented failures"),
        ):
            stated = int(one(pattern, text, where))
            if stated != n:
                errors.append(f"{where} states {stated} failures; incidents.csv has {n}")
    except GateError as exc:
        errors.append(str(exc))
    for code, label in README_CLASSES:
        subset = [r for r in rows if r["class"] == code]
        public = sum(r["reach"] == "public" for r in subset)
        need(readme, f"| {label} | {len(subset)} | {public} |", f"README class table, class {code},")
    public = sum(r["reach"] == "public" for r in rows)
    need(readme, f"| **Total** | **{n}** | **{public}** |", "README class table total")
    reviewed = sum(bool({"REF", "AVW"} & set(detectors(r))) for r in rows)
    need(readme, f"caught {reviewed} of the {n} incidents ({round(100 * reviewed / n)}%)", "README AI-review share")
    agree, _, k = kappa(rows)
    need(readme, f"agreed on {agree} of {n} class labels (κ = {k:.3f})", "README agreement")

    # The case-study version the README names.
    try:
        case_version = one(r"^Version (\d+\.\d+) · ", case, "case study")
        named = one(r"\(\[PDF\]\(docs/case-study/ai-research-failure-modes\.pdf\)\), version (\d+\.\d+)", readme, "README case-study version")
        if named != case_version:
            errors.append(f"README names case study {named}; the manuscript is {case_version}")
    except GateError as exc:
        errors.append(str(exc))

    # Release version.
    try:
        changelog = read("CHANGELOG.md")
        citation = read("CITATION.cff")
        versions = {
            "plugin.json": json.loads(read(f"{PLUGIN}/.claude-plugin/plugin.json"))["version"],
            "CITATION.cff": one(r"^version: (\S+)\s*$", citation, "CITATION.cff"),
            "SKILL.md": one(r"^Release: (\S+)\s*$", skill, "SKILL.md"),
        }
        if len(set(versions.values())) != 1:
            raise GateError(f"version mismatch {versions}")
        version = versions["plugin.json"]
        if not re.fullmatch(r"\d+\.\d+\.\d+", version):
            raise GateError(f"version is not semver: {version}")
        headed = dict(re.findall(r"^## (\d+\.\d+\.\d+) \((\d{4}-\d{2}-\d{2})\)", changelog, re.M))
        if version not in headed:
            raise GateError(f"CHANGELOG.md has no '## {version} (date)' heading")
        released = one(r"^date-released: (\S+)\s*$", citation, "CITATION.cff")
        if released != headed[version]:
            errors.append(f"CITATION.cff date-released {released}; CHANGELOG.md dates {version} {headed[version]}")
        described = one(r"the skill release is (\d+\.\d+\.\d+)\.", case, "case study")
        if described not in headed:
            errors.append(f"case study describes skill {described}, which has no changelog heading")
        elif semver(described) > semver(version):
            errors.append(f"case study describes skill {described}, newer than this release {version}")
    except GateError as exc:
        errors.append(str(exc))

    # The plugin is instructions only.
    plugin = root / PLUGIN
    for name in ("hooks/hooks.json", ".mcp.json", ".lsp.json"):
        if (plugin / name).exists():
            errors.append(f"plugin ships {name}, a command")
    for path in sorted(plugin.rglob("*")):
        if path.suffix in {".sh", ".py", ".js", ".pyc"}:
            errors.append(f"plugin ships a script: {path.relative_to(plugin)}")
    for heading in ("## Goal", "## 8. Optional: "):
        need(skill, heading, "SKILL.md")

    # Overclaim phrases in shipped prose.
    for path in SHIPPED_PROSE:
        found = {}
        for hit in scan(read(path)):
            found[hit["phrase"]] = found.get(hit["phrase"], []) + [hit["line"]]
        for phrase, lines in found.items():
            allowed = QUOTED.get((path, phrase), 0)
            if len(lines) > allowed:
                errors.append(f"{path}: {phrase!r} on lines {lines}; {allowed} quotation(s) allowed")
    return errors


def build_zip(root, dest):
    """Write the claude.ai upload. The same inputs always give the same bytes."""
    members = {
        "research-integrity/SKILL.md": (root / SKILL).read_bytes(),
        "research-integrity/LICENSE": (root / PLUGIN / "LICENSE").read_bytes(),
    }
    dest.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(dest, "w") as archive:
        for name, data in members.items():
            info = zipfile.ZipInfo(name, date_time=ZIP_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, data)
    with zipfile.ZipFile(dest) as archive:
        packed = {name: archive.read(name) for name in archive.namelist()}
    if packed != members:
        raise GateError(f"zip does not hold exactly {sorted(members)}: {sorted(packed)}")
    return dest.read_bytes()


DROP_LAST_ROW = object()


def planted_faults():
    """(name, path, old, new, reason). Each must make check() report `reason`.

    old is the text to replace, None to create the file, or DROP_LAST_ROW.
    """
    return [
        ("README count 79", "README.md", "80 documented failures", "79 documented failures", "README.md states 79"),
        ("skill count 79", SKILL, "80 failures", "79 failures", "SKILL.md states 79"),
        ("one incident dropped", "docs/case-study/incidents.csv", DROP_LAST_ROW, None, "README class table, class P"),
        ("README class V public 5 -> 4", "README.md", "| 20 | 5 |", "| 20 | 4 |", "README class table, class V"),
        ("citation version 0.0.1", "CITATION.cff", "\nversion: ", "\nversion: 0.0.1\nold-version: ", "version mismatch"),
        ("README case study 1.0", "README.md", "ai-research-failure-modes.pdf)), version ", "ai-research-failure-modes.pdf)), version 1.0 ", "values disagree"),
        ("priority wording in README", "README.md", "## Install", "This is the first skill of its kind.\n\n## Install", "'this is the first' on lines"),
        ("hook in plugin", f"{PLUGIN}/hooks/hooks.json", None, "{}", "plugin ships hooks/hooks.json"),
    ]


def failure_controls():
    with tempfile.TemporaryDirectory() as tmp:
        copy = Path(tmp) / "tree"
        shutil.copytree(ROOT, copy, ignore=shutil.ignore_patterns(".git", "dist", "__pycache__"))
        clean = check(copy)
        if clean:
            return None  # the real run reports these; a dirty tree cannot test the controls
        for name, path, old, new, reason in planted_faults():
            target = copy / path
            original = target.read_text(encoding="utf-8") if target.exists() else None
            if old is None:
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(new, encoding="utf-8")
            elif old is DROP_LAST_ROW:
                target.write_text("".join(original.splitlines(keepends=True)[:-1]), encoding="utf-8")
            else:
                if old not in original:
                    raise GateError(f"failure control '{name}' cannot be planted: {old!r} not in {path}")
                target.write_text(original.replace(old, new, 1), encoding="utf-8")
            errors = check(copy)
            if original is None:
                target.unlink()
            else:
                target.write_text(original, encoding="utf-8")
            if not any(reason in e for e in errors):
                raise GateError(f"failure control '{name}' was not rejected for its reason ({reason}): {errors}")
        if check(copy):
            raise GateError("the copy did not return to a passing state after the controls")
        first = build_zip(copy, Path(tmp) / "a.zip")
        second = build_zip(copy, Path(tmp) / "b.zip")
        if first != second:
            raise GateError("two builds of the zip differ, so a download cannot be compared with a build")
        (copy / SKILL).write_text((copy / SKILL).read_text() + "\n", encoding="utf-8")
        if build_zip(copy, Path(tmp) / "c.zip") == first:
            raise GateError("a changed SKILL.md gave the same zip")
    return [name for name, *_ in planted_faults()]


def main():
    controls = failure_controls()
    errors = check(ROOT)
    if errors:
        raise GateError("\n     ".join(errors))
    built = build_zip(ROOT, ROOT / ZIP_NAME)
    version = json.loads((ROOT / PLUGIN / ".claude-plugin/plugin.json").read_text())["version"]
    rows = sum(1 for _ in csv.DictReader(io.StringIO((ROOT / "docs/case-study/incidents.csv").read_text())))
    print(f"OK: gate passed for {version}, {rows} incidents, zip {ZIP_NAME}")
    print(f"Failure control: {len(controls)} planted faults rejected ({'; '.join(controls)}); "
          "two zip builds identical; a changed SKILL.md changes the zip.")
    if "--compare" in sys.argv:
        index = sys.argv.index("--compare")
        if index + 1 >= len(sys.argv):
            raise GateError("--compare needs the path of a downloaded zip")
        downloaded = Path(sys.argv[index + 1]).read_bytes()
        if downloaded != built:
            raise GateError(f"{sys.argv[index + 1]} is not the zip this commit builds")
        print(f"OK: {sys.argv[index + 1]} is byte for byte the zip this commit builds")


if __name__ == "__main__":
    try:
        main()
    except GateError as exc:
        print(f"FAIL {exc}", file=sys.stderr)
        sys.exit(1)
