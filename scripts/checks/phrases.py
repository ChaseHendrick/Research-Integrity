"""Overclaim phrases the skill tells an assistant not to ship as its own finding.

A hit is not a proof that the sentence is false. It is a phrase that, in this
project's record, was used to outrun the evidence. Lines in a fenced code block
or a markdown table are skipped: that is where the skill quotes the phrase in
order to forbid it.
"""
import re
import sys

PATTERNS = (
    ("this is the first", re.compile(r"this is the first\b", re.I)),
    ("no prior work exists", re.compile(r"no prior work exists", re.I)),
    ("independently reviewed", re.compile(r"independently reviewed", re.I)),
    ("externally reviewed", re.compile(r"externally reviewed", re.I)),
    ("we are not aware", re.compile(r"we are not aware", re.I)),
)


def scan(text):
    """Return a list of {phrase, line} hits. Empty means none of the phrases."""
    hits = []
    fenced = False
    for lineno, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if stripped.startswith("```"):
            fenced = not fenced
            continue
        if fenced or stripped.startswith("|"):
            continue
        for name, pattern in PATTERNS:
            if pattern.search(line):
                hits.append({"phrase": name, "line": lineno})
    return hits


def self_test():
    caught = scan("This is the first proof of the bound.\n")
    if not any(h["phrase"] == "this is the first" for h in caught):
        raise SystemExit("FAIL planted phrase was not caught")
    clean = scan(
        "Searches of the sources that loaded found no earlier statement. "
        "Two indexes did not open.\n"
    )
    if clean:
        raise SystemExit(f"FAIL clean sentence was flagged: {clean}")
    quoted = scan('| "This is the first ..." | "Say how far the search reached." |\n')
    if quoted:
        raise SystemExit("FAIL a table quoting the phrase was flagged")
    print("OK phrases: planted phrase caught, clean sentence passed, table skipped")


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        self_test()
    else:
        raise SystemExit("usage: phrases.py --self-test")
