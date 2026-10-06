#!/usr/bin/env python3
"""Build ai-research-failure-modes.pdf from the Markdown manuscript and its SVG figures.

Uses fpdf2 and markdown (pure Python) and the Liberation Serif fonts.
The PDF's Keywords field carries the sha256 of the manuscript and figures it
was built from, so check_numbers.py can tell when the committed PDF is stale.
The creation date is the manuscript's own date, so a rebuild of the same
sources on the same versions of fpdf2 and the fonts gives the same file.
"""
import re
from datetime import datetime, timezone
from pathlib import Path

import markdown
from fpdf import FPDF

from digest import TAG, source_digest

ROOT = Path(__file__).resolve().parent.parent
FONT_DIR = Path("/usr/share/fonts/truetype/liberation")
FONTS = {
    "": FONT_DIR / "LiberationSerif-Regular.ttf",
    "B": FONT_DIR / "LiberationSerif-Bold.ttf",
    "I": FONT_DIR / "LiberationSerif-Italic.ttf",
    "BI": FONT_DIR / "LiberationSerif-BoldItalic.ttf",
}
MONTHS = "January February March April May June July August September October November December".split()
FIGURE = re.compile(r"^!\[([^\]]*)\]\(([^)]+\.svg)\)\s*$", re.M)
SUPERSCRIPT = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹⁻", "0123456789-")


def to_html(md):
    body = markdown.markdown(md, extensions=["tables", "sane_lists", "smarty"])
    # Liberation Serif has no Unicode superscripts, and <sup> cannot sit inside a table cell here.
    body = re.sub(r"[⁰¹²³⁴⁵⁶⁷⁸⁹⁻]+", lambda m: "^" + m.group(0).translate(SUPERSCRIPT), body)
    body = body.replace("<h1>", "<h2>").replace("</h1>", "</h2>")
    # fpdf2 cannot nest <code> inside a table cell.
    return body.replace("<code>", "").replace("</code>", "")


def manuscript_date(src):
    m = re.search(r"^Version (\d+\.\d+) · (\d{1,2}) (\w+) (\d{4})", src, re.M)
    if not m:
        raise SystemExit("manuscript has no 'Version X.Y · D Month YYYY' line")
    version, day, month, year = m.groups()
    when = datetime(int(year), MONTHS.index(month) + 1, int(day), tzinfo=timezone.utc)
    return version, when


def main():
    missing = [p for p in FONTS.values() if not p.is_file()]
    if missing:
        raise SystemExit("missing fonts: " + ", ".join(str(p) for p in missing))
    src = (ROOT / "ai-research-failure-modes.md").read_text()
    version, when = manuscript_date(src)

    pdf = FPDF(format="letter")
    pdf.set_auto_page_break(auto=True, margin=18)
    for style, path in FONTS.items():
        pdf.add_font("Body", style, str(path))
    pdf.set_font("Body", size=10)
    pdf.set_title("Eighty Failures: Error Modes and Controls in AI-Assisted Mathematical Research")
    pdf.set_author("Chase Hendrick")
    pdf.set_subject(f"Case study, version {version}")
    pdf.set_keywords(f"{TAG} {source_digest()}")
    pdf.set_creator("docs/case-study/code/build_pdf.py")
    pdf.set_creation_date(when)
    pdf.add_page()

    pos = 0
    figures = 0
    for m in FIGURE.finditer(src):
        pdf.write_html(to_html(src[pos:m.start()]))
        caption, name = m.group(1), m.group(2)
        pdf.ln(2)
        pdf.image(str(ROOT / name), w=pdf.epw)
        pdf.ln(1)
        pdf.write_html(f"<p><i>{to_html(caption)[3:-4]}</i></p>")
        figures += 1
        pos = m.end()
    pdf.write_html(to_html(src[pos:]))

    out = ROOT / "ai-research-failure-modes.pdf"
    pdf.output(str(out))
    print(f"wrote {out.name} ({out.stat().st_size} bytes, {pdf.pages_count} pages, {figures} figures)")


if __name__ == "__main__":
    main()
