#!/usr/bin/env python3
"""Draw Figures 1–3.

Figures 1 and 2 are counted from incidents.csv.
Control dates are the ones stated in the manuscript, not estimated.
Figure 3 is not counted from the CSV. It redraws the five session totals
already printed on that figure.
"""
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
REACH_COLOR = {
    "public": "#8f3b2e",
    "uncertain": "#9a7430",
    "caught/internal": "#1c4c3e",
}
INK = "#1c1916"
MUTED = "#6f675e"
RULE = "#e4ddd2"
HAIR = "#f3efe8"
PAPER = "#ffffff"
SERIF = "Georgia, Palatino, 'Palatino Linotype', 'Liberation Serif', serif"

# Session totals already printed on Figure 3. Not remeasured here.
OVERHEAD = [
    ("Full setup", 65600),
    ("No MCP servers", 42326),
    ("Also no skills", 39584),
    ("Also no user plugins/settings (bare)", 34068),
    ("Bare, no tools", 2864),
]


def fmt(v):
    v = round(float(v), 2)
    if abs(v - round(v)) < 1e-6:
        return str(int(round(v)))
    text = f"{v:.2f}".rstrip("0").rstrip(".")
    return text


def comma(n):
    return f"{n:,}"


def text(x, y, body, size=12, fill=INK, anchor="start", weight="normal"):
    extra = "" if weight == "normal" else f' font-weight="{weight}"'
    return (
        f'<text x="{fmt(x)}" y="{fmt(y)}" text-anchor="{anchor}" fill="{fill}" '
        f'font-size="{size}"{extra}>{body}</text>'
    )


