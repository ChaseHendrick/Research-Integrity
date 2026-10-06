# Changelog

## Unreleased

The skill is unchanged, so this is not a plugin release.

- Case study v1.18: Section 4.1 names N4, the last public incident that was not named in its class's section. It is the same kind of gap as V18 and V19 in v1.17.
- `check_numbers.py` now fails if a public incident is left out of its class's section, if Section 5.3 does not list every public incident dated after 25 September, or if Table B1 is not the differences between the Figure 3 totals. Ten planted faults are rejected first, up from seven.
- `CITATION.cff` names the case-study version, and the gate fails if it differs from the manuscript.
- `docs/case-study/code/requirements.txt` pins the two packages `build_pdf.py` needs, so that a rebuild gives the same PDF.

## 1.5.0 (2026-10-06)

A review of the 1.2.0–1.4.4 work, which was drafted with Grok, found that two of this repository's own checks could not fail, and that the skill told every project it was installed in that `scripts/gate.py` existed there.

Skill:
- Removed the sentence "This repository asked for it: `scripts/gate.py`" from the shipped skill. In a user's project it pointed at a program that is not there.
- Section 8 is renamed "a program gate instead of a checklist". The rule is unchanged and still off unless asked for.
- Rule 4 gains two sentences: anchor a match to the row or sentence that states the claim, and make a failure control exercise the code that decides. Section 8 asks for a reproducible build, so a downloaded archive can be compared byte for byte.

Checks in this repository:
- `scripts/gate.py`: its planted-count control raised its own error and never ran the comparison the real check used. Each control now writes its fault into a copy of the tree, and the real check must reject it for its own reason. The gate now also checks the README's class table, AI-review share and agreement figures against `incidents.csv`, the README's case-study version, the citation date against the changelog, and the shipped prose for overclaim phrases beyond the listed quotations.
- `scripts/gate.py` builds a reproducible zip, now with the license. `--compare FILE` checks a downloaded release asset against it.
- `docs/case-study/code/check_numbers.py`: it confirmed a Table 2 row by finding `| 3 |` anywhere in the manuscript, which a cell of Table 1 also matches, and it checked the figures for tokens such as `>1<` that any axis contains. It now checks Tables 1 and 2 row by row, the abstract counts, rates, κ and all 80 rows of Appendix A; compares each figure with a fresh drawing; and fails if the PDF was built from other sources. Seven planted faults must each be rejected first.
- Removed `scripts/checks/check_write.py` and `scripts/checks/server.py`. Nothing ran them after 1.4.4, and the server still reported version 1.4.1. `phrases.py` stays and the gate uses it.
- A release workflow publishes a release from the zip built on the released commit (a pushed tag, or a run by hand on main that creates the tag), then downloads it and compares.

Case study v1.17:
- Section 4.4 named three of the five public incidents in class V. V18 and V19 are now named.
- Section 5.4 states the 1.4.x releases in one sentence and records the two defects above. The manuscript names the skill release it describes rather than "the current" one, so a plugin release no longer forces a manuscript revision.
- The PDF shows the figures instead of naming them, and carries a digest of the files it was built from.
- Figures: the reach colors are re-stepped to pass a colorblind-safety check the old set failed; the timeline has wider columns and labels each control line directly. Counts unchanged.
- `README.md` names the plugin skill as `/research-integrity:research-integrity`.

## 1.4.4 (2026-10-04)

- The plugin ships no hook and no server. The directory follows a command only when the script has no variables and opens no path, which a checker cannot do. The phrase checks remain in `scripts/checks/` for this repository. They are not part of the plugin.
- Case study v1.16 records this release.

## 1.4.3 (2026-10-04)

- The hook and the server are the shell scripts themselves. They start no other program, so there is no second file for the directory to refuse to follow. The server only reports phrases. It does not open a file.
- Case study v1.15 records this release.

## 1.4.2 (2026-10-04)

- The hook and server scripts no longer compute a path. Each command is `${CLAUDE_PLUGIN_ROOT}` plus a fixed script name. An error string that said "pass row" is gone, and so is the author profile URL. The Python files those scripts start are still one level down, which the directory says a reviewer reads.
- Case study v1.14 records this release.

