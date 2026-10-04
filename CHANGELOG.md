# Changelog

## Unreleased

- Plugin listing fields for the Claude directory: `displayName`, and a README in the plugin folder that states the skill sends nothing and fetches nothing.
- Case study v1.10: the manuscript names skill release 1.2.0, and says rule 8 was not a control during the study window.
- Case study v1.9: the commit counts now match `98e7fc4`. The history has 315 commits from 17 September, not a root on 22 September and not 151 commits. The 55 Zenodo DOIs are the distinct identifiers in `papers/papers.json`. `docs/EVIDENCE.md` records the skill 1.1.0 sentences that were not controls during the window.
- Case study v1.8: Section 5.2 is the protocol on 3 October. Skill 1.1.0, committed the next day, is recorded separately in Section 5.4 and is not treated as having been in force during the window.
- Case study v1.7: the claim to be unaware of an earlier record is withdrawn. Section 1.1 compares Weinhold (2026), Li et al. (2026), Bui-Thanh (2026) and Yeung (2026), and the benchmark taxonomies those readings actually reached. κ is 0.905, recomputed from `incidents.csv`. The Poisson-solved line is no longer given as a coder disagreement. Figures 1 and 2 are drawn by `docs/case-study/code/make_figures.py`.
- Case study v1.6: the eleven incidents with no named control are assigned from the record that caught them, and Table 2 and Figure 1 are sorted by that count.
- Case study v1.5: Appendix B with the full session-overhead measurements and a third figure.
- Case study v1.4: connectors that silently fail to load as another source of false "nothing found" results.
- Case study v1.3: a new discussion section on the cost of the controls (measured session overhead and how usage limits cut verification short), links to the issues filed from it, and consistency fixes.
- Added the case study *Eighty Failures* (Markdown and PDF), its two figures and the 80-incident dataset under [docs/case-study/](docs/case-study/), and linked them from the README and the evidence page.

## 1.4.2 (2026-10-04)

- The hook and server scripts no longer compute a path. Each command is `${CLAUDE_PLUGIN_ROOT}` plus a fixed script name. An error string that said "pass row" is gone, and so is the author profile URL. The Python files those scripts start are still one level down, which the directory says a reviewer reads.

## 1.4.1 (2026-10-04)

- Directory validation. The hook and the server are started from shell scripts under the plugin path. Neither reads the process environment. A square PNG icon is at `.claude-plugin/icon.png`. The Python files those scripts start may still be held for a person to read.

## 1.4.0 (2026-10-04)

- A local MCP server and a Write/Edit hook, both stdlib Python, no network. The hook warns by default and blocks only when the project sets `"block": true`. Claude Chat does not run either.

## 1.3.0 (2026-10-04)

- Beating a checklist is optional. Rules 1–7 stay on. Section 8 applies only when someone asks, or when the project already has a gate they chose. This repository still runs `scripts/gate.py`.
- Case study v1.11 records that choice.

## 1.2.0 (2026-10-04)

- Goal: beat a checklist. A release gate is a committed program that recomputes public counts and fails on a planted fault, not a box the drafting session can tick.
- Rule 8 in the skill. A public error is dated by the artifact that shipped. A contribution sentence says what it does not claim and how far the sources were read.
- `scripts/gate.py` holds this repository to that rule and builds `research-integrity.zip`.

## 1.1.0 (2026-10-04)

- The skill now requires a status on every claim (`proved`, `computer-assisted`, `cited`, `numerical`, `conjectured`), a hypothesis check before a cited theorem is applied, and a named source field for every public number.
- A check's failure control must fail for the reason under test. A cut-short search, check, or review is not a pass.
- Superseded priority wording has to be removed from every file that ships. Review notes name every AI tool used, and do not invent a co-author.

## 1.0.0 (2026-10-04)

First release.

- The `research-integrity` skill: seven rules, a pre-release quality checklist, and a table of phrases to avoid.
- Claude Code plugin marketplace, so the skill installs with `/plugin marketplace add ChaseHendrick/Research-Integrity`.
- A release ZIP for claude.ai and Cowork.
- Evidence for each rule ([docs/EVIDENCE.md](docs/EVIDENCE.md)) and worked examples ([docs/EXAMPLES.md](docs/EXAMPLES.md)).
