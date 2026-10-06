#!/usr/bin/env python3
"""Check the case study against incidents.csv. Exits 1 on any disagreement.

Recomputes from incidents.csv, and fails if the manuscript states otherwise:
  - the class counts in the abstract and Table 1, row by row;
  - Table 2, row by row, and its order;
  - the AI-review share, the owner count and the rates;
  - Cohen's kappa, the chance term and the six disagreements;
  - every row of Appendix A.
Redraws the three figures in memory and fails if a committed SVG differs.
Fails if the committed PDF was built from a different manuscript or figures.

Every match is anchored to the row or sentence that makes the claim. A bare
"| 3 |" also matches a cell of another table, so it cannot fail.

Failure control: before the real check runs, seven planted faults must each
be rejected for their own reason, and the clean inputs must pass. If not, this
program exits 1. A check that has not been shown to fail is not a check.

Not checked: anything in GENChase itself. The commit counts (245, 315) and the
nine preprints are copied from that repository and are not recomputed here.
"""
import csv
import io
import re
import sys
from collections import Counter
from datetime import date
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import make_figures  # noqa: E402
from digest import TAG, source_digest  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
MANUSCRIPT = "ai-research-failure-modes.md"
FIGURES = ("fig-classes.svg", "fig-timeline.svg", "fig-overhead.svg")

# Copied from GENChase at 98e7fc4 (Section 3). Not recomputable from the CSV.
COMMITS_IN_WINDOW = 245
PREPRINTS = 9

CLASSES = [
    # code, Table 1 label, abstract wording
    ("N", "N. Unsupported novelty or priority", "unsupported novelty or priority"),
    ("L", "L. Literature misuse", "literature misuse"),
    ("W", "W. Wrong numbers, overstated results", "wrong numbers or overstated results"),
    ("V", "V. Verification that could not fail or did not exist", "verification that could not fail or did not exist"),
    ("P", "P. Process and tooling", "process and tooling failures"),
]
DETECTORS = {
    "REF": "Separate-agent referee reading (REF)",
    "SELF": "The working session itself (SELF)",
    "AVW": "Adversarial verification workflow (AVW)",
    "REV": "Full reading of a source (REV)",
    "AUD": "Literature or novelty audit (AUD)",
    "OWN": "Owner (OWN)",
    "RUN": "Re-run or download check (RUN)",
    "this study": "This study",
    "IND": "Independent re-derivation (IND)",
    "CI": "CI",
    "cross-assistant review": "Cross-assistant review",
}
REACH = ["public", "uncertain", "caught/internal"]
REACH_CODE = {"public": "P", "uncertain": "?", "caught/internal": "C"}
UNITS = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen".split()
TENS = {2: "twenty", 3: "thirty", 4: "forty", 5: "fifty", 6: "sixty", 7: "seventy", 8: "eighty", 9: "ninety"}


def words(n):
    if n < 20:
        return UNITS[n]
    tens, unit = divmod(n, 10)
    return TENS[tens] + ("" if unit == 0 else "-" + UNITS[unit])


def detectors(row):
    return [p.strip() for p in row["detected_by"].split(",") if p.strip()]


def kappa(rows):
    n = len(rows)
    first = [r["class"] for r in rows]
    second = [r["second_coder_class"] for r in rows]
    agree = sum(a == b for a, b in zip(first, second))
    c1, c2 = Counter(first), Counter(second)
    chance = sum(c1[k] * c2[k] for k in set(c1) | set(c2))
    pe = chance / (n * n)
    return agree, chance, (agree / n - pe) / (1 - pe)


def table_rows(text, header):
    """The data rows of the markdown table whose header line starts with `header`."""
    lines = text.splitlines()
    start = next((i for i, line in enumerate(lines) if line.startswith(header)), None)
    if start is None:
        return []
    rows = []
    for line in lines[start + 2:]:
        if not line.startswith("|"):
            break
        rows.append([cell.strip() for cell in line.strip("|").split("|")])
    return rows


