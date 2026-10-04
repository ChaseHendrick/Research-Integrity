#!/usr/bin/env python3
"""Draw Figures 1 and 2 from incidents.csv. Control dates are the ones stated in the manuscript, not estimated."""
import csv
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ROWS = list(csv.DictReader((ROOT / "incidents.csv").open(newline="")))

CLASS_ORDER = [
    ("N", "Unsupported novelty"),
    ("L", "Literature misuse"),
    ("W", "Wrong numbers / overstated"),
    ("V", "Verification could not fail"),
    ("P", "Process and tooling"),
]
REACH_ORDER = ["public", "uncertain", "caught/internal"]
REACH_COLOR = {"public": "#c0503a", "uncertain": "#e3b341", "caught/internal": "#2f7a5f"}
SCALE = 8.5  # px per incident in Figure 1A


def detections():
    # Order and labels match Table 2. Dark bars are the two in-project AI reviews.
    order = [
        ("REF", "AI referee reading", True),
        ("SELF", "Working session itself", False),
        ("AVW", "Adversarial verification", True),
        ("REV", "Full source reading", False),
        ("AUD", "Literature / novelty audit", False),
        ("OWN", "Owner", False),
        ("RUN", "Re-run or download", False),
        ("this study", "This study", False),
        ("IND", "Independent re-derivation", False),
        ("CI", "CI", False),
        ("cross-assistant review", "Cross-assistant review", False),
    ]
    counts = Counter()
    for row in ROWS:
        for part in [p.strip() for p in row["detected_by"].split(",") if p.strip()]:
            counts[part] += 1
    known = {code for code, _, _ in order}
    extra = sorted(set(counts) - known)
    if extra:
        raise SystemExit(f"detector not in Table 2: {extra}")
    return [(label, counts[code], dark) for code, label, dark in order]


def figure_classes():
    lines = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 780 340" font-family="Helvetica,Arial,sans-serif" font-size="11">',
        '<rect width="100%" height="100%" fill="white"/>',
        '<text x="10" y="18" font-weight="bold" fill="#222">A. Incidents by class and reach</text>',
    ]
    y = 44
    for code, label in CLASS_ORDER:
        subset = [r for r in ROWS if r["class"] == code]
        x = 170
        lines.append(f'<text x="162" y="{y + 19}" text-anchor="end" fill="#333">{label}</text>')
        for reach in REACH_ORDER:
            n = sum(1 for r in subset if r["reach"] == reach)
            if not n:
                continue
            w = n * SCALE
            lines.append(f'<rect x="{x}" y="{y}" width="{w}" height="30" fill="{REACH_COLOR[reach]}"/>')
            if w >= 16:
                lines.append(
                    f'<text x="{x + w / 2}" y="{y + 19}" text-anchor="middle" fill="white" font-size="10">{n}</text>'
                )
            x += w
        lines.append(f'<text x="{x + 6}" y="{y + 19}" fill="#333">{len(subset)}</text>')
        y += 42
    lines.append('<rect x="20" y="276" width="10" height="10" fill="#c0503a"/><text x="34" y="285" fill="#333">Reached public</text>')
    lines.append('<rect x="150" y="276" width="10" height="10" fill="#e3b341"/><text x="164" y="285" fill="#333">Uncertain</text>')
    lines.append('<rect x="250" y="276" width="10" height="10" fill="#2f7a5f"/><text x="264" y="285" fill="#333">Caught / internal</text>')
    lines.append('<text x="410" y="18" font-weight="bold" fill="#222">B. What caught them (detections)</text>')
    bars = detections()
    max_n = max(n for _, n, _ in bars)
    y = 32
    for label, n, dark in bars:
        w = 180 * n / max_n
        color = "#163f35" if dark else "#8aa79b"
        lines.append(f'<text x="552" y="{y + 11}" text-anchor="end" fill="#333">{label}</text>')
        lines.append(f'<rect x="560" y="{y}" width="{w:.1f}" height="14" fill="{color}"/>')
        lines.append(f'<text x="{560 + w + 4:.1f}" y="{y + 11}" fill="#333">{n}</text>')
        y += 20
    lines.append(
        '<text x="410" y="278" fill="#555" font-size="10">Dark: in-project AI review, 39 of 80 incidents (49%)</text>'
    )
    lines.append("</svg>")
    (ROOT / "fig-classes.svg").write_text("\n".join(lines) + "\n")


