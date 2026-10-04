# research-integrity

A Claude skill that keeps an AI research assistant's claims within their evidence.

It comes from a documented record of **80 failures in two weeks of AI-assisted mathematical research**, across nine preprints. Most of those failures were not inventions. They were claims that outran their evidence:
- a literature search that could not reach the journals, read as proof of novelty;
- a check that could not fail, reported as passed;
- an abstract read as if it were the paper;
- a number taken from a mislabeled metric.

The skill encodes the controls that caught them.

## What it does

When Claude does research work (literature searches, novelty checks, proofs, verification code, reviews, releases), the skill has it:

1. **Label every claim with how it is known**: `read-directly`, `abstract-only`, `search-summary`, `repository` or `reasoning`. A search summary is never treated as a reading.
2. **Log what could not be searched.** Blocked and paywalled sources are recorded, and "I did not find it" is not used when the likeliest source never loaded.
3. **Never infer novelty from a search.** Novelty is stated only within the search's reach, and classical sources are credited.
4. **Make every check able to fail**, using failure controls, mutation testing, exact output matching and results bound to their source.
5. **Review adversarially.** Separate sessions find errors, further sessions try to refute the findings, and the drafting session never checks its own fixes.
6. **Label review honestly.** An AI reading is not peer review.
7. **Not bend a release gate to fit a release.**

It also includes a pre-release quality checklist and a table of phrases to avoid, with what to write instead.

## Install

In Claude Code:

```
/plugin marketplace add ChaseHendrick/research-integrity
/plugin install research-integrity@research-integrity
```

Or copy `plugins/research-integrity/skills/research-integrity/` into `~/.claude/skills/`.

## Evidence

The rules are drawn from the public [GENChase](https://github.com/ChaseHendrick/GENChase) research workspace. The case study *Eighty Failures: Error Modes and Controls in AI-Assisted Mathematical Research* (Hendrick, 2026) documents each incident with a file, line and commit.

## License

Apache-2.0
