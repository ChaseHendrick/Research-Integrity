#!/usr/bin/env python3
"""Local MCP server. Stdio, newline-delimited JSON-RPC, no network.

Tools:
  scan_text     report overclaim phrases in a passage
  read_field    copy one named field out of a file under the project
  append_search append one search row the caller already stated
"""
import json
import os
import sys
from pathlib import Path

from phrases import scan

MAX_FILE = 1_000_000


def project_root():
    return Path.cwd().resolve()


def inside_project(path):
    root = project_root()
    try:
        Path(path).resolve().relative_to(root)
        return True
    except ValueError:
        return False


def read_field(path, field, row):
    if not field or not str(field).strip():
        raise ValueError("field is empty")
    candidate = Path(path)
    if not candidate.is_absolute():
        candidate = project_root() / candidate
    if not inside_project(candidate):
        raise ValueError("path is outside the project")
    if not candidate.is_file():
        raise ValueError("file does not exist")
    if candidate.stat().st_size > MAX_FILE:
        raise ValueError("file is over 1 MB")
    raw = candidate.read_text(encoding="utf-8")
    field = str(field)
    stripped = raw.lstrip()
    if stripped.startswith("{") or stripped.startswith("["):
        return _json_field(raw, field)
    if "," in raw.splitlines()[0]:
        return _csv_field(raw, field, row)
    return _line_field(raw, field)


def _json_field(raw, field):
    # Copy the source text of a top-level value. json.loads would reprint numbers.
    pattern = rf'"{re_escape(field)}"\s*:\s*("(?:\\.|[^"\\])*"|-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?|true|false|null)'
    import re
    found = re.search(pattern, raw)
    if not found:
        raise ValueError(f"{field} is not a top-level string, number, or literal in this file")
    value = found.group(1)
    if value.startswith('"'):
        value = json.loads(value)
    return value


def re_escape(text):
    import re
    return re.escape(text)


def _csv_field(raw, field, row):
    import csv
    import io
    rows = list(csv.DictReader(io.StringIO(raw)))
    if not rows or field not in rows[0]:
        raise ValueError(f"{field} is not a CSV column")
    if row is None:
        if len(rows) != 1:
            raise ValueError(f"column {field} has {len(rows)} rows; pass row")
        row = 0
    row = int(row)
    if row < 0 or row >= len(rows):
        raise ValueError(f"row {row} is outside 0..{len(rows) - 1}")
    return rows[row][field]


def _line_field(raw, field):
    prefix = field + "="
    prefix_colon = field + ":"
    for line in raw.splitlines():
        stripped = line.strip()
        if stripped.startswith(prefix) or stripped.startswith(prefix_colon):
            return stripped.split("=", 1)[-1].split(":", 1)[-1].strip()
    raise ValueError(f"{field} is not a key=value or key: value line")


def append_search(query, opened, blocked, stopped, conclusion):
    if not str(query).strip():
        raise ValueError("query is empty; a search that was not run is not a row")
    directory = project_root() / ".research-integrity"
    directory.mkdir(exist_ok=True)
    path = directory / "searches.jsonl"
    row = {
        "query": query,
        "opened": opened,
        "blocked": blocked,
        "stopped": stopped,
        "conclusion": conclusion,
    }
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    return {"path": str(path), "row": row}


def tool_scan(arguments):
    text = arguments.get("text")
    if not isinstance(text, str):
        raise ValueError("text must be a string")
    hits = scan(text)
    return {"hits": hits, "not_claimed": "A hit is not proof the sentence is false."}


def call_tool(name, arguments):
    arguments = arguments or {}
    if name == "scan_text":
        return tool_scan(arguments)
    if name == "read_field":
        value = read_field(arguments.get("path", ""), arguments.get("field", ""), arguments.get("row"))
        return {"value": value, "field": arguments.get("field"), "not_claimed": "This is the stored text, not a new measurement."}
    if name == "append_search":
        return append_search(
            arguments.get("query", ""),
            arguments.get("opened", ""),
            arguments.get("blocked", ""),
            arguments.get("stopped", ""),
            arguments.get("conclusion", ""),
        )
    raise ValueError(f"unknown tool {name}")


