---
name: research-integrity
description: >
  Use when doing or writing up research: literature searches, prior-art or novelty
  checks, proofs, computer-assisted proofs, numerical checks, test harnesses for
  scientific claims, referee-style reviews, and preprints or releases. Keeps every
  claim inside its evidence. Each claim carries an access label and a status
  (proved, computer-assisted, cited, numerical, or conjectured). Searches record
  what did not load. Novelty is never inferred from a search or a check that
  passed. A cited theorem is applied only with its hypotheses checked. A public
  number is copied from the run that produced it. A check must be able to fail
  for the reason it tests. Reviews are adversarial and labelled as in-project.
  A release gate that already exists is not relaxed to fit a release. Beating a
  checklist with a program is optional, and only when someone asks for it.
  Skip casual questions and code that makes no scientific or factual claim.
license: Apache-2.0
---

# Research integrity

Release: 1.4.3

## Goal

Keep every claim inside its evidence. Rules 1–7 are the skill, and they are on every time it is used.

Beating a checklist is optional. Apply section 8 only when the user asks for it, or when the project already has a release gate the user chose to keep. This repository asked for it: `scripts/gate.py`. A project that did not ask is not a failed release. Do not add a program they did not ask for, and do not talk them into turning it on.

Not claimed. The skill does not open sources the assistant cannot reach. An in-project review is not peer review. Nothing here measures whether the rules reduce errors.

These rules come from a documented record of 80 failures in two weeks of
AI-assisted mathematical research (nine preprints). Most failures were not
inventions. They were **claims that outran their evidence**: a search that could
not reach the journals read as proof of novelty, a check that could not fail
reported as passed, an abstract read as if it were the paper, a number taken from
a mislabeled metric. Each looked reasonable and none announced itself. Rules 1–7
are the controls that caught them. Section 8 is optional. It is not one of those controls.

If a search, a check, or a review is cut short, say so in the first sentence.
Do not let a summary turn an unfinished step into a finished one.

When you record or rely on a claim, a search, or a check, use the three records
below. Skip them for a casual question.

```
Claim: <one sentence>
Status: proved | computer-assisted | cited | numerical | conjectured
Access: read-directly | abstract-only | search-summary | repository | reasoning
Source: <file:line, citation, or none>
Not claimed: <what this sentence does not show>
```

```
Query: "<exact query>"   Date: YYYY-MM-DD
Opened: <sources actually read>
Blocked: <sources that failed to load, were paywalled, or were refused>
Stopped: no | yes (<budget, timeout, or a connector that did not load>)
Conclusion: <one sentence, within what was opened>
```

```
Check: <program> for <claim>
Binds: <commit, file hash, or source version>
Success match: <exact pattern that failure output does not match>
Failure control: <fault> must fail because <reason>. Observed: <fail or pass>
Mutation: <caught> of <tried>
Number taken from: <named field of this run>
```

| Status | Meaning |
|---|---|
| `proved` | A written proof. No computation |
| `computer-assisted` | A written proof in which finitely many inequalities are decided by a named program, in exact or ball/interval arithmetic, that stops on a failed check |
| `cited` | A published result, used only where its hypotheses were checked |
| `numerical` | No error control. Never a step in a proof |
| `conjectured` | Stated as open |

## 1. Label every claim with how it is known

Attach one access label to each factual claim you record or rely on:

| Label | Meaning |
|---|---|
| `read-directly` | You read the relevant passage of the source itself |
| `abstract-only` | Only the abstract or landing page was read |
| `search-summary` | Only a search engine's summary was seen; the page was not opened |
| `repository` | Taken from code, data, or files you inspected |
| `reasoning` | Your own inference; no source states it |

- **A search summary is not a reading.** Summaries can attribute a generic
  statement to a specific subject, or assert that a source exists when it does
  not. Never cite from a summary as if you read the page.
- A proof step may depend only on `read-directly` sources, and on `repository`
  results bound to the source version the proof names. It may not depend on
  `abstract-only`, `search-summary`, or `reasoning`.
- Attach a status as well as an access label. `computer-assisted` is not
  `proved`. `numerical` is neither. An enclosure is not an exact value.
