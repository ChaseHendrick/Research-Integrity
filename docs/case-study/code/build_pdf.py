#!/usr/bin/env python3
"""Build ai-research-failure-modes.pdf from the Markdown manuscript.

Uses fpdf2 (pure Python) and a DejaVu or Liberation font already on the machine.
Figures stay in the SVG files next to the manuscript; the PDF names them.
"""
import re
from pathlib import Path

import markdown
from fpdf import FPDF

ROOT = Path(__file__).resolve().parent.parent
FONT_DIR = Path("/usr/share/fonts/truetype/liberation")
FONTS = {
    "": FONT_DIR / "LiberationSerif-Regular.ttf",
    "B": FONT_DIR / "LiberationSerif-Bold.ttf",
    "I": FONT_DIR / "LiberationSerif-Italic.ttf",
    "BI": FONT_DIR / "LiberationSerif-BoldItalic.ttf",
}
missing = [p for p in FONTS.values() if not p.is_file()]
if missing:
    raise SystemExit("missing fonts: " + ", ".join(str(p) for p in missing))

src = (ROOT / "ai-research-failure-modes.md").read_text()
src = re.sub(
    r"!\[([^\]]*)\]\(([^)]+)\)",
    r"\n\n*[Figure file: \2. \1]*\n\n",
    src,
)
body = markdown.markdown(src, extensions=["tables", "sane_lists", "smarty"])
# Liberation Serif has no Unicode superscripts, and <sup> cannot sit inside a table cell here.
_sup = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹⁻", "0123456789-")
body = re.sub(r"[⁰¹²³⁴⁵⁶⁷⁸⁹⁻]+", lambda m: "^" + m.group(0).translate(_sup), body)
# fpdf2's HTML subset has no h1–h3 size control worth fighting; keep the tags it accepts.
body = body.replace("<h1>", "<h2>").replace("</h1>", "</h2>")
# fpdf2 cannot nest <code> inside a table cell.
body = body.replace("<code>", "").replace("</code>", "")

pdf = FPDF(format="letter")
pdf.set_auto_page_break(auto=True, margin=18)
pdf.add_page()
pdf.add_font("Body", "", str(FONTS[""]))
pdf.add_font("Body", "B", str(FONTS["B"]))
pdf.add_font("Body", "I", str(FONTS["I"]))
pdf.add_font("Body", "BI", str(FONTS["BI"]))
pdf.set_font("Body", size=10)
pdf.write_html(body)
out = ROOT / "ai-research-failure-modes.pdf"
pdf.output(out)
print(f"wrote {out} ({out.stat().st_size} bytes, {pdf.pages_count} pages)")
