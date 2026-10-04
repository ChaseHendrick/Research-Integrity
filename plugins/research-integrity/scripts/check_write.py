#!/usr/bin/env python3
"""PreToolUse hook for Write and Edit.

Warns when the text about to be written contains an overclaim phrase.
Blocks only if the project file .research-integrity.json says {"block": true}.
No network. A missing or unreadable config does not block.
"""
import json
import sys
from pathlib import Path

from phrases import scan

MAX_CHARS = 200_000


def project_blocks(file_path):
    roots = [Path.cwd()]
    if file_path:
        roots.append(Path(file_path).resolve().parent)
    seen = set()
    for root in roots:
        try:
            current = root.resolve()
        except OSError:
            continue
        for _ in range(6):
            if current in seen:
                break
            seen.add(current)
            config = current / ".research-integrity.json"
            if config.is_file():
                try:
                    data = json.loads(config.read_text(encoding="utf-8"))
                except (OSError, json.JSONDecodeError):
                    return False
                return bool(isinstance(data, dict) and data.get("block") is True)
            if current.parent == current:
                break
            current = current.parent
    return False


def proposed_text(tool_input):
    if not isinstance(tool_input, dict):
        return "", ""
    path = tool_input.get("file_path") or tool_input.get("path") or ""
    if isinstance(tool_input.get("content"), str):
        return path, tool_input["content"]
    if isinstance(tool_input.get("new_string"), str):
        return path, tool_input["new_string"]
    return path, ""


def inside_plugin(path):
    if not path:
        return False
    root = Path(__file__).resolve().parents[1]
    try:
        Path(path).resolve().relative_to(root)
        return True
    except ValueError:
        return False


def judge(text, block):
    if not text or len(text) > MAX_CHARS:
        return 0, ""
    hits = scan(text)
    if not hits:
        return 0, ""
    shown = ", ".join(f"{h['phrase']} (line {h['line']})" for h in hits[:8])
    if block:
        return 2, (
            f"Blocked write. Overclaim phrase: {shown}. "
            "Rephrase with how far the search went, or set block to false in "
            ".research-integrity.json. A hit is not proof the sentence is false."
        )
    return 0, (
        f"Overclaim phrase, not blocked: {shown}. "
        "The write proceeded. Set {\"block\": true} in .research-integrity.json "
        "to refuse these writes."
    )


def self_test():
    code, message = judge("This is the first proof.\n", False)
    if code != 0 or "this is the first" not in message:
        raise SystemExit(f"FAIL warn path: {code} {message}")
    code, message = judge("This is the first proof.\n", True)
    if code != 2 or not message:
        raise SystemExit(f"FAIL block path did not block: {code} {message}")
    code, message = judge("Searches of X found no earlier statement.\n", True)
    if code != 0 or message:
        raise SystemExit(f"FAIL clean text was blocked: {code} {message}")
    print("OK check_write: warn, block, and clean paths")


def main():
    if "--self-test" in sys.argv:
        self_test()
        return
    raw = sys.stdin.read()
    if not raw.strip():
        return
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        return
    tool_input = payload.get("tool_input") or {}
    path, text = proposed_text(tool_input)
    if inside_plugin(path):
        return
    code, message = judge(text, project_blocks(path))
    if message:
        print(message, file=sys.stderr)
    raise SystemExit(code)


if __name__ == "__main__":
    main()
