#!/usr/bin/env python3
"""Validate the marketplace, plugin manifest and SKILL.md frontmatter. Exits 1 on any failure."""
import json, pathlib, re, sys

root = pathlib.Path(__file__).resolve().parent.parent
errors = []

def load(path):
    try:
        return json.loads((root / path).read_text())
    except Exception as e:
        errors.append(f"{path}: {e}")
        return {}

market = load(".claude-plugin/marketplace.json")
for key in ("name", "owner", "plugins"):
    if key not in market:
        errors.append(f"marketplace.json: missing '{key}'")

for entry in market.get("plugins", []):
    src = root / entry.get("source", "")
    manifest = load(str((src / ".claude-plugin/plugin.json").relative_to(root)))
    if manifest.get("name") != entry.get("name"):
        errors.append(f"{entry.get('name')}: marketplace name does not match plugin.json name")
    if not re.fullmatch(r"\d+\.\d+\.\d+", manifest.get("version", "")):
        errors.append(f"{entry.get('name')}: version is not semver")
    skills = sorted(src.glob("skills/*/SKILL.md"))
    if not skills:
        errors.append(f"{entry.get('name')}: no skills found")
    for skill in skills:
        text = skill.read_text()
        m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
        if not m:
            errors.append(f"{skill.relative_to(root)}: missing frontmatter")
            continue
        front = m.group(1)
        name = re.search(r"^name:\s*(\S+)", front, re.M)
        if not name or name.group(1) != skill.parent.name:
            errors.append(f"{skill.relative_to(root)}: 'name' must match its folder")
        desc = re.search(r"^description:\s*>?\s*\n?((?:.|\n)*?)(?=^\w+:|\Z)", front, re.M)
        if not desc or not desc.group(1).strip():
            errors.append(f"{skill.relative_to(root)}: missing description")
        elif len(" ".join(desc.group(1).split())) > 1024:
            errors.append(f"{skill.relative_to(root)}: description over 1024 characters")

if errors:
    print("\n".join("FAIL " + e for e in errors))
    sys.exit(1)
print("OK: marketplace, plugin manifest and skill frontmatter are valid")