- When you cite, say how far you read: "read in full", "Section 3 only", "abstract".
- **Check the hypotheses before you apply a theorem.** Name the ones you checked
  against this instance and the ones you did not. An unchecked hypothesis is not
  a proof step. Do not drop conditions and call the result unconditional.
- Copy quotations, titles, years, and pages from the source. Do not reconstruct them.
- Do not cite a reading, a file, or a check that is not in the tree.
- Date a public error by the artifact that contains it. If the note that records it was written on another day, give both dates. Do not place the error before a control when the artifact is dated after the control.

## 2. Record what you could not search

- **"I did not find it" means nothing if the likeliest source never loaded.**
  If a fetch fails, record it under Blocked. Never fold it into "no results".
- A tool, connector, or index that did not load is Blocked. A session that
  started before its connectors connected did not search.
- If the search was cut off, write `Stopped: yes`. That row is not evidence of absence.
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
- When a priority sentence is withdrawn, delete it from every file that can ship:
  the manuscript, the statements file, the README, the changelog, and any
  fingerprint. A correction in one file does not clear the others.
- End a contribution sentence with what it does not claim, how far each source it depends on was read, and which indexes did not open.

## 4. Every check must be able to fail

A check that cannot miss is not a check. For each verification:

- **Give it a failure control**: a deliberately wrong input or code change that
  the check must reject, for the reason it is meant to test. It must pass when
  that fault is absent. A control that cannot fail to fail, or that fails for a
  side reason, is not a control.
- **Mutate the code under test** (flip a sign, change a constant, drop a term)
  and confirm the check catches it. If most mutations pass, the check has no power.
- **Match on exact success output.** A grep that matches both the success and
  the failure line, or a status printed regardless of the value, is not a check.
- **Bind results to the source that produced them**, so that a proof step
  cannot consume results computed from an older version. The certified block
  must be the block the proof uses.
- **The object computed is the object claimed:** the same parameter values that
  actually ran, the same sign, the same branch. Check a description of the model
  (which terms carry a factor, which quantity was differentiated) against the
  program, not against the draft.
- **Every number in a public claim is copied from a named field of that run.**
  Say whether the digits were truncated or rounded. Do not take a nearby metric,
  a rounded display, or a number from memory. The domain of the claim is the
  domain that was proved, not a nearby round value.
- Transcribe a constant from the printed source and name the page. If a later
  source says the print is wrong, record both, and record which one the proof
  uses. Do not silently correct a printed constant.
- Do not report "verified" for anything no program actually checked. Map every
  verification claim in a paper to a committed, runnable check. Do not report a
  measurement that was not made.
- A check that was cut off, or that exists only in an uncommitted container, is
  not a pass. Say what was not run.
- Never round a measurement toward theory, and never hide a disagreement.
- Asserts stripped by optimization flags (`python -O`) are not gates. Use
  explicit failures.

## 5. Review adversarially, then doubt the reviewer

- For each proof or computational claim, start a **separate session** briefed only
  with the paper and its programs, and told to find errors. The drafting session
  does not review its own work, and does not check its own fixes.
- For a computer-assisted theorem, add an **independent reimplementation** that
  never reads the original code, or write down why that step was not done.
- Before applying a finding, give it to **one or two further sessions told to
  refute it**. Record findings that do not survive.
- A finding relayed from another assistant is not a finding until it is checked
  against the source. Do not adopt it on the relay.
- Two checkers that disagree are information. Two that agree are not proof.
- After fixes, have a further reader confirm them. Record that the reading
  happened, not that it is planned.

## 6. Label review honestly

- An AI reading is **not** peer review and not an outside review. Every review
  note says so in its first lines, for example: "An in-project reading by a
  separate AI session. It is not an outside review."
- Never write that work was independently or externally reviewed unless a person
  outside the project reviewed it.
- Name every AI tool that wrote, searched, checked, or reviewed, and say what it
  did. Naming only the main one is not a disclosure.
- Do not add a co-author trailer, email, or identity you have not verified
  belongs to a person who contributed. The git author name is not evidence of
  which assistant wrote the text.

## 7. Do not bend a gate to fit a release