def check(text, rows, committed_svgs, drawn_svgs, pdf_bytes):
    errors = []

    def need(fragment, why):
        if fragment not in text:
            errors.append(f"{why}: manuscript does not contain {fragment!r}")

    n = len(rows)
    by_class = {code: [r for r in rows if r["class"] == code] for code, _, _ in CLASSES}
    reach_total = Counter(r["reach"] for r in rows)

    # Abstract and Table 1.
    need(f"**{n} incidents in five classes**", "abstract total")
    for code, label, phrase in CLASSES:
        subset = by_class[code]
        need(f"{phrase} ({len(subset)})", f"abstract class {code}")
        cells = [sum(1 for r in subset if r["reach"] == reach) for reach in REACH]
        need(f"| {label} | {len(subset)} | {cells[0]} | {cells[1]} | {cells[2]} |", f"Table 1 class {code}")
    totals = [reach_total[r] for r in REACH]
    need(f"| **Total** | **{n}** | **{totals[0]}** | **{totals[1]}** | **{totals[2]}** |", "Table 1 total")
    need(
        f"{words(totals[0]).capitalize()} reached a public artifact, {words(totals[1])} are uncertain, "
        f"and {words(totals[2])} were caught",
        "abstract reach",
    )

    # Table 2, row by row and in the stated order.
    named = Counter(d for r in rows for d in detectors(r))
    unknown = sorted(set(named) - set(DETECTORS))
    if unknown:
        errors.append(f"Table 2: detectors with no label {unknown}")
    table = table_rows(text, "| Control | Incidents detected |")
    stated = {label: value for label, value in table}
    for code, label in DETECTORS.items():
        if stated.get(label) != str(named[code]):
            errors.append(f"Table 2 row {label!r}: manuscript {stated.get(label)}, data {named[code]}")
    counts = [int(v) for _, v in table if v.isdigit()]
    if counts != sorted(counts, reverse=True):
        errors.append(f"Table 2 is not sorted by count: {counts}")

    # AI review share, owner, rates.
    ref = sum("REF" in detectors(r) for r in rows)
    avw = sum("AVW" in detectors(r) for r in rows)
    both = sum({"REF", "AVW"} <= set(detectors(r)) for r in rows)
    either = ref + avw - both
    share = round(100 * either / n)
    need(f"account for {ref} detections and an adversarial verification workflow for {avw}", "abstract REF/AVW")
    if both == 0:
        need(f"No incident carries both, so that is {either} of {n} ({share}%)", "abstract AI review share")
    need(f"detected {either} of {n} incidents ({share}%)", "Section 5.1 AI review share")
    need(f"The owner is a detector on {named['OWN']}", "abstract owner count")
    dated = sorted(date.fromisoformat(r["date_recorded"]) for r in rows if r["date_recorded"])
    days = (dated[-1] - dated[0]).days + 1
    undated = n - len(dated)
    need(f"{days} calendar days, with {words(undated)} incident undated", "Section 3 window")
    need(
        f"about {n / days:.1f} per calendar day, one per {COMMITS_IN_WINDOW / n:.1f} commits in that window, "
        f"and {n / PREPRINTS:.1f} per preprint",
        "Section 3 rates",
    )

    # Second coder.
    agree, chance, k = kappa(rows)
    need(f"agreed on **{agree} of {n}** classes", "Section 3 agreement")
    need(f"Cohen's κ is **{k:.3f}**", "Section 3 kappa")
    need(f"Chance agreement is {chance}/{n * n} = {chance / (n * n)}", "Section 3 chance term")
    need(f"agreed on {agree} of {n} classes (Cohen's κ = {k:.3f})", "abstract kappa")
    sentence = text.split("The six disagreements are ", 1)[-1].split(".", 1)[0]
    for r in rows:
        if r["class"] != r["second_coder_class"]:
            pair = f"{r['id']} ({r['class']} against {r['second_coder_class']})"
            if pair not in sentence:
                errors.append(f"disagreement {pair} is not named in the reliability paragraph")
    disagreements = sum(r["class"] != r["second_coder_class"] for r in rows)
    if disagreements != 6:
        errors.append(f"the manuscript says six disagreements; the data has {disagreements}")

    # Appendix A.
    for r in rows:
        line = f"| {r['id']} | {r['incident']} | {r['detected_by']} | {REACH_CODE[r['reach']]} |"
        if line not in text:
            errors.append(f"Appendix A row {r['id']} does not match incidents.csv")

    # Withdrawn or corrected wording.
    for gone, why in (
        ("We are not aware", "withdrawn contribution sentence"),
        ("random-matrix", "rank-window described as random-matrix spectra"),
        ("κ = 0.91", "rounded kappa"),
    ):
        if gone in text:
            errors.append(f"{why} is still present")

    # Figures and PDF.
    for name in FIGURES:
        if committed_svgs.get(name) != drawn_svgs[name]:
            errors.append(f"{name} differs from a fresh drawing; run code/make_figures.py")
    texts = {MANUSCRIPT: text, **committed_svgs}
    want = f"{TAG} {source_digest(texts)}".encode()
    if want not in pdf_bytes:
        found = re.search(rb"source-sha256 [0-9a-f]{64}", pdf_bytes)
        errors.append(
            "PDF was not built from this manuscript and these figures "
            f"({found.group(0).decode() if found else 'no source digest'}); run code/build_pdf.py"
        )
    return errors


