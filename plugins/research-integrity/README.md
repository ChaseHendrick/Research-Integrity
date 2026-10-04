# Research integrity

Instructions for an assistant that is searching literature, checking a proof, running a numerical argument, or preparing a preprint. The skill is `skills/research-integrity/SKILL.md`.

On Claude Code, and on Cowork when the session is on your computer, the plugin also starts two local pieces. Neither opens a network connection, and neither runs in Claude Chat. The skill zip uploaded to Chat is the instructions only.

**Local server.** `.mcp.json` runs `scripts/server.sh`, which starts `scripts/server.py`. The tools are `scan_text` (report a few overclaim phrases), `read_field` (copy one named field from a file in the project), and `append_search` (append a search row you already stated to `.research-integrity/searches.jsonl` in the project). `read_field` refuses a path outside the project. `append_search` refuses an empty query. Nothing is sent off the machine. The programs do not read the process environment.

**Hook.** `hooks/hooks.json` runs `scripts/check_write.sh`, which starts `scripts/check_write.py`, before Write and Edit. It looks at the text about to be written. By default it warns and lets the write through. It blocks only if the project has `.research-integrity.json` with `"block": true`. A missing or broken config does not block.

The rules come from a public record of 80 failures in one research project. The hook and the server do not measure whether those rules reduce errors. This plugin is not an Anthropic product.
