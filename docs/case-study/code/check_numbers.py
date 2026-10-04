#!/usr/bin/env python3
"""Recompute Table 1, the detector counts and Cohen's kappa from incidents.csv, and fail if the manuscript disagrees."""
import csv
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
rows = list(csv.DictReader((ROOT / "incidents.csv").open(newline="")))
text = (ROOT / "ai-research-failure-modes.md").read_text()
errors = []

if len(rows) != 80:
    errors.append(f"expected 80 incidents, found {len(rows)}")

classes = "NLWVP"
reach_order = ["public", "uncertain", "caught/internal"]
for code in classes:
    subset = [r for r in rows if r["class"] == code]
    counts = [sum(1 for r in subset if r["reach"] == reach) for reach in reach_order]
    total = len(subset)
    # The manuscript table uses these exact cells. N has a 0 uncertain cell.
    needle = f"| {total} | {counts[0]} | {counts[1]} | {counts[2]} |"
    if needle not in text:
        errors.append(f"class {code}: manuscript missing {needle}")

labels = [r["class"] for r in rows]
second = [r["second_coder_class"] for r in rows]
n = len(rows)
agree = sum(a == b for a, b in zip(labels, second))
c1, c2 = Counter(labels), Counter(second)
keys = sorted(set(c1) | set(c2))
pe_num = sum(c1[k] * c2[k] for k in keys)
pe = pe_num / (n * n)
kappa = (agree / n - pe) / (1 - pe)
if agree != 74:
    errors.append(f"agreements {agree}, expected 74")
if pe_num != 1356:
    errors.append(f"chance numerator {pe_num}, expected 1356")
if abs(kappa - 0.9048374306106265) > 1e-12:
    errors.append(f"kappa {kappa}")
for token in ("0.905", "1356/6400", "74 of 80"):
    if token not in text:
        errors.append(f"manuscript missing {token}")

disagreements = sorted(r["id"] for r in rows if r["class"] != r["second_coder_class"])
expected = ["P14", "V13", "V16", "V19", "W14", "W15"]
if disagreements != expected:
    errors.append(f"disagreements {disagreements}")
for ident in expected:
    if ident not in text.split("The six disagreements are", 1)[-1][:400]:
        errors.append(f"disagreement {ident} not named in the reliability paragraph")

both = 0
ref = avw = 0
for row in rows:
    parts = {p.strip() for p in row["detected_by"].split(",")}
    if "REF" in parts:
        ref += 1
    if "AVW" in parts:
        avw += 1
    if "REF" in parts and "AVW" in parts:
        both += 1
if (ref, avw, both) != (28, 11, 0):
    errors.append(f"REF/AVW/both = {ref, avw, both}")

named = Counter()
for row in rows:
    for part in [p.strip() for p in row["detected_by"].split(",") if p.strip()]:
        named[part] += 1
expected_detectors = {
    "REF": 28, "SELF": 16, "AVW": 11, "REV": 6, "AUD": 6, "OWN": 4,
    "RUN": 3, "this study": 3, "IND": 2, "CI": 2, "cross-assistant review": 1,
}
if dict(named) != expected_detectors:
    errors.append(f"detectors {dict(named)}")
if sum(named.values()) != 82:
    errors.append(f"detection total {sum(named.values())}, expected 82")
for code, n in (("SELF", 16), ("RUN", 3)):
    if f"| {n} |" not in text:
        errors.append(f"Table 2 missing count {n} for {code}")

if "We are not aware" in text:
    errors.append("withdrawn contribution sentence is still present")
if "random-matrix" in text:
    errors.append("rank-window is still described as random-matrix spectra")
if "κ = 0.91" in text or "kappa = 0.91" in text:
    errors.append("rounded kappa 0.91 is still present")

svg = (ROOT / "fig-classes.svg").read_text()
for token in (">9<", ">18<", ">19<", ">20<", ">14<", ">28<", ">16<", ">11<", ">6<", ">4<", ">3<", ">2<", ">1<"):
    if token not in svg:
        errors.append(f"fig-classes.svg missing {token}")
if "Not stated" in svg or "Other recorded" in svg:
    errors.append("fig-classes.svg still has the pre-1.6 detector grouping")
if "Yeung" not in text:
    errors.append("manuscript does not cite Yeung (2026)")
timeline = (ROOT / "fig-timeline.svg").read_text()
for token in (">20<", ">15<", ">13<"):
    if token not in timeline:
        errors.append(f"fig-timeline.svg missing daily total {token}")

if errors:
    print("\n".join("FAIL " + e for e in errors))
    sys.exit(1)
print(f"OK: 80 incidents, kappa {kappa:.3f}, chance {pe_num}/6400, REF {ref} + AVW {avw}")