def load():
    rows = list(csv.DictReader(io.StringIO((ROOT / "incidents.csv").read_text())))
    text = (ROOT / MANUSCRIPT).read_text()
    committed = {name: (ROOT / name).read_text() for name in FIGURES}
    pdf = (ROOT / "ai-research-failure-modes.pdf").read_bytes()
    return text, rows, committed, make_figures.render(), pdf


def failure_controls(text, rows, committed, drawn, pdf):
    """Each planted fault must be rejected, with an error that names it."""
    if check(text, rows, committed, drawn, pdf):
        return  # the real run reports these; a dirty baseline cannot test the controls

    def plant(old, new):
        if old not in text:
            raise SystemExit(f"FAIL failure control cannot plant: {old!r} not in manuscript")
        return text.replace(old, new, 1)

    w18 = next(r for r in rows if r["id"] == "W18")
    svg = committed["fig-timeline.svg"]
    faults = [
        # The old checker searched the whole file for "| 3 |", which Table 1 also contains.
        ("Table 2 RUN 3 -> 4", plant("| Re-run or download check (RUN) | 3 |", "| Re-run or download check (RUN) | 4 |"), rows, committed, "Table 2 row"),
        ("Table 1 V public 5 -> 4", plant("| 20 | 5 | 1 | 14 |", "| 20 | 4 | 1 | 14 |"), rows, committed, "Table 1 class V"),
        ("kappa 0.905 -> 0.904", plant("Cohen's κ is **0.905**", "Cohen's κ is **0.904**"), rows, committed, "Section 3 kappa"),
        ("abstract reach twenty-two -> twenty-one", plant("Twenty-two reached", "Twenty-one reached"), rows, committed, "abstract reach"),
        ("CSV W18 reach public -> uncertain", text, [dict(r, reach="uncertain") if r is w18 else r for r in rows], committed, "Appendix A row W18"),
        ("one byte of a figure", text, rows, dict(committed, **{"fig-timeline.svg": svg.replace(">20<", ">21<", 1)}), "fig-timeline.svg differs"),
        ("PDF from an older manuscript", plant("## Abstract", "## Abstract "), rows, committed, "PDF was not built"),
    ]
    for name, planted_text, planted_rows, planted_svgs, reason in faults:
        errors = check(planted_text, planted_rows, planted_svgs, drawn, pdf)
        if not any(reason in e for e in errors):
            raise SystemExit(f"FAIL failure control '{name}' was not rejected for its reason ({reason}): {errors}")
    return [name for name, *_ in faults]


def main():
    text, rows, committed, drawn, pdf = load()
    controls = failure_controls(text, rows, committed, drawn, pdf)
    errors = check(text, rows, committed, drawn, pdf)
    if errors:
        print("\n".join("FAIL " + e for e in errors))
        sys.exit(1)
    agree, chance, k = kappa(rows)
    print(f"OK: {len(rows)} incidents, kappa {k:.3f}, chance {chance}/{len(rows) ** 2}, figures and PDF match their sources")
    print(f"Failure control: {len(controls)} planted faults rejected ({'; '.join(controls)}).")


if __name__ == "__main__":
    main()
