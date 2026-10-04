---
name: research-integrity
description: >
  Use when doing or writing up research: literature searches, prior-art or novelty
  checks, proofs, numerical verification, building test harnesses for scientific
  claims, referee-style reviews, and preparing preprints or releases. Keeps claims
  within their evidence: every claim carries how it is known, searches record what
  could not be reached, novelty is never inferred from a failed search, checks must
  be able to fail, reviews are adversarial and labelled honestly, and release gates
  are not relaxed to fit a release. Skip for casual questions and for code that
  makes no scientific or factual claim.
license: Apache-2.0
---

# Research integrity

These rules come from a documented record of 80 failures in two weeks of
AI-assisted mathematical research (nine preprints). Most failures were not
inventions. They were **claims that outran their evidence**: a search that could
not reach the journals read as proof of novelty, a check that could not fail
reported as passed, an abstract read as if it were the paper, a number taken from
a mislabeled metric. Each looked reasonable and none announced itself. The rules
below are the controls that caught them.

## 1. Label every claim with how it is known

Attach one access label to each factual claim you record or rely on:

| Label | Meaning |
|---|---|
| `read-directly` | You read the relevant passage of the source itself |
| `abstract-only` | Only the abstract or landing page was read |
| `search-summary` | Only a search engine's summary was seen; the page was not opened |
| `repository` | Taken from code, data or files you inspected |
| `reasoning` | Your own inference; no source states it |

- **A search summary is not a reading.** Summaries can attribute a generic
  statement to a specific subject, or assert that a source exists when it does
  not. Never cite from a summary as if you read the page.
- A proof step may depend only on sources labelled `read-directly`.
- When you cite, say how far you read: "read in full", "Section 3 only", "abstract".

## 2. Record what you could not search

Keep a search log. One row per search:

```
Query: "<exact query>"   Date: YYYY-MM-DD
Opened: <sources actually read>
Blocked: <sources that failed to load, were paywalled, or were refused by the network>
Conclusion: <one sentence, stated within what was opened>
```

- **"I did not find it" means nothing if the likeliest source never loaded.**
  If a fetch fails, record it under Blocked. Never fold it into "no results".
- If you did not search, do not write a row. Never invent a search.
- Check the log before calling a paper unread or re-running a search.

## 3. Never infer novelty from a search

- Do not claim a result is new, first, or original because a search found nothing,
  or because a numerical check succeeded.
- Before deriving anything, search for the closed form and for the extremum
  itself. If a paper already states either, stop and credit it.
- State novelty only within the search's reach: "Searches of X and Y found no
  earlier statement; Z and W could not be opened."
- Give results descriptive titles. Never attach a personal name to a result, and
  never rename a published result.
- Do not count one result's special cases as several contributions.

## 4. Every check must be able to fail

A check that cannot miss is not a check. For each verification:

- **Give it a failure control**: a deliberately wrong input or code change that
  the check must reject, for the reason it is meant to test.
- **Mutate the code under test** (flip a sign, change a constant, drop a term)
  and confirm the check catches it. If most mutations pass, the check has no power.
- **Match on exact success output.** A grep that matches both the success and
  the failure line, or a status printed regardless of the value, is not a check.
- **Bind results to the source that produced them**, so that a proof step
  cannot consume results computed from an older version.
- Do not report "verified" for anything no program actually checked. Map every
  verification claim in a paper to a committed, runnable check.
- Never round a measurement toward theory, and never hide a disagreement.
- Asserts stripped by optimization flags (`python -O`) are not gates. Use
  explicit failures.

## 5. Review adversarially, then doubt the reviewer

- For each proof or computational claim, start a **separate session** briefed only
  with the paper and its programs, and told to find errors. The drafting session
  does not review its own work, and does not check its own fixes.
- Where possible, add an **independent reimplementation** that never reads the
  original code.
- Before applying a finding, give it to **one or two further sessions told to
  refute it**. Record findings that do not survive.
- Two checkers that disagree are information. Two that agree are not proof.
- After fixes, have a further reader confirm them. Record that the reading
  happened, not that it is planned.

## 6. Label review honestly

- An AI reading is **not** peer review and not an outside review. Every review
  note says so in its first lines, for example: "An in-project reading by a
  separate AI session. It is not an outside review."
- Never write that work was independently or externally reviewed unless a person
  outside the project reviewed it.
- Disclose every AI tool used, not only the main one.

## 7. Do not bend a gate to fit a release

- Before a preprint, release or DOI, every quality item must be **done and
  recorded**, not planned.
- If a gate fails, the release waits. Do not change the gate so the release
  passes. If a gate must change, record the change, the reason, and which release
  it unblocked.
- After release, download the archive and confirm it contains what the notes
  say it contains. A changelog heading is not evidence.

## Quality checklist (before any preprint or release)

- [ ] **Proofs complete.** No step is "left to the reader" or planned.
- [ ] **Computation rigorous.** Exact or interval arithmetic where a proof
      depends on it, in a committed program that stops on a failed check and has
      negative controls.
- [ ] **Every claim labelled**: proved, computed, cited, or conjectured.
- [ ] **Sources read.** Every source a proof depends on is `read-directly`;
      background citations say how far they were read.
- [ ] **Prior work searched and logged**, with blocked sources listed, and every
      novelty statement within the search's reach.
- [ ] **Adversarial second reading done**, every must-fix fixed, and the fixes read
      by someone other than the drafting session.
- [ ] **Reproducible** from a fresh checkout with pinned versions.

## Phrases to avoid, and what to write instead

| Avoid | Write |
|---|---|
| "This is the first ..." | "Searches of X and Y found no earlier statement; Z could not be opened." |
| "Verified" (with no program) | "Checked by `script.py`, which fails on <control>." |
| "Independently reviewed" | "Read by a separate AI session in this project; not an outside review." |
| "No prior work exists" | "No prior work was found in the sources that loaded (listed below)." |
| "Exact" (for an enclosure) | "Enclosed in [a, b] by interval arithmetic." |
| "Does not replicate" (weak test) | State the test, its power, and the result. |
