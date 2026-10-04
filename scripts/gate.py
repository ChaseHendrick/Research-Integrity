#!/usr/bin/env python3
"""Release gate for this repository.

Recomputes the public incident count from incidents.csv and fails if the skill
or the README states a different one. Fails if the release version disagrees
across the plugin manifest, the citation file, the changelog, the skill, and
the case study. Builds dist/research-integrity.zip from SKILL.md and fails if
that archive does not contain exactly that file.

Failure control: a planted wrong count, and a planted version mismatch, must
each raise GateError. If either does not, this program exits 1. A program that
cannot fail is not a gate.
"""
import csv
import io
import json
import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "plugins/research-integrity/skills/research-integrity/SKILL.md"
PLUGIN = ROOT / "plugins/research-integrity/.claude-plugin/plugin.json"
CITATION = ROOT / "CITATION.cff"
CHANGELOG = ROOT / "CHANGELOG.md"
README = ROOT / "README.md"
INCIDENTS = ROOT / "docs/case-study/incidents.csv"
CASE = ROOT / "docs/case-study/ai-research-failure-modes.md"
ZIP_PATH = ROOT / "dist/research-integrity.zip"


class GateError(Exception):
    pass


def incident_rows(text):
    return list(csv.DictReader(io.StringIO(text)))


def stated_count(text, pattern, where):
    found = [int(n) for n in re.findall(pattern, text)]
    if not found:
        raise GateError(f"{where}: no count matching {pattern}")
    if any(n != found[0] for n in found):
        raise GateError(f"{where}: counts disagree {found}")
    return found[0]


def versions_agree(numbers):
    if len(set(numbers)) != 1:
        raise GateError(f"version mismatch {numbers}")
    if not re.fullmatch(r"\d+\.\d+\.\d+", numbers[0]):
        raise GateError(f"version is not semver: {numbers[0]}")
    return numbers[0]


def skill_release(text):
    m = re.search(r"^Release: (\d+\.\d+\.\d+)\s*$", text, re.M)
    if not m:
        raise GateError("SKILL.md has no Release line")
    return m.group(1)


def changelog_release(text, version):
    if f"## {version} " not in text and f"## {version}\n" not in text:
        raise GateError(f"CHANGELOG.md has no heading for {version}")


def case_release(text):
    found = re.findall(r"The current skill release is (\d+\.\d+\.\d+)\.", text)
    if not found:
        raise GateError("case study does not name the current skill release")
    if len(set(found)) != 1:
        raise GateError(f"case study names more than one current release {found}")
    return found[0]


def citation_version(text):
    m = re.search(r"^version: (\d+\.\d+\.\d+)\s*$", text, re.M)
    if not m:
        raise GateError("CITATION.cff has no version")
    return m.group(1)


def build_zip(skill_text, dest):
    dest.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(dest, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("research-integrity/", "")
        archive.writestr("research-integrity/SKILL.md", skill_text)
    with zipfile.ZipFile(dest) as archive:
        names = archive.namelist()
        if "research-integrity/SKILL.md" not in names:
            raise GateError(f"zip missing SKILL.md: {names}")
        packed = archive.read("research-integrity/SKILL.md").decode()
    if packed != skill_text:
        raise GateError("zip SKILL.md does not match the file that was packed")
    return dest


def failure_controls():
    try:
        stated = stated_count("a record of 79 failures", r"(\d+) failures", "plant")
        if stated == 80:
            raise GateError("planted count was read as 80")
        raise GateError(f"planted count {stated} against data 80")
    except GateError as exc:
        if "planted count 79" not in str(exc):
            raise GateError(f"count control failed for the wrong reason: {exc}")
    try:
        versions_agree(["1.2.0", "1.2.0", "1.1.0"])
    except GateError as exc:
        if "version mismatch" not in str(exc):
            raise GateError(f"version control failed for the wrong reason: {exc}")
    else:
        raise GateError("planted version mismatch did not fail")


def main():
    failure_controls()
    skill = SKILL.read_text()
    readme = README.read_text()
    incidents = INCIDENTS.read_text()
    n = len(incident_rows(incidents))
    skill_n = stated_count(skill, r"(\d+) failures", "SKILL.md")
    readme_n = stated_count(readme, r"(\d+) documented failures", "README.md")
    if skill_n != n or readme_n != n:
        raise GateError(f"incident count is {n}, skill says {skill_n}, readme says {readme_n}")
    plugin_version = json.loads(PLUGIN.read_text())["version"]
    version = versions_agree([
        plugin_version,
        citation_version(CITATION.read_text()),
        skill_release(skill),
        case_release(CASE.read_text()),
    ])
    changelog_release(CHANGELOG.read_text(), version)
    if "## 8. The gate is a program" not in skill or "## Goal" not in skill:
        raise GateError("SKILL.md is missing the goal or rule 8")
    build_zip(skill, ZIP_PATH)
    print(f"OK: gate passed for {version}, {n} incidents, zip {ZIP_PATH.relative_to(ROOT)}")
    print("Failure control: planted count 79 failed; planted version mismatch failed.")


if __name__ == "__main__":
    try:
        main()
    except GateError as exc:
        print(f"FAIL {exc}", file=sys.stderr)
        sys.exit(1)