## 1.4.1 (2026-10-04)

- Directory validation. The hook and the server are started from shell scripts under the plugin path. Neither reads the process environment. A square PNG icon is at `.claude-plugin/icon.png`. The Python files those scripts start may still be held for a person to read.
- Case study v1.13 records this release.

## 1.4.0 (2026-10-04)

- A local MCP server and a Write/Edit hook, both stdlib Python, no network. The hook warns by default and blocks only when the project sets `"block": true`. Claude Chat does not run either.
- Case study v1.12 records this release.

## 1.3.0 (2026-10-04)

- Plugin listing fields for the Claude directory: `displayName`, and a README in the plugin folder that states the skill sends nothing and fetches nothing.
- Beating a checklist is optional. Rules 1–7 stay on. Section 8 applies only when someone asks, or when the project already has a gate they chose. This repository still runs `scripts/gate.py`.
- Case study v1.11 records that choice.

## 1.2.0 (2026-10-04)

- Goal: beat a checklist. A release gate is a committed program that recomputes public counts and fails on a planted fault, not a box the drafting session can tick.
- Rule 8 in the skill. A public error is dated by the artifact that shipped. A contribution sentence says what it does not claim and how far the sources were read.
- `scripts/gate.py` holds this repository to that rule and builds `research-integrity.zip`.

Also in this tag (listed as Unreleased until 1.5.0):

- Case study v1.10: the manuscript names skill release 1.2.0, and says rule 8 was not a control during the study window.
- Case study v1.9: the commit counts now match `98e7fc4`. The history has 315 commits from 17 September, not a root on 22 September and not 151 commits. The 55 Zenodo DOIs are the distinct identifiers in `papers/papers.json`. `docs/EVIDENCE.md` records the skill 1.1.0 sentences that were not controls during the window.
- Case study v1.8: Section 5.2 is the protocol on 3 October. Skill 1.1.0, committed the next day, is recorded separately in Section 5.4 and is not treated as having been in force during the window.
- Case study v1.7: the claim to be unaware of an earlier record is withdrawn. Section 1.1 compares Weinhold (2026), Li et al. (2026), Bui-Thanh (2026) and Yeung (2026), and the benchmark taxonomies those readings actually reached. κ is 0.905, recomputed from `incidents.csv`. The Poisson-solved line is no longer given as a coder disagreement. Figures 1 and 2 are drawn by `docs/case-study/code/make_figures.py`.
- Case study v1.6: the eleven incidents with no named control are assigned from the record that caught them, and Table 2 and Figure 1 are sorted by that count.
- Case study v1.5: Appendix B with the full session-overhead measurements and a third figure.
- Case study v1.4: connectors that silently fail to load as another source of false "nothing found" results.
- Case study v1.3: a new discussion section on the cost of the controls (measured session overhead and how usage limits cut verification short), links to the issues filed from it, and consistency fixes.
- Added the case study *Eighty Failures* (Markdown and PDF), its two figures and the 80-incident dataset under [docs/case-study/](docs/case-study/), and linked them from the README and the evidence page.

## 1.1.0 (2026-10-04)

Not tagged and not released on its own. Its changes first shipped in the v1.2.0 tag.

- The skill now requires a status on every claim (`proved`, `computer-assisted`, `cited`, `numerical`, `conjectured`), a hypothesis check before a cited theorem is applied, and a named source field for every public number.
- A check's failure control must fail for the reason under test. A cut-short search, check, or review is not a pass.
- Superseded priority wording has to be removed from every file that ships. Review notes name every AI tool used, and do not invent a co-author.

## 1.0.0 (2026-10-04)

First release.

- The `research-integrity` skill: seven rules, a pre-release quality checklist, and a table of phrases to avoid.
- Claude Code plugin marketplace, so the skill installs with `/plugin marketplace add ChaseHendrick/Research-Integrity`.
- A release ZIP for claude.ai and Cowork.
- Evidence for each rule ([docs/EVIDENCE.md](docs/EVIDENCE.md)) and worked examples ([docs/EXAMPLES.md](docs/EXAMPLES.md)).