def detections():
    # Order and labels match Table 2. Filled marks are the two in-project AI reviews.
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
    bars = detections()
    width, height = 700, 668
    label_x = 236
    dot_x = 252
    radius = 3.4
    pitch = 11
    row_y0 = 78
    row_h = 34
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'font-family="{SERIF}">',
        f'<rect width="100%" height="100%" fill="{PAPER}"/>',
        f'<title>Incidents by class and reach, and detections by control</title>',
        text(28, 32, "A", 15),
        text(48, 32, "Incidents by class and reach", 15),
        text(28, 50, "Each dot is one incident", 11, MUTED),
    ]
    totals = []
    for i, (code, label) in enumerate(CLASS_ORDER):
        subset = [r for r in ROWS if r["class"] == code]
        cy = row_y0 + i * row_h
        lines.append(text(label_x, cy + 4, label, 12.5, anchor="end"))
        x = dot_x
        for reach in REACH_ORDER:
            n = sum(1 for r in subset if r["reach"] == reach)
            if not n:
                continue
            color = REACH_COLOR[reach]
            for k in range(n):
                cx = x + radius + k * pitch
                lines.append(
                    f'<circle cx="{fmt(cx)}" cy="{fmt(cy)}" r="{radius}" fill="{color}"/>'
                )
            end = x + radius + (n - 1) * pitch + radius
            lines.append(text(end + 7, cy + 3.5, str(n), 10, MUTED))
            x = end + 7 + (14 if n < 10 else 20) + 12
        totals.append((cy, len(subset)))
    total_x = 668
    lines.append(
        f'<line x1="{total_x - 28}" y1="60" x2="{total_x - 28}" y2="{row_y0 + 4 * row_h + 12}" '
        f'stroke="{RULE}" stroke-width="1"/>'
    )
    for cy, n in totals:
        lines.append(text(total_x, cy + 4, str(n), 13, anchor="end"))
    legend_y = row_y0 + 5 * row_h + 6
    legend = [
        (28, "Reached public", REACH_COLOR["public"]),
        (176, "Uncertain", REACH_COLOR["uncertain"]),
        (300, "Caught / internal", REACH_COLOR["caught/internal"]),
    ]
    for x, name, color in legend:
        lines.append(f'<circle cx="{x + 4}" cy="{fmt(legend_y - 3)}" r="3.4" fill="{color}"/>')
        lines.append(text(x + 14, legend_y, name, 11.5, MUTED))

    panel_b = legend_y + 46
    lines.append(text(28, panel_b, "B", 15))
    lines.append(text(48, panel_b, "What caught them", 15))
    lines.append(text(28, panel_b + 18, "Detections. One incident can have more than one.", 11, MUTED))
    axis_x = 268
    axis_w = 360
    scale = 30
    top = panel_b + 46
    plot_bottom = top + (len(bars) - 1) * 26
    for tick in (0, 10, 20, 30):
        x = axis_x + axis_w * tick / scale
        lines.append(
            f'<line x1="{fmt(x)}" y1="{fmt(top - 16)}" x2="{fmt(x)}" y2="{fmt(plot_bottom + 10)}" '
            f'stroke="{HAIR if tick else RULE}" stroke-width="1"/>'
        )
        lines.append(text(x, top - 22, str(tick), 10, MUTED, anchor="middle"))
    for i, (label, n, dark) in enumerate(bars):
        cy = top + i * 26
        x = axis_x + axis_w * n / scale
        lines.append(text(axis_x - 12, cy + 4, label, 12.5, anchor="end"))
        lines.append(
            f'<line x1="{axis_x}" y1="{fmt(cy)}" x2="{fmt(x)}" y2="{fmt(cy)}" '
            f'stroke="{"#163f35" if dark else "#cfc6ba"}" stroke-width="1.25"/>'
        )
        if dark:
            lines.append(f'<circle cx="{fmt(x)}" cy="{fmt(cy)}" r="3.6" fill="#163f35"/>')
        else:
            lines.append(
                f'<circle cx="{fmt(x)}" cy="{fmt(cy)}" r="3.4" fill="{PAPER}" '
                f'stroke="#163f35" stroke-width="1.25"/>'
            )
        lines.append(text(x + 10, cy + 4, str(n), 12))
    note_y = plot_bottom + 32
    lines.append(
        text(
            28,
            note_y,
            "Filled marks: in-project AI review, 39 of 80 incidents (49%).",
            11.5,
            MUTED,
        )
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
    width, height = 760, 430
    unit = 6.4
    col_w = 9
    base = 328
    left = 58
    pitch = 44
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'font-family="{SERIF}">',
        f'<rect width="100%" height="100%" fill="{PAPER}"/>',
        "<title>Incidents by the date they were recorded</title>",
        text(28, 24, "Incidents by the date they were recorded", 15),
    ]
    legend = [
        (28, "Reached public", REACH_COLOR["public"]),
        (168, "Uncertain", REACH_COLOR["uncertain"]),
        (280, "Caught / internal", REACH_COLOR["caught/internal"]),
    ]
    for x, name, color in legend:
        lines.append(f'<rect x="{x}" y="38" width="8" height="8" fill="{color}"/>')
        lines.append(text(x + 12, 46, name, 11.5, MUTED))
    key = ["gate", "quality bar", "adversarial"]
    kx = 430
    for name in key:
        lines.append(
            f'<line x1="{kx}" y1="42" x2="{kx + 14}" y2="42" stroke="#163f35" '
            f'stroke-width="1" stroke-dasharray="1.5 2"/>'
        )
        lines.append(text(kx + 18, 46, name, 11, MUTED))
        kx += 110
    for tick in (0, 5, 10, 15, 20):
        y = base - tick * unit
        lines.append(
            f'<line x1="48" y1="{fmt(y)}" x2="730" y2="{fmt(y)}" stroke="{HAIR}" stroke-width="1"/>'
        )
        lines.append(text(40, y + 3, str(tick), 10, MUTED, anchor="end"))
    lines.append(f'<line x1="48" y1="{base}" x2="730" y2="{base}" stroke="{INK}" stroke-width="1"/>')
    for i, day in enumerate(days):
        x = left + i * pitch
        if day in controls:
            mark = x - 8
            lines.append(
                f'<line x1="{mark}" y1="62" x2="{mark}" y2="{base}" stroke="#163f35" '
                f'stroke-width="1" stroke-dasharray="1.5 2.5"/>'
            )
        y = base
        total = sum(by[day].values())
        for reach in REACH_ORDER:
            n = by[day][reach]
            if not n:
                continue
            h = n * unit
            y -= h
            lines.append(
                f'<rect x="{fmt(x)}" y="{fmt(y)}" width="{col_w}" height="{fmt(h)}" '
                f'fill="{REACH_COLOR[reach]}"/>'
            )
        if total:
            lines.append(text(x + col_w / 2, y - 6, str(total), 11, anchor="middle"))
        lines.append(text(x + col_w / 2, base + 16, str(int(day[-2:])), 11, MUTED, anchor="middle"))
    sep0 = left + col_w / 2
    sep1 = left + 11 * pitch + col_w / 2
    oct0 = left + 12 * pitch + col_w / 2
    oct1 = left + 14 * pitch + col_w / 2
    lines.append(f'<line x1="{fmt(sep0)}" y1="{base + 28}" x2="{fmt(sep1)}" y2="{base + 28}" stroke="{RULE}"/>')
    lines.append(f'<line x1="{fmt(oct0)}" y1="{base + 28}" x2="{fmt(oct1)}" y2="{base + 28}" stroke="{RULE}"/>')
    lines.append(text((sep0 + sep1) / 2, base + 44, "September", 12, MUTED, anchor="middle"))
    lines.append(text((oct0 + oct1) / 2, base + 44, "October", 12, MUTED, anchor="middle"))
    lines.append(text(380, base + 66, "Date recorded, 2026", 12, MUTED, anchor="middle"))
    lines.append(
        f'<text transform="translate(16,210) rotate(-90)" text-anchor="middle" fill="{MUTED}" '
        f'font-size="12">Incidents</text>'
    )
    lines.append("</svg>")
    (ROOT / "fig-timeline.svg").write_text("\n".join(lines) + "\n")


