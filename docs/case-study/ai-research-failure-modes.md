# Eighty Failures: Error Modes and Controls in AI-Assisted Mathematical Research

**A case study of one month in the GENChase research workspace**

Chase Hendrick · Hendrick Research · ORCID [0009-0002-9754-6087](https://orcid.org/0009-0002-9754-6087)

Version 1.2 · 4 October 2026 · Case study, not peer reviewed

---

## Abstract

AI coding assistants are now used to search literature, write proofs, build verification programs and prepare preprints. Their failure modes in that setting are rarely documented with primary evidence. This study examines GENChase, a public research workspace in which AI assistants produced nine mathematical preprints, a simulation studio and a supporting research ledger between 19 September and 3 October 2026. Most of the work was done in Claude Code, with smaller contributions from Grok and from OpenAI's Codex and ChatGPT. Every incident was reconstructed from the repository's own records at commit `98e7fc4`, with a file and line or a commit hash for each: 260 quotations were checked mechanically against the source.

We identify **80 incidents in five classes**:

- unsupported novelty or priority (9);
- literature misuse (18);
- wrong numbers or overstated results (19);
- verification that could not fail or did not exist (20);
- process and tooling failures (14).

Twenty-two incidents reached a public artifact, and eight more may have. Fifty were caught before release or never left internal notes.

In-project AI review caught more incidents than any other control. Referee readings by separate agent sessions found 28, and adversarial verification found 11, for 39 of 80 (49%). The owner caught 4 directly, and requested the audit that caught the largest one. A second, independent model, blind to our labels, agreed with 74 of the 80 class assignments (Cohen's κ = 0.91). The most consequential single failure was a literature search that could not open most journals, read as evidence of novelty. The result was a public claim of five "first public" identities, of which, on audit, zero were new.

The errors that reached the public cluster before the controls were in place. After a seven-item quality bar and adversarial second readings were introduced (25–26 September), one recorded manuscript error reached a published paper: a model description in the cardiac-rings 1.1.0 preprint, found by a formula audit the day after release. The other public failures after that date are release and packaging failures, plus one quality gate that was bypassed and then weakened.

We describe the controls that emerged, report where they failed, and give recommendations for researchers and for the builders of AI research tools.

---

## 1. Introduction

The common worry about AI research assistants is fabrication: invented citations and hallucinated results. This case shows a subtler and more frequent problem. Most failures here were not inventions from nothing. They were **claims that outran their evidence**: a negative search treated as a positive finding of novelty, a check that could not fail reported as a passed check, an abstract read as if it were the paper, a number taken from a mislabeled metric. Each looks reasonable, and none announces itself.

GENChase offers an unusual vantage point because its assistants were instructed to record their own corrections. The research ledger (`RESEARCH.md`, 2,180 lines) logs every search, every blocked source and every retraction. Quality records accompany every paper. Referee notes record in-project reviews. Because these records were kept as the work happened, the failure history can be reconstructed from evidence rather than from memory.

This study asks three questions:

1. **What kinds of errors** does AI-assisted mathematical research produce, and how often?
2. **Which controls caught them**, and which errors escaped every control?
3. **What should change**, in research practice and in the tools?

### 1.1 Related work

Studies of AI in research have so far looked at two things: **the outputs of autonomous research systems**, and **specific error types measured in isolation**.

**Autonomous research systems.** Lu et al. (2024) introduced *The AI Scientist*, which generates ideas, runs experiments and writes papers end to end. An independent evaluation by Beel, Kan and Baumgart (2025) found that its literature reviews "produced poor novelty assessments, often misclassifying established concepts … as novel". They also found that 42% of its experiments failed from coding errors, and that some papers contained hallucinated numerical results. Si, Yang and Hashimoto (2024) had over 100 NLP researchers blind-review research ideas, and found LLM-generated ideas judged more novel than expert ideas (p < 0.05) but slightly less feasible. They also report failures of LLM self-evaluation. Both lines of work evaluate *outputs*. Neither follows a human-directed project over time to record what went wrong and what caught it.

**Fabricated citations.** Walters and Wilder (2023) examined 636 citations in 84 ChatGPT-generated papers. They found that 55% of GPT-3.5 citations and 18% of GPT-4 citations were fabricated, and that substantive errors remained in 43% and 24% of the real ones. That work measures one failure type in generated text. The present record contains almost no wholly fabricated citations. Its literature failures are subtler: unread sources, misstated theorems, and search summaries taken for sources.

**Weak tests.** In software engineering, LLM-generated test suites are known to look stronger than they are. Wang, Xu, Briand and Liu (2025) report test suites with 100% code coverage but only a 4% mutation score, and argue that mutation score, not coverage, measures a suite's ability to find faults. Our Class V is the research-computation counterpart: a verification harness in which 13 of 16 mutations passed every check.

**Contribution.** We are not aware of a study that documents every recorded failure of a real, human-directed, AI-assisted mathematical research project, links each one to primary evidence, and measures which controls caught it. This case study aims to provide one. Its taxonomy is checked by an independent second coder, and the full dataset is published.

## 2. Setting

**The workspace.** GENChase ([github.com/ChaseHendrick/GENChase](https://github.com/ChaseHendrick/GENChase)) is a single-author research and simulation workspace. Over the study window it produced:

- nine preprints with 55 Zenodo version DOIs, covering point-vortex collapse, neural-field and Hodgkin–Huxley traveling waves, double-pendulum dynamics, random-matrix spectra and rotating waves in rings of cardiac cells;
- a draft software paper;
- a browser-based studio of scientific simulations.

**The assistants.** Most work was done in Claude Code sessions, including cloud sessions with a sandboxed network. Grok worked on the repository from about 27 to 29 September and on the cardiac study on 1 October. OpenAI's Codex ran part of the cardiac computations around 30 September and 2 October, and ChatGPT was used in small amounts. 58 of the 151 commits on `main` carry a `Claude-Session:` trailer, and seven carry `Co-authored-by: Claude`. A trailer shows that a commit was made from a Claude Code session. It does not show which model wrote a given sentence, and a missing trailer does not mean another assistant did the work. **This study therefore does not attribute individual errors to individual models.**

**The owner's role.** The owner set direction, made editorial decisions, fetched papers the sandbox could not reach, and approved releases. Several controls in this study began as owner instructions.

## 3. Method

**Source.** The repository at commit `98e7fc4` (3 October 2026), read without modification. The git history starts at a root commit dated 22 September. Events from 19 to 21 September are dated only by the notes that record them.

**Unit of analysis.** An *incident* is a recorded instance in which a claim, number, check, citation or process step was wrong or unsupported, and the repository records it being found. Where one report bundles several related findings, they form a single incident.

**Coding.** Each incident was coded for:

- **class** (Section 4);
- **date and commit**;
- **evidence**: a verbatim quote with its file and line;
- **detecting control**: owner (OWN), literature or novelty audit (AUD), separate-agent referee reading (REF), adversarial verification workflow (AVW), independent re-derivation (IND), full reading of a source (REV), re-run or download check (RUN), the working session itself (SELF), or continuous integration (CI);
- **reach**: public, uncertain, or caught/internal.

"Public" means the error was present in a tagged GitHub release, a companion or Zenodo release, or the repository while it was public. Where this could not be established, the incident is marked *uncertain*.

**Verification of the evidence.** 255 file-and-line quotations were checked mechanically: the quoted text must occur on exactly that line in the repository. Three claims were checked by re-execution:

- the v0.5.0 tag still contains the wrong agreement figure;
- the v0.6.2 tag still contains the factor-2 eigenvalues;
- the paper quality check fails at the hh-pulse release commit.

**Coder.** The evidence base was compiled by an AI agent (Claude, in Claude Code) under the owner's direction. The incidents are drawn from the repository's own records, which were themselves largely written by AI sessions. Section 8 discusses what this implies.

**Reliability of the classification.** To test whether the five classes can be applied consistently, a second coder classified all 80 incidents independently. The coder was a different model (Claude Sonnet) in a separate session. It saw only each incident's short name and evidence quote, under shuffled identifiers, plus the written codebook, and never saw our labels. It agreed with our class on **74 of 80 incidents (92.5%)**. Cohen's κ is **0.91**, against 21% agreement expected by chance. All 53 incidents it rated high-confidence matched. The six disagreements all fall on the borders between classes W, V and P. For example, a status line that printed "Poisson solved" unconditionally can be read as a vacuous check (V) or as a misleading number (W). The second coder's class for every incident is included in the dataset. Agreement was measured for class only; reach and detecting control were not independently re-coded.

**Rates.** Over 15 days and 151 commits, the record contains 80 incidents: about 5.3 per day, one per 1.9 commits, and 8.9 per preprint. These are rates of recorded and corrected failures, not of all failures.

## 4. A taxonomy of failures

Table 1 gives the five classes and their reach.

**Table 1. Incidents by class and reach.**

| Class | Incidents | Reached public | Uncertain | Caught / internal |
|---|---:|---:|---:|---:|
| N. Unsupported novelty or priority | 9 | 4 | 0 | 5 |
| L. Literature misuse | 18 | 2 | 3 | 13 |
| W. Wrong numbers, overstated results | 19 | 6 | 3 | 10 |
| V. Verification that could not fail or did not exist | 20 | 5 | 1 | 14 |
| P. Process and tooling | 14 | 5 | 1 | 8 |
| **Total** | **80** | **22** | **8** | **50** |

### 4.1 Class N: unsupported novelty and priority

The most serious failure in the record, and the origin of most later controls.

**Case N1–N2: five "first public" identities.** Early in the project, the workspace presented five closed-form results on point-vortex collapse as new and publicly first. The supporting literature search could not open most journals: the ledger notes "Blocked: … Most journals." It concluded that the results "were not in those sources". At the owner's request, the work was reopened "to verify all five against the internet". A full reading of Gröbli (1877) then reproduced the first candidate from his original equations. Kimura (1987) was later found to give the governing ratio explicitly. The audit's conclusion, now the first line of the ledger:

> "Confirmed novel findings among the five candidates: 0." (`RESEARCH.md:11`)

The audit document states that it "supersedes the repository's earlier unqualified claims of being the first public source of these formulas" (`identities/NOVELTY-AUDIT.md:6`). A personal name given to one classical result was also retired (N3). The pattern is the central lesson of this study: **the absence of evidence was reported as evidence of absence, and novelty was asserted from a search that could not have found the prior work.**

Later novelty overclaims were caught by referee readings before release:

- the rank-window note's central point was anticipated and uncited (N6);
- the hh-dynamics novelty statement overreached (N7);
- the double-pendulum and hh-pulse priority statements rested on papers that were read only through search snippets or not at all (N8, N9).

In each case the statement was narrowed to what the search had actually reached.

### 4.2 Class L: literature misuse

Eighteen incidents involve how sources were found, read and cited. Three mechanisms recur.

**Blocked access read as absence (L1, L2).** The cloud sandbox's network policy blocked arXiv, Springer, Crossref, OpenAlex, Semantic Scholar, Wikipedia and most journal sites. The ledger records sessions that searched sites which never loaded "and then write 'I did not find it' as if those sites had loaded" (`RESEARCH.md:306`).

**Search summaries treated as sources (L3, L4).** The web search tool returns a model-written summary of results. Twice the summary asserted something no source supported:

- it claimed a May 2024 preprint of a paper for which no preprint could be found (`RESEARCH.md:239`);
- it attributed a publisher's generic preprint policy to a specific journal. A verifying agent identified this as "the search model's inference, not text from any RCD or Pleiades page" (`docs/wip/research-2026-09-24-unverified.md:395`).

**Citing what was not read (L6–L17).** These include:

- a claim resting on a paper that "was not read" (L6);
- a source's printed value said to match for two examples when it matched one (L12);
- a theorem misstated as unconditional when it assumes five conditions (L14, L15);
- misrepresentations of the Smale–Birkhoff theorem (L16);
- wrong titles, pages and credits (L10, L13, L17);
- in the cardiac-rings manuscript, a reading cited that did not exist (L18).

Referee readings or full source readings caught all but two of these before release. The two exceptions concern a superseded identities note that sat in the public repository.

### 4.3 Class W: wrong numbers and overstated results

**Case W18: a model described wrongly in a released paper.** The cardiac-rings 1.1.0 preprint described its cell model in two ways that did not match the equations actually solved. It applied a capacitance ratio to calcium terms that do not carry it, and it described holding intracellular potassium fixed as a restriction of the full model when it in fact changes the equations. A formula audit on 3 October found both, the day after release. The source was corrected, and the note records that "the released 1.1.0 PDF and immutable tag remain untouched" (`papers/cardiac-rings/notes/model-correction-rebuild-2026-10-03.md:4`). The theorems themselves concern the stated model and were not affected. A second cardiac-rings reading also found "two wrong numbers in statements" before the first release (W19).

**Case W1: the mislabeled metric.** A verification table reported agreement of 6 × 10⁻²⁵. The figure "came from a mislabeled metric in `verify_general_mu.py`; the true figure is 4.5 × 10⁻²¹", and 13 values had been checked, not 12 (`RESEARCH.md:155`). The wrong figure shipped in release v0.5.0, whose tag still contains it. It was corrected the same day, and a rule followed: every verification claim in a paper must map to a committed check.

Other numeric errors that reached a release:

- Hessian eigenvalues printed for 2P instead of P (W5, v0.6.2);
- a configuration announced as a collapse that in fact expands; its mirror image collapses (W6, v0.6.2 notes);
- two studio defects: one compared plates against an infinite-size limit, so correct plates read as wrong (W14), and a silently overwritten parameter meant every plate of one model ran at v = 2 whatever the slider said (W15).

The overstated-result incidents were caught by referee readings before release:

- theorem domains claimed larger than proved (W8);
- "exact" values that rested only on numerical enclosures (W11);
- a "no replication" verdict that overstated a weak held-out test (W12);
- abstract wording such as "rarely or not at all" without uncertainty (W13).

### 4.4 Class V: verification that could not fail, or did not exist

This is the largest class and the hardest to see. A check that cannot fail looks exactly like a check that passed.

**Case V1–V3: the nf-pulse harness.** An adversarial verification workflow ran four independent checkers in parallel on 26 September: mathematics, code audit with mutation testing, an independent reimplementation that never read the original code, and prior-article search. It found:

- a check whose grep pattern "matches the line printed on success and on failure" (`papers/nf-pulse/review/MATH.md:295`);
- a Jacobian test where "an error of 4.7e-2 still prints OK" (`papers/nf-pulse/review/VERIFY.md:72`);
- a configuration under which the harness "prints all 15 OK, while the proof log records `cone_pd False`" (`VERIFY.md:59`);
- that "13 of the 16 integrator mutations still pass all 15 checks" (`VERIFY.md:63`).

The code checker and the mathematics checker found the first defect independently.

**Claimed but nonexistent verification (V4–V7, V9, V12–V14).** Recorded instances include:

- "The claimed consistency check of the manifold recursion did not exist" (`papers/nf-pulse/ext/faye-model/REPORT.md:289`);
- a README describing written proofs that did not yet exist (V5);
- a hypothesis the paper says a program verifies, which "is not checked by any program" (`papers/double-pendulum/notes/review-1.md:64`);
- a quality item ticked before the readings it certified had been recorded, so that merging "would have synced the unread additions to the public companion" (V12).

**Tautologies (V8, V10, V11, V15–V17).** These include:

- a negative control that "cannot fail to fail" (V8);
- a symbolic check that compared a polynomial with itself reordered (V11);
- simulation status lines printing "Poisson solved" unconditionally and "mass conserved" with no measurement (V15);
- README agreement values of "1 ; 1" that were later "removed rather than transformed into invented zero-error measurements" (V16).

**Stale evidence (V20).** During the cardiac-rings 1.1.0 work, a review found that "the Hopf bridge could consume older point-proof successes without current-source binding" (`docs/HANDOFF-2026-10-02-cardiac-rings-1.1.0-codex.md:65`): a proof step could have been satisfied by results computed from an earlier version of the source. The program was changed to bind each result to the exact source it came from.

The studio-side incidents (V15–V17) reached public releases before an uncertainty gate was added on 24 September. All the paper-side incidents in this class were caught before release.

### 4.5 Class P: process and tooling

**Case P1: a bypassed quality gate.** On 28 September the hh-pulse paper was marked ready while two of its seven quality items, including the adversarial second reading, were still open. The repository's own check fails at that commit; re-running it today reports "the quality bar is not met (open: item 6, 7)". The preprint was archived with a Zenodo DOI anyway. Five hours later, a change to the checking tool made an already archived paper with open items report them rather than fail. The open items were closed the next day and the owner chose not to withdraw. This is the clearest case in the record of a **control being weakened to accommodate the failure it caught**, and the record does not show who triggered the release.

Other process incidents:

- release notes that said papers were attached when the release script had stopped (P2);
- a Zenodo archive missing its manuscript PDF (P3);
- invented co-author trailers on `main` after a rule against them existed (P4);
- an arXiv endorsement asserted as unnecessary when it was required (P9);
- research verification stopped "to save usage", leaving 179 of 236 gathered claims never verified (P6);
- work that existed only in an ephemeral cloud container (P7);
- for cardiac-rings, the check that a referee's must-fix findings had been fixed was made by the drafting session itself, and the fixes from the third reading "have not been read by a further reader" (P14, `papers/cardiac-rings/notes/QUALITY.md:256`, `:262`).

## 5. The controls

### 5.1 What caught what

**Table 2. Detecting control, counted across the 80 incidents.** An incident may have more than one detector.

| Control | Incidents detected |
|---|---:|
| Separate-agent referee reading (REF) | 28 |
| Adversarial verification workflow (AVW) | 11 |
| The working session itself (SELF) | 8 |
| Full reading of a source (REV) | 6 |
| Literature or novelty audit (AUD) | 6 |
| Owner (OWN) | 4 |
| Re-run or download check (RUN) | 2 |
| Independent re-derivation (IND) | 2 |
| CI | 2 |
| Other (cross-assistant review; this study) | 2 |
| Not stated, not recorded or not detected | 11 |

**In-project AI review, from referee readings and adversarial workflows, detected 39 of 80 incidents (49%).** Every referee note opens with a disclaimer such as: "An in-project reading by a separate AI agent (a headless Claude session started for it) … It is not an outside review." Most referee notes in the repository carry one.

These readings were consistently productive:

- six readings of the hh-dynamics paper found 18 surviving findings, five of them must-fix, in the first three alone;
- four readings of minimal-winding 2.2.0 found ten confirmed serious findings.

![Figure 2. (A) The 80 incidents by class, split by whether the error reached a public artifact. (B) Detections by control; an incident can have more than one detector. In-project AI review, from separate referee sessions and adversarial verification workflows, accounts for 39 of the 80 incidents.](fig-classes.svg)

### 5.2 The protocol as it stands

By 30 September the workspace had converged on the following controls. Each traces to incidents in Section 4.

**Provenance labels for every claim.** A gathered claim carries an access label: `read-directly`, `search-summary`, `repository`, `reasoning` or `legal-text`. "Do not take a search summary as a reading" (`RESEARCH.md:140`).

**A written record of search limits.** A standing table lists what the sessions could and could not open. "A negative result is weakest of all where the likeliest home for the thing is a site in the right-hand column" (`RESEARCH.md:324`). Every search is logged with its query, what was opened, what was blocked and its conclusion: "If you are an agent and you did not search, do not invent a row" (`RESEARCH.md:865`).

**A bounded meaning for "new".** "Claim originality from a numerical check or unsuccessful literature search" is forbidden (`RESEARCH.md:302`). Results take descriptive titles, never personal names, and classical sources are credited (`AGENTS.md:19`).

**Checks that can fail.** "A check that cannot miss is not a check" (`AGENTS.md:161`). Every numerical record needs a `failureControl`, defined as "a deliberate wrong result or implementation change that the test detects". Comparisons without a stated basis are refused by code, and a lint fails any value printed against a reference by hand.

**A seven-item quality bar, enforced by a tool.** The items are: complete proofs; rigorous computation in exact or interval arithmetic with negative controls; every claim labelled; every source a proof depends on read in full; a logged prior-article review; an adversarial second reading by a reviewer "told to find errors, briefed only with the paper and its programs"; and reproducibility. "A second reading that is only planned does not" count (`docs/PUBLISHING-PAPERS.md:65`).

**Skeptic agents.** Before a referee's finding is applied, two further agents are told to refute it. Some findings did not survive. On rank-window, two of five must-fix findings were dropped this way.

**Honest review labels.** "No text may claim an outside review that has not taken place" (`AGENTS.md:66`).

**Release verification.** Every Zenodo archive is downloaded and checked for its manuscript PDF. "A new `RELEASES.md` heading is not evidence" (`docs/PUBLISHING-PAPERS.md:176`).

### 5.3 Timing

![Figure 1. Incidents by the date they were recorded, colored by whether the error reached a public artifact. Dashed lines mark the introduction of four controls (23–26 September). Most incidents are dated by when they were recorded, often the day they were found, so errors made earlier and corrected later appear on the later date. Three public incidents dated 27 September are of this kind. One undated incident is omitted.](fig-timeline.svg)


The public incidents cluster early. The novelty claims (N1–N4), the wrong numbers in v0.5.0 and v0.6.2 (W1, W5, W6), and the studio's vacuous checks (V15–V17) all predate the key controls:

- the uncertainty gate (24 September);
- the seven-item quality bar (25 September);
- the adversarial verification workflow (26 September).

After those dates, almost every recorded manuscript-content error was caught before the paper's release. There are two exceptions. V14, a fix list that called two items done that were not, may have shipped. W18, the cardiac-rings model description, did ship, and was found by an audit the day after release. The other public failures after 25 September were in releasing and packaging (P1–P3, P14) or in the studio (W14), not in the mathematics. The sample is small and the window short, so this is an observation, not a measured effect.

## 6. Discussion

**The dominant failure is overreach, not invention.** Of the 80 incidents, few involve material invented from nothing. The search-summary artifacts (L3, L4) and the invented co-author trailers (P4) come closest. Most are claims stated more strongly than the evidence allowed. The failure is in calibration, so the remedy is to make evidence strength visible at every claim, not just to check facts.

**Blocked access is a correctness problem.** A literature search that cannot reach the literature does not produce a weak result; it produces a misleading one, because it is read as negative. The single most damaging incident in this study (N1–N2) follows directly from a network policy. Two things would have prevented it: tooling that reported which sources were unreachable, and conclusions that stated their reach.

**These failures echo known patterns, in a new setting.** The misclassification of known results as novel (Class N) is the failure Beel et al. (2025) found in an autonomous system, here appearing in a human-directed project with a human in the loop. The verification harness that passed 13 of 16 mutations parallels the gap between coverage and mutation score in LLM-written software tests (Wang et al., 2025). The near absence of outright fabricated citations, compared with the rates Walters and Wilder (2023) measured, suggests the frontier has moved from inventing sources to misreading them.

**Verification needs its own verification.** Twenty incidents concern checks that could not fail or did not exist, or that could be satisfied by stale results. An AI assistant asked to build a verification harness will build one that passes, and a passing harness is not evidence. Mutation testing, negative controls with a specific expected failure reason, and independent reimplementations that never read the original code were the techniques that found these defects.

**In-project AI review works, within limits.** Separate agent sessions told to find errors were the most productive control in the record. They are not outside review. They share the training, blind spots and literature access of the sessions they check. When two checkers verified the same 26 claims, they agreed on only 12, and ten claims were "confirmed" by one and "unverifiable" by the other. Disagreement between AI checkers is information; agreement is not proof.

**Controls erode under release pressure.** The hh-pulse case (P1) shows a gate that worked, a release that went ahead regardless, and a tool change hours later that stopped the gate from failing. Controls that can be edited by the same process they constrain need a record of every relaxation.

## 7. Recommendations

### 7.1 For researchers using AI assistants

1. **Label every claim with how it is known**: read in full, abstract only, search summary, or reasoning. Never let a search summary stand in for a reading.
2. **Write down what could not be searched**, and state novelty only within that reach. Treat "I did not find it" as worthless when the likeliest source was unreachable.
3. **Give every check a failure control** and test it with mutations. A check that has never failed has not been tested.
4. **Use separate adversarial sessions** to review proofs and code, then use skeptic sessions to test the reviewers' findings. Record disagreements.
5. **Label in-project review honestly.** An AI reading is not peer review.
6. **Make release gates tamper-evident.** Record every relaxation of a gate with its reason and the release it unblocked.

### 7.2 For builders of AI research tools

These follow from the incidents and are framed as requests. Several are filed on the Claude Code issue tracker.

1. **Provenance in search results.** Web-search summaries should separate what a page says from what the summarizer infers, and every assertion of existence should carry a URL. Filed as [anthropics/claude-code#99385](https://github.com/anthropics/claude-code/issues/99385).
2. **Report unreachable sources as a result.** When a fetch is blocked by policy, the tool output should say so in a form the model cannot mistake for an empty result.
3. **Research network presets.** Sandboxed cloud sessions should offer a scholarly allowlist (arXiv, DOI resolvers, major publishers, Crossref, OpenAlex, Semantic Scholar) as a one-click option.
4. **Visible and reservable search budgets.** The session's search budget should be visible, and a verification stage should be able to reserve part of it. See [anthropics/claude-code#91723](https://github.com/anthropics/claude-code/issues/91723).
5. **First-class adversarial verification.** A built-in verify step should run independent checkers, mutation tests and negative controls, and report what it could not check as unverified rather than refuted.
6. **Respect project identity and policy.** Harness hooks should not instruct the agent against a repository's written rules, for example rewriting commit authorship. See [anthropics/claude-code#69201](https://github.com/anthropics/claude-code/issues/69201).
7. **Durable work in ephemeral sandboxes.** Background results in cloud sessions should persist, or the user should be warned before a container is reclaimed.

## 8. Limitations

- **Single case, short window.** One workspace, one owner and twelve days of git history (22 September to 3 October). The incidence of each class will differ elsewhere.
- **Recorded incidents only.** The study sees only errors the workspace recorded finding. Undetected errors are by definition absent, so the counts are a lower bound, and the share caught by each control is a share of what was caught at all.
- **The record was written largely by AI sessions**, and the evidence base was compiled by an AI agent. The quotations were checked mechanically against the source, but the selection and coding of incidents was not independently replicated.
- **Attribution.** Commit trailers show which tool session committed work, not which model wrote any sentence. No incident here should be read as a finding about a specific model.
- **Pre-history.** Events before 22 September are dated only by the notes that record them.
- **Coding judgment.** An independent second coder agreed on the class of 74 of 80 incidents (κ = 0.91), but that coder was also an AI model, and the detecting control and reach of each incident were coded only once. Several are marked uncertain in the appendix.
- **Dates.** Most incidents are dated by when they were recorded rather than when the error was made, which shifts some early errors to later dates (Figure 1).

## 9. Conclusion

Over two weeks of recorded history, AI-assisted research in GENChase produced 80 recorded failures. The most important was a novelty claim built on a search that could not reach the literature. The most numerous were checks that could not fail. The errors that reached the public came mostly before the controls existed. After them, the mathematics was almost always caught before release; what still escaped was mostly the release process itself, and once, a model description that only a later audit caught. The controls that worked were mostly made of more AI: separate sessions told to find errors, and others told to doubt the finders. They worked because the work was required to show its evidence, its reach and its limits at every step.

---

## Data availability

All evidence is in the public repository [ChaseHendrick/GENChase](https://github.com/ChaseHendrick/GENChase). The incident dataset (`incidents.csv`: 80 rows with class, the second coder's class, date, verbatim evidence, detecting control and reach) is published with this paper. File and line references in this paper refer to commit `98e7fc4` (3 October 2026); a reference `path:N` can be opened as `https://github.com/ChaseHendrick/GENChase/blob/98e7fc4/path#LN`. The controls described in Section 5.2 are packaged as a Claude skill at [ChaseHendrick/Research-Integrity](https://github.com/ChaseHendrick/Research-Integrity).

## Use of AI

This case study was drafted with Claude (Opus 5.5) in Claude Code. An AI agent compiled the evidence base from the repository under the author's direction, and the quotations were checked mechanically against the source. The second coding was done by Claude Sonnet in a separate session. The related-work sources were read at the level of their published abstracts, which is a limit on how they are characterized here. The author is responsible for the content.

## Ethics

This study involves no human participants. It reports the author's own project, including errors that reached public releases. Incidents are described by what the record shows, without attributing them to individual AI models, because the record cannot support that attribution.

## Conflicts of interest

None. The author is the owner of the workspace studied and of the Research-Integrity skill.

## References

1. Beel, J., Kan, M.-Y., & Baumgart, M. (2025). Evaluating Sakana's AI Scientist: Bold claims, mixed results, and a promising future? arXiv:2502.14297.
1. Gröbli, W. (1877). *Specielle Probleme über die Bewegung geradliniger paralleler Wirbelfäden*. Inaugural dissertation, Georg-August-Universität Göttingen; printed by Zürcher und Furrer, Zürich. English translation: arXiv:2404.01305.
1. Kimura, Y. (1987). Similarity solution of two-dimensional point vortices. *Journal of the Physical Society of Japan*, 56, 2024–2030. doi:[10.1143/JPSJ.56.2024](https://doi.org/10.1143/JPSJ.56.2024).
1. Lu, C., Lu, C., Lange, R. T., Foerster, J., Clune, J., & Ha, D. (2024). The AI Scientist: Towards fully automated open-ended scientific discovery. arXiv:2408.06292.
1. Si, C., Yang, D., & Hashimoto, T. (2024). Can LLMs generate novel research ideas? A large-scale human study with 100+ NLP researchers. arXiv:2409.04109.
1. Walters, W. H., & Wilder, E. I. (2023). Fabrication and errors in the bibliographic citations generated by ChatGPT. *Scientific Reports*, 13, 14045. doi:[10.1038/s41598-023-41032-5](https://doi.org/10.1038/s41598-023-41032-5).
1. Wang, G., Xu, Q., Briand, L., & Liu, K. (2025). Mutation-guided unit test generation with a large language model. arXiv:2506.02954.
1. GENChase repository, commit `98e7fc4`, files cited in text: `RESEARCH.md`, `AGENTS.md`, `identities/NOVELTY-AUDIT.md`, `docs/PUBLISHING-PAPERS.md`, `papers/*/notes/QUALITY.md`, `papers/*/notes/referee-*.md`, `papers/nf-pulse/review/VERIFY.md`, `papers/nf-pulse/review/MATH.md`, `docs/wip/research-2026-09-24-unverified.md`.

---

## Appendix A. Incident index

Reach: **P** reached public · **?** uncertain · **C** caught before release or internal. Detector codes as in Section 3.

| ID | Incident | Detected by | Reach |
|---|---|---|---|
| N1 | Three-vortex "uniqueness" concluded from a search that could not open most journals; result is in Gröbli 1877 and Kimura 1987 | AUD, REV | P |
| N2 | Five identities presented as first-public; audit found zero novel | AUD | P |
| N3 | Personal name given to a classical result | OWN | P |
| N4 | Priority wording left in a fingerprinted statements file | REF | P |
| N5 | Published equations given private names in draft | not stated | C |
| N6 | Rank-window central point anticipated and uncited | REF | C |
| N7 | hh-dynamics novelty statement overreached | REF | C |
| N8 | Double-pendulum novelty rested on search snippets | REF | C |
| N9 | hh-pulse priority rested on two unread papers | REF | C |
| L1 | "I did not find it" on sites that never loaded | SELF | ? |
| L2 | Network policy blocked most scholarly hosts; conclusions from abstracts | SELF | C |
| L3 | Search summary asserted a preprint that could not be found | SELF | C |
| L4 | Search summary attributed a generic publisher policy to a specific journal | AVW | C |
| L5 | Truncated quotes and a mixed-up citation in gathered research | AVW | C |
| L6 | Claim rested on an unread paper | REV | ? |
| L7 | Prior work under-credited | REV | C |
| L8 | Paper already read was called unread | SELF | C |
| L9 | Wording and credit errors in paper 1 | REF | ? |
| L10 | Credits misattributed in the retired identities note | REF | P |
| L11 | Source result asserted while assuming its hypothesis | REV | P |
| L12 | Source value said to match for two examples; matched one | REF | C |
| L13 | Wrong published title and page for two sources | REV | C |
| L14 | Hastings's theorem misstated; wrong paper cited | REF | C |
| L15 | Theorem with five conditions reported as unconditional | AVW | C |
| L16 | Smale–Birkhoff theorem misrepresented; ratio misquoted | REF | C |
| L17 | A slip misattributed; theorem credited only to a secondary source | REF | C |
| L18 | Cardiac-rings manuscript cited a reading that did not exist | REF | C |
| W1 | Agreement 6 × 10⁻²⁵ from a mislabeled metric (true 4.5 × 10⁻²¹) | not stated | P |
| W2 | Witness value used a misprinted source formula | IND | ? |
| W3 | Floor reported on one branch; lower minimum missed | IND | ? |
| W4 | Six-vortex geometry wrongly declared unable to collapse | REV | ? |
| W5 | Hessian eigenvalues printed for 2P, not P | not stated | P |
| W6 | Configuration announced as a collapse actually expands | not stated | P |
| W7 | Digits rounded instead of truncated | not stated | C |
| W8 | Theorem claimed on a larger set than proved | REF | C |
| W9 | Stale check counts; "two controls" where there are three | REF | C |
| W10 | Theorem proved at 6.2999999999999998 °C; unsupported bound; numbers not in certificates | REF | C |
| W11 | "Exact" values rested only on enclosures | REF | C |
| W12 | "No replication" overstated a weak held-out test | REF | C |
| W13 | Claims beyond outputs; uncertainty missing from abstract | REF | C |
| W14 | Studio plates compared with an infinite-size limit | not stated | P |
| W15 | Studio parameter silently overwritten (every plate at v = 2) | AUD | P |
| W16 | Print audit overstated its own findings | AVW | C |
| W17 | Suggestions relayed from another assistant overstated prior work | cross-assistant review | C |
| W18 | Cardiac-rings 1.1.0 described its model wrongly (capacitance scope, potassium clamp) | AUD | P |
| W19 | Two wrong numbers in cardiac-rings theorem statements | REF | C |
| V1 | Harness check matched success and failure lines; test printed OK for any value | AVW | C |
| V2 | Harness passed a failing proof with assertions disabled | AVW | C |
| V3 | 13 of 16 integrator mutations passed all checks | AVW | C |
| V4 | Block labelled "certified" was not the block the proof uses | AVW | C |
| V5 | README described proofs that were not written | AVW | C |
| V6 | Claimed consistency check did not exist; report was an unfinished template | AVW | C |
| V7 | Parameter range never checked; negative controls failed for side reasons | AVW | C |
| V8 | Negative control that cannot fail to fail | REF | C |
| V9 | Hypothesis said to be program-verified was checked by no program | REF | C |
| V10 | Proposition check cannot fail in practice | REF | C |
| V11 | Symbolic check compared a polynomial with itself | REF | C |
| V12 | Quality item ticked before the readings it certified existed | REF | C |
| V13 | Program said to prove a quantity it only encloses | REF | C |
| V14 | Fix list called two items done that were not | REF | ? |
| V15 | Status lines printed "Poisson solved" unconditionally | AUD | P |
| V16 | README agreement values "1 ; 1" with no measurement | not stated | P |
| V17 | Tautological and preview-hidden checks shipped | not stated | P |
| V18 | Sharpness tool sampled half the pixels and called sharp plates featureless | AUD | P |
| V19 | Escape helper escaped nothing | CI | P |
| V20 | Hopf proof step could accept results from an older source version | REF | C |
| P1 | Paper archived with two quality items open; gate then weakened | RUN, OWN | P |
| P2 | Release notes said papers were attached; they were not | not stated | P |
| P3 | Zenodo archive missing its manuscript PDF | RUN | P |
| P4 | Invented co-author trailers after a rule against them | not recorded | P |
| P5 | Scratch folder landed on main despite its own instruction | not detected | ? |
| P6 | Verification stopped to save usage; 179 of 236 claims never checked | SELF | C |
| P7 | Work existing only in an ephemeral container | SELF | C |
| P8 | Audit stopped before its verification stage | SELF | C |
| P9 | arXiv endorsement asserted as unnecessary; it was required | OWN | C |
| P10 | Another process modified files during a review | REF | C |
| P11 | Checks cut off by their own time limits | CI | C |
| P12 | Handoff misstated commit authorship | this study | C |
| P13 | AI disclosure in a draft names only one assistant | OWN | C |
| P14 | Cardiac-rings fixes checked only by the drafting session; last fixes unread by a further reader | SELF | P |