TOOLS = [
    {
        "name": "scan_text",
        "description": "Report overclaim phrases in a passage. A hit is not proof the sentence is false. No network.",
        "inputSchema": {
            "type": "object",
            "properties": {"text": {"type": "string"}},
            "required": ["text"],
            "additionalProperties": False,
        },
    },
    {
        "name": "read_field",
        "description": "Copy one named field from a JSON object, a CSV column, or a key=value line under the project. Does not read outside the project and does not fetch.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "path": {"type": "string"},
                "field": {"type": "string"},
                "row": {"type": "integer", "description": "CSV row, from 0. Required when the column has more than one row."},
            },
            "required": ["path", "field"],
            "additionalProperties": False,
        },
    },
    {
        "name": "append_search",
        "description": "Append one search row the caller already stated to .research-integrity/searches.jsonl in the project. Refuses an empty query. Does not search.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "opened": {"type": "string"},
                "blocked": {"type": "string"},
                "stopped": {"type": "string"},
                "conclusion": {"type": "string"},
            },
            "required": ["query", "opened", "blocked", "stopped", "conclusion"],
            "additionalProperties": False,
        },
    },
]


def result(message_id, payload):
    return {"jsonrpc": "2.0", "id": message_id, "result": payload}


def error(message_id, code, message):
    return {"jsonrpc": "2.0", "id": message_id, "error": {"code": code, "message": message}}


def handle(message):
    method = message.get("method")
    message_id = message.get("id")
    if method == "initialize":
        version = (message.get("params") or {}).get("protocolVersion") or "2024-11-05"
        return result(message_id, {
            "protocolVersion": version,
            "capabilities": {"tools": {}},
            "serverInfo": {"name": "research-integrity", "version": "1.4.1"},
        })
    if method and method.startswith("notifications/"):
        return None
    if method == "ping":
        return result(message_id, {})
    if method == "tools/list":
        return result(message_id, {"tools": TOOLS})
    if method == "tools/call":
        params = message.get("params") or {}
        try:
            payload = call_tool(params.get("name"), params.get("arguments"))
        except (ValueError, OSError, KeyError) as exc:
            return result(message_id, {"content": [{"type": "text", "text": str(exc)}], "isError": True})
        return result(message_id, {
            "content": [{"type": "text", "text": json.dumps(payload, ensure_ascii=False)}],
            "isError": False,
        })
    if message_id is None:
        return None
    return error(message_id, -32601, f"method not found: {method}")


def serve():
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            message = json.loads(line)
        except json.JSONDecodeError:
            continue
        reply = handle(message)
        if reply is None:
            continue
        sys.stdout.write(json.dumps(reply, ensure_ascii=False) + "\n")
        sys.stdout.flush()


def self_test():
    import tempfile
    hits = call_tool("scan_text", {"text": "This is the first proof.\n"})
    if not hits["hits"]:
        raise SystemExit("FAIL scan_text missed the planted phrase")
    clean = call_tool("scan_text", {"text": "Searches of X found no earlier statement.\n"})
    if clean["hits"]:
        raise SystemExit("FAIL scan_text flagged a bounded sentence")
    try:
        call_tool("append_search", {"query": "  ", "opened": "", "blocked": "", "stopped": "", "conclusion": ""})
    except ValueError:
        pass
    else:
        raise SystemExit("FAIL empty query was written")
    with tempfile.TemporaryDirectory() as tmp:
        previous = Path.cwd()
        os.chdir(tmp)
        outside = Path(tempfile.gettempdir()) / "ri-outside-field.txt"
        outside.write_text("marker=1\n", encoding="utf-8")
        try:
            try:
                read_field(str(outside), "marker", None)
            except ValueError:
                pass
            else:
                raise SystemExit("FAIL read_field followed a path outside the project")
            sample = Path(tmp) / "run.json"
            sample.write_text('{"agreement": "4.5e-21", "other": "6e-25"}\n', encoding="utf-8")
            copied = read_field("run.json", "agreement", None)
            if copied != "4.5e-21":
                raise SystemExit(f"FAIL read_field copied {copied!r}")
            try:
                read_field("run.json", "missing", None)
            except ValueError:
                pass
            else:
                raise SystemExit("FAIL missing field returned a value")
        finally:
            os.chdir(previous)
            outside.unlink(missing_ok=True)
    init = handle({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2024-11-05"}})
    if init["result"]["serverInfo"]["name"] != "research-integrity":
        raise SystemExit("FAIL initialize")
    print("OK server: phrase scan, empty search refused, outside path refused, field copied")


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        self_test()
    else:
        serve()
