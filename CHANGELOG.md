# Changelog

## Unreleased

- Case study v1.7: the claim to be unaware of an earlier record is withdrawn. Section 1.1 compares Weinhold (2026), Li et al. (2026), Bui-Thanh (2026) and Yeung (2026), and the benchmark taxonomies those readings actually reached. κ is 0.905, recomputed from `incidents.csv`. The Poisson-solved line is no longer given as a coder disagreement. Figures 1 and 2 are drawn by `docs/case-study/code/make_figures.py`.
- Case study v1.6: the eleven incidents with no named control are assigned from the record that caught them, and Table 2 and Figure 1 are sorted by that count.
- Case study v1.5: Appendix B with the full session-overhead measurements and a third figure.
- Case study v1.4: connectors that silently fail to load as another source of false "nothing found" results.
- Case study v1.3: a new discussion section on the cost of the controls (measured session overhead and how usage limits cut verification short), links to the issues filed from it, and consistency fixes.
- Added the case study *Eighty Failures* (Markdown and PDF), its two figures and the 80-incident dataset under [docs/case-study/](docs/case-study/), and linked them from the README and the evidence page.

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
