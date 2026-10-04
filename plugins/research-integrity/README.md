# Research integrity

Instructions for an assistant that is searching literature, checking a proof, running a numerical argument, or preparing a preprint. The skill is `skills/research-integrity/SKILL.md`.

On Claude Code, and on Cowork when the session is on your computer, the plugin also starts two local pieces. Neither opens a network connection, and neither runs in Claude Chat. The skill zip uploaded to Chat is the instructions only.

**Local server.** `.mcp.json` runs `scripts/server.sh` and nothing else. The only tool is `scan_text`, which reports a few overclaim phrases in the text it is given. It does not open a file, does not start another program, and does not send anything off the machine.

**Hook.** `hooks/hooks.json` runs `scripts/check_write.sh` and nothing else, before Write and Edit. It looks at the raw text. By default it warns and lets the write through. It blocks only if the current directory has `.research-integrity.json` with `"block": true`. A missing file does not block.


The rules come from a public record of 80 failures in one research project. The hook and the server do not measure whether those rules reduce errors. This plugin is not an Anthropic product.
