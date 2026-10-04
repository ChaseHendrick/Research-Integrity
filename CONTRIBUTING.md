# Contributing

Contributions are welcome, especially from people using AI assistants for research in fields other than mathematics.

## Proposing a rule

Every rule in the skill exists because of a failure that actually happened. A new rule should come with the same kind of evidence. Open an issue with:

1. **What happened**: the claim, check or citation that was wrong, and how it was found. A link to a public record is best: a commit, a review note or a correction.
2. **Why it was not obvious**: why the failure looked reasonable at the time.
3. **The rule** that would have caught it, phrased as an instruction Claude can follow.

Rules without a real failure behind them are unlikely to be added. The skill stays short so that Claude actually follows it.

## Changing the skill

- Keep `SKILL.md` short and concrete. Prefer one clear instruction over a paragraph of advice.
- Keep the frontmatter `description` under 1024 characters. It decides when Claude loads the skill.
- Run `python3 scripts/validate.py`, `python3 docs/case-study/code/check_numbers.py`, and `python3 scripts/gate.py` before opening a pull request. CI runs them too.
- Add a line to `CHANGELOG.md`, and bump `version` in `plugins/research-integrity/.claude-plugin/plugin.json`.

## Reporting a problem

If the skill makes Claude worse at something, for example by refusing reasonable claims or adding noise to simple answers, open an issue with the prompt and what happened.