def figure_overhead():
    width, height = 720, 292
    axis_x = 292
    axis_w = 340
    scale = 70000
    top = 72
    row_h = 36
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'font-family="{SERIF}">',
        f'<rect width="100%" height="100%" fill="{PAPER}"/>',
        "<title>Context carried by one fresh session before any work</title>",
        text(28, 26, "Context carried by one fresh Claude Code session before any work", 14),
        text(28, 46, "Tokens. Each row switches one more component off.", 11.5, MUTED),
    ]
    for tick in (0, 20000, 40000, 60000):
        x = axis_x + axis_w * tick / scale
        lines.append(text(x, top - 14, comma(tick), 10, MUTED, anchor="middle"))
        lines.append(
            f'<line x1="{fmt(x)}" y1="{top - 6}" x2="{fmt(x)}" y2="{fmt(top + 4 * row_h + 8)}" '
            f'stroke="{HAIR if tick else RULE}" stroke-width="1"/>'
        )
    for i, (label, n) in enumerate(OVERHEAD):
        cy = top + i * row_h
        x = axis_x + axis_w * n / scale
        lines.append(text(axis_x - 14, cy + 4, label, 12.5, anchor="end"))
        lines.append(
            f'<line x1="{axis_x}" y1="{fmt(cy)}" x2="{fmt(x)}" y2="{fmt(cy)}" '
            f'stroke="#163f35" stroke-width="1.35"/>'
        )
        lines.append(f'<circle cx="{fmt(x)}" cy="{fmt(cy)}" r="4" fill="#163f35"/>')
        lines.append(text(x + 10, cy + 4, comma(n), 12))
    lines.append(
        text(
            28,
            276,
            "Claude Code 2.1.286, Opus 5.5, one-turn claude -p sessions.",
            11,
            MUTED,
        )
    )
    lines.append("</svg>")
    (ROOT / "fig-overhead.svg").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    figure_classes()
    figure_timeline()
    figure_overhead()
    print("wrote fig-classes.svg, fig-timeline.svg and fig-overhead.svg")
