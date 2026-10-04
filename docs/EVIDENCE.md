# Where each rule comes from

Every rule in the skill answers failures that actually happened in [GENChase](https://github.com/ChaseHendrick/GENChase) between 19 September and 3 October 2026. Links point to commit [`98e7fc4`](https://github.com/ChaseHendrick/GENChase/tree/98e7fc4) so they keep showing the same lines.

A note on attribution: the repository does not record which AI assistant wrote any given sentence, so nothing here is a finding about a specific model.

## 1. Label every claim with how it is known

**What happened.** A web-search summary claimed a May 2024 preprint of a paper; no preprint could be found ([`RESEARCH.md:239`](https://github.com/ChaseHendrick/GENChase/blob/98e7fc4/RESEARCH.md#L239)). Another summary attributed a publisher's generic preprint policy to one specific journal, which a verifier identified as "the search model's inference, not text from any RCD or Pleiades page" ([`research-2026-09-24-unverified.md:395`](https://github.com/ChaseHendrick/GENChase/blob/98e7fc4/docs/wip/research-2026-09-24-unverified.md#L395)). Several novelty statements rested on papers seen only through search snippets.

**What changed.** Every gathered claim carries an access label, and "Do not take a search summary as a reading" ([`RESEARCH.md:140`](https://github.com/ChaseHendrick/GENChase/blob/98e7fc4/RESEARCH.md#L140)). Skill 1.1.0, committed on 4 October 2026 after the study commit, also requires a status: `proved`, `computer-assisted`, `cited`, `numerical`, or `conjectured`. An enclosure is not an exact value (W11, V13). A cited theorem is applied only after its hypotheses are checked against the instance (L11, L15). Those sentences were not controls during the window. The incident identifiers are the case study's.

## 2. Record what could not be searched

**What happened.** The cloud sessions' network policy blocked arXiv, Springer, Crossref, OpenAlex, Semantic Scholar, Wikipedia and most journal sites. Sessions searched sites that never loaded "and then write 'I did not find it' as if those sites had loaded" ([`RESEARCH.md:306`](https://github.com/ChaseHendrick/GENChase/blob/98e7fc4/RESEARCH.md#L306)).

**What changed.** A standing table of what could and could not be opened, and a log line for every search: query, opened, blocked, conclusion. "If you are an agent and you did not search, do not invent a row" ([`RESEARCH.md:865`](https://github.com/ChaseHendrick/GENChase/blob/98e7fc4/RESEARCH.md#L865)). Skill 1.1.0 adds that a search cut short is not evidence of absence (P6, P8).

## 3. Never infer novelty from a search

**What happened.** Five closed-form results on point-vortex collapse were presented as new and "the first public source of these formulas". The supporting search's own log says "Blocked: … Most journals." An audit requested by the owner reproduced the first result from Gröbli's 1877 dissertation, and later found the governing ratio in Kimura (1987). The audit's conclusion: "Confirmed novel findings among the five candidates: 0" ([`identities/NOVELTY-AUDIT.md`](https://github.com/ChaseHendrick/GENChase/blob/98e7fc4/identities/NOVELTY-AUDIT.md)). A personal name given to one classical result was retired.

**What changed.** "Claim originality from a numerical check or unsuccessful literature search" is forbidden ([`RESEARCH.md:302`](https://github.com/ChaseHendrick/GENChase/blob/98e7fc4/RESEARCH.md#L302)). Results take descriptive titles, never personal names, and classical sources are credited ([`AGENTS.md:19`](https://github.com/ChaseHendrick/GENChase/blob/98e7fc4/AGENTS.md#L19)). Skill 1.1.0 adds that a withdrawn priority sentence is deleted from every file that can ship, not only from the note that records the withdrawal (N4).

## 4. Every check must be able to fail

**What happened.** This was the largest class, with 20 incidents. An adversarial review of one paper's verification harness found:
- a check whose pattern "matches the line printed on success and on failure" ([`MATH.md:295`](https://github.com/ChaseHendrick/GENChase/blob/98e7fc4/papers/nf-pulse/review/MATH.md#L295));
- a test where "an error of 4.7e-2 still prints OK" ([`VERIFY.md:72`](https://github.com/ChaseHendrick/GENChase/blob/98e7fc4/papers/nf-pulse/review/VERIFY.md#L72));
- that "13 of the 16 integrator mutations still pass all 15 checks" ([`VERIFY.md:63`](https://github.com/ChaseHendrick/GENChase/blob/98e7fc4/papers/nf-pulse/review/VERIFY.md#L63)).

Elsewhere:
- "The claimed consistency check of the manifold recursion did not exist" ([`REPORT.md:289`](https://github.com/ChaseHendrick/GENChase/blob/98e7fc4/papers/nf-pulse/ext/faye-model/REPORT.md#L289));
- a symbolic check compared a polynomial with itself reordered;
- a proof step could accept results computed from an older version of its source ([`HANDOFF-2026-10-02-cardiac-rings-1.1.0-codex.md:65`](https://github.com/ChaseHendrick/GENChase/blob/98e7fc4/docs/HANDOFF-2026-10-02-cardiac-rings-1.1.0-codex.md#L65)).

A verification figure of 6 × 10⁻²⁵ shipped in a release; it "came from a mislabeled metric … the true figure is 4.5 × 10⁻²¹" ([`RESEARCH.md:155`](https://github.com/ChaseHendrick/GENChase/blob/98e7fc4/RESEARCH.md#L155)).

**What changed.** "A check that cannot miss is not a check" ([`AGENTS.md:161`](https://github.com/ChaseHendrick/GENChase/blob/98e7fc4/AGENTS.md#L161)). Every numerical record needs a failure control. Every verification claim in a paper maps to a committed check. Skill 1.1.0 adds three sentences that were not in force during the window: the control must fail for the reason under test (V7, V8); a public number is copied from a named field of the run, and the claimed domain is the proved domain (W1, W7, W8, W10); a check that was cut short, or that exists only in an uncommitted container, is not a pass (P6, P7, P8, P11).

## 5. Review adversarially, then doubt the reviewer

**What happened.** Separate AI sessions told to find errors caught 39 of the 80 incidents, more than any other control. But two checkers given the same 26 claims agreed on only 12. And on one paper, the check that review fixes had been made was done by the drafting session itself, and the last round of fixes "have not been read by a further reader" ([`papers/cardiac-rings/notes/QUALITY.md:262`](https://github.com/ChaseHendrick/GENChase/blob/98e7fc4/papers/cardiac-rings/notes/QUALITY.md#L262)).

**What changed.** Every must-fix finding goes to two further sessions told to refute it before it is applied. An adversarial second reading is a required quality item, and "a second reading that is only planned does not" count.

## 6. Label review honestly

**What changed.** "No text may claim an outside review that has not taken place" ([`AGENTS.md:66`](https://github.com/ChaseHendrick/GENChase/blob/98e7fc4/AGENTS.md#L66)). Every referee note opens with a line such as "An in-project reading by a separate AI agent … It is not an outside review." Skill 1.1.0 adds that the note names every AI tool that wrote, searched, checked, or reviewed (P13), and that no co-author trailer is added for an identity that was not checked (P4).

## 7. Do not bend a gate to fit a release

**What happened.** A paper was archived with a DOI while two of its seven quality items, including the adversarial second reading, were still open. The repository's own check fails at that commit. Hours later, the check was changed so that an already archived paper with open items reports them instead of failing. Separately:
- release notes said the papers were attached when the release script had stopped;
- a Zenodo archive was missing its manuscript PDF.

**What changed.** Every archive is now downloaded and checked after release. "A new `RELEASES.md` heading is not evidence" ([`docs/PUBLISHING-PAPERS.md:176`](https://github.com/ChaseHendrick/GENChase/blob/98e7fc4/docs/PUBLISHING-PAPERS.md#L176)).

## 8. The gate is a program

**What happened.** The quality bar in GENChase was a checklist. A paper was archived while two items were still open, and the checker was then changed so an archived paper reported them instead of failing (case-study P1). A quality item was ticked before the reading it certified existed (V12). In this repository, case study version 1.8 stated 151 commits and a history starting on 22 September. `git rev-list --count` at the cited commit `98e7fc4`, run on 4 October 2026, is 315, and the first commit is dated 17 September. No program failed that sentence.

**What changed.** Rule 8. [`scripts/gate.py`](../scripts/gate.py) reads [`incidents.csv`](case-study/incidents.csv) and fails if the skill or the README states a different count. It fails if the plugin manifest, the citation file, the changelog heading, the skill's release line, and the case study disagree about the version. A planted count of 79, and a planted version mismatch, must each make it fail. The downloadable zip is built from `SKILL.md` in the same run. This rule was not a control during the study window.

## The full record

The case study [*Eighty Failures: Error Modes and Controls in AI-Assisted Mathematical Research*](case-study/ai-research-failure-modes.md) ([PDF](case-study/ai-research-failure-modes.pdf)) documents all 80 incidents. The [incident dataset](case-study/incidents.csv) has them as a CSV. Each one has its class, date, commit, detecting control and whether it reached a public release.