- Before a preprint, release, or DOI, every quality item must be **done and
  recorded**, not planned. Do not tick an item before the record it certifies
  exists.
- If a gate fails, the release waits. Do not change the gate so the release
  passes. If a gate must change, record the change, the reason, and which release
  it unblocked. Make that change before the release, not in order to unblock it.
- After release, download the archive and confirm it contains the manuscript,
  the programs, and the data the notes name. A changelog heading is not evidence.
  If the project has no program gate, do not invent one. If it has one, do not
  edit it so this release passes. A green check on the branch is not the archive.

## 8. Optional: beat a checklist

Off unless the user asks, or the project already has a gate they chose to keep. When it is off, skip this section. A checklist the user is willing to tick is allowed.

When it is on:

- A committed program recomputes every public count from the file that produced it and exits non-zero if the prose disagrees.
- The same program must reject a planted fault: a wrong count, or a version string that does not match. Record that the fault failed and that the clean tree passed. A program that has not been shown to fail is not a gate.
- Do not change the program so this release passes. If the program is wrong, fix it first, and name the fault it previously missed.
- The archive that is tagged is the archive that was checked. Build it from the same commit, then download the published file and compare it to that build.

## Local tools, when the plugin is installed

Claude Code, and Cowork on the user's computer, start two shell scripts. Claude Chat does not. The skill zip has no server and no hook. Do not claim a tool ran if it is not connected.

Neither script starts another program, and neither opens a network connection.

- The hook scans the raw Write or Edit for the phrases in the table below. It warns, and the write proceeds, unless the current directory has `.research-integrity.json` containing `"block": true`. Then it blocks. It does not skip a table or a code fence. A hit is not proof the sentence is false.
- The server's only tool is `scan_text`, which reports those same phrases. It does not open a file and it does not search. It does not copy a number out of a file and it does not store a search row.

Not claimed. The hook cannot tell a quotation of a mistake from a new claim.

## Quality checklist (before any preprint or release)

- [ ] **Proofs complete.** No step is "left to the reader" or planned.
- [ ] **Computation rigorous.** Where a proof depends on a computation, it is
      exact or interval arithmetic, in a committed program that stops on a failed
      check, with a failure control that fails for the reason under test.
- [ ] **Every claim labelled** `proved`, `computer-assisted`, `cited`, `numerical`,
      or `conjectured`. Nothing `numerical` is used inside a proof.
- [ ] **Hypotheses checked.** Every cited theorem names the hypotheses checked
      against this instance, and names any that were not.
- [ ] **Numbers copied from the run.** Every public number names the field it
      came from. The claimed domain is the proved domain.
- [ ] **Sources read.** Every source a proof depends on is `read-directly`;
      background citations say how far they were read.
- [ ] **Prior work searched and logged**, with blocked and stopped sources listed,
      and every novelty statement within the search's reach. Superseded priority
      wording is gone from every file that ships.
- [ ] **Adversarial second reading done**, every must-fix fixed, and the fixes read
      by someone other than the drafting session.
- [ ] **Reproducible** from a fresh checkout with pinned versions.
- [ ] **Archive checked** by downloading it. It contains what the notes name.
- [ ] **Program gate, only if section 8 is on.** Public counts were recomputed from their files. A planted fault made the program fail. The downloaded archive matches the build that passed. If section 8 is off, leave this unticked and do not treat that as a failure.

## Phrases to avoid, and what to write instead

| Avoid | Write |
|---|---|
| "This is the first ..." | "Searches of X and Y found no earlier statement; Z could not be opened." |
| "Verified" (with no program) | "Checked by `script.py`, which fails on <control>." |
| "Independently reviewed" | "Read by a separate AI session in this project; not an outside review." |
| "No prior work exists" | "No prior work was found in the sources that loaded (listed below)." |
| "Exact" (for an enclosure) | "Enclosed in [a, b] by interval arithmetic." |
| "Computed" (for a proof) | "`computer-assisted`: decided by `script.py`, which fails on <control>." |
| "Holds in general" | "Proved on <the set that was proved>." |
| "Does not replicate" (weak test) | State the test, its power, and the result. |
| "The checklist passed" (only if section 8 is on) | "Checked by the project's gate, which fails when the stated count is wrong." |
