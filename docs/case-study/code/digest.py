"""The digest that binds the PDF to the files it was built from.

build_pdf.py writes it into the PDF's Keywords field. check_numbers.py
recomputes it and fails if the committed PDF was built from other files.
"""
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCES = (
    "ai-research-failure-modes.md",
    "fig-classes.svg",
    "fig-timeline.svg",
    "fig-overhead.svg",
)
TAG = "source-sha256"


def source_digest(texts=None):
    """sha256 over each source's name and bytes. texts maps name to str, for checks run in memory."""
    h = hashlib.sha256()
    for name in SOURCES:
        body = texts[name] if texts is not None else (ROOT / name).read_text()
        h.update(name.encode() + b"\0" + body.encode() + b"\0")
    return h.hexdigest()