def figure_timeline():
    by = defaultdict(Counter)
    for row in ROWS:
        if row["date_recorded"]:
            by[row["date_recorded"]][row["reach"]] += 1
    days = [
        "2026-09-19", "2026-09-20", "2026-09-21", "2026-09-22", "2026-09-23",
        "2026-09-24", "2026-09-25", "2026-09-26", "2026-09-27", "2026-09-28",
        "2026-09-29", "2026-09-30", "2026-10-01", "2026-10-02", "2026-10-03",
    ]
    # Stated in the manuscript. Not fitted.
    controls = {
        "2026-09-24": "gate",
        "2026-09-25": "quality bar",
        "2026-09-26": "adversarial",
    }
    unit = 11.2
    base = 300
    left = 50
    pitch = 46
    lines = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 360" font-family="Helvetica,Arial,sans-serif" font-size="11">',
        '<rect width="100%" height="100%" fill="white"/>',
    ]
    for tick, label in ((0, "0"), (5, "5"), (10, "10"), (15, "15"), (20, "20")):
        y = base - tick * unit
        lines.append(f'<line x1="46" x2="740" y1="{y}" y2="{y}" stroke="#e2e2e2"/>')
        lines.append(f'<text x="40" y="{y + 4}" text-anchor="end" fill="#555">{label}</text>')
    for i, day in enumerate(days):
        x = left + i * pitch
        y = base
        total = sum(by[day].values())
        for reach in REACH_ORDER:
            n = by[day][reach]
            if not n:
                continue
            h = n * unit
            y -= h
            lines.append(f'<rect x="{x}" y="{y}" width="38" height="{h}" fill="{REACH_COLOR[reach]}"/>')
        if total:
            lines.append(f'<text x="{x + 19}" y="{y - 4}" text-anchor="middle" fill="#333">{total}</text>')
        lines.append(f'<text x="{x + 19}" y="316" text-anchor="middle" fill="#333">{day[-2:]}</text>')
        if day in controls:
            lines.append(
                f'<line x1="{x - 4}" x2="{x - 4}" y1="28" y2="{base}" stroke="#163f35" stroke-dasharray="3,3"/>'
            )
            lines.append(f'<text x="{x - 1}" y="24" fill="#163f35" font-size="9">{controls[day]}</text>')
    lines.append('<text x="250" y="332" text-anchor="middle" fill="#666">September</text>')
    lines.append('<text x="640" y="332" text-anchor="middle" fill="#666">October</text>')
    lines.append('<text x="380" y="350" text-anchor="middle" fill="#333">Date recorded, 2026</text>')
    lines.append('<text transform="translate(14,180) rotate(-90)" text-anchor="middle" fill="#333">Incidents</text>')
    lines.append('<rect x="46" y="6" width="11" height="11" fill="#c0503a"/><text x="62" y="15" fill="#333">Reached public</text>')
    lines.append('<rect x="176" y="6" width="11" height="11" fill="#e3b341"/><text x="192" y="15" fill="#333">Uncertain</text>')
    lines.append('<rect x="280" y="6" width="11" height="11" fill="#2f7a5f"/><text x="296" y="15" fill="#333">Caught / internal</text>')
    lines.append('<line x1="430" x2="450" y1="11" y2="11" stroke="#163f35" stroke-dasharray="3,3"/><text x="456" y="15" fill="#333">control dated in the text</text>')
    lines.append("</svg>")
    (ROOT / "fig-timeline.svg").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    figure_classes()
    figure_timeline()
    print("wrote fig-classes.svg and fig-timeline.svg")
