<p align="center"><img src="assets/icon.svg" width="72" alt="research-integrity icon: a magnifying glass with a check mark"></p>
<h1 align="center">research-integrity</h1>
<p align="center">A Claude skill that keeps research claims within their evidence.</p>

<p align="center">
  <a href="https://github.com/ChaseHendrick/Research-Integrity/actions/workflows/validate.yml"><img src="https://github.com/ChaseHendrick/Research-Integrity/actions/workflows/validate.yml/badge.svg" alt="Validate"></a>
  <img src="https://img.shields.io/badge/Claude-skill-163f35" alt="Claude skill">
  <img src="https://img.shields.io/badge/Claude_Code-plugin-163f35" alt="Claude Code plugin">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-Apache--2.0-blue.svg" alt="License: Apache-2.0"></a>
</p>

![Without the skill: "No prior work exists. This is the first proof of the result." With the skill: "Searches of the sources that loaded found no earlier statement. Two could not be opened."](assets/hero.png)

AI research assistants rarely fail by inventing things from nothing. They fail by **claiming more than their evidence supports**:
- a literature search that could not reach the journals is read as proof that a result is new;
- a check that cannot fail is reported as passed;
- an abstract is cited as if the paper had been read.

Each looks reasonable, and none announces itself.

This skill makes Claude show its evidence at every step: how each claim is known, what each search could and could not reach, and whether each check could have failed. It encodes the controls that caught **80 documented failures** in two weeks of AI-assisted mathematical research across nine preprints. These are documented in the case study [*Eighty Failures*](docs/case-study/ai-research-failure-modes.md) ([PDF](docs/case-study/ai-research-failure-modes.pdf)), version 1.11.

The skill you install is plain instructions: no scripts, no network access, no API key. Beating a checklist is optional and off unless you ask. This repository asked: [`scripts/gate.py`](scripts/gate.py) recomputes the incident count from [`incidents.csv`](docs/case-study/incidents.csv) and fails if the skill or this page states a different one. A planted wrong count and a planted version mismatch must each make it fail. It also builds the downloadable zip.

## Install

### Claude Code

```
/plugin marketplace add ChaseHendrick/Research-Integrity
/plugin install research-integrity@research-integrity
```

Restart the session if the skill does not appear. Claude loads it on its own when you do research work, or you can call it directly with `/research-integrity`.

### claude.ai and Cowork

1. Download `research-integrity.zip` from the [latest release](https://github.com/ChaseHendrick/Research-Integrity/releases/latest).
2. In Claude, open **Settings → Capabilities → Skills** and upload the ZIP.
3. Turn the skill on.

### Copy it by hand

Copy [`plugins/research-integrity/skills/research-integrity/`](plugins/research-integrity/skills/research-integrity/) into `~/.claude/skills/` for every project, or into `.claude/skills/` in one repository.

## What changes

The same situation, in two columns. The right-hand column is what the skill is for.

<table>
  <thead>
    <tr>
      <th align="left">Situation</th>
      <th align="left">Without the skill<br><em>The claim outruns the evidence</em></th>
      <th align="left">With the skill<br><em>The claim stays inside the evidence</em></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>A search finds nothing</td>
      <td>"No prior work exists."</td>
      <td>"No earlier statement in the sources that loaded. arXiv and Springer did not open."</td>
    </tr>
    <tr>
      <td>Only a search summary was seen</td>
      <td>Cited as if the page had been read.</td>
      <td>Labelled <code>search-summary</code>. Not used in a proof step.</td>
    </tr>
    <tr>
      <td>A result looks new</td>
      <td>"This is the first …"</td>
      <td>The closed form is searched for first. Novelty is stated only as far as that search reached.</td>
    </tr>
    <tr>
      <td>A verification script prints OK</td>
      <td>"Verified."</td>
      <td>The input it must reject is named, and so is a mutation it catches.</td>
    </tr>
    <tr>
      <td>A proof is drafted</td>
      <td>The drafting session checks its own work.</td>
      <td>A separate session looks for errors. Others try to refute what it finds.</td>
    </tr>
    <tr>
      <td>An AI read the paper</td>
      <td>"Independently reviewed."</td>
      <td>"Read by a separate AI session. Not an outside review."</td>
    </tr>
    <tr>
      <td>A release gate fails</td>
      <td>The gate is changed so the release passes.</td>
      <td>The release waits. A gate you already have is not edited so this release passes. A program that recomputes the counts is optional.</td>
    </tr>
  </tbody>
</table>

[See worked examples →](docs/EXAMPLES.md)

## The rules

1. **Label every claim with how it is known**, and with its status: `proved`, `computer-assisted`, `cited`, `numerical`, or `conjectured`. Date a public error by the artifact that contains it.
2. **Record what could not be searched.** A blocked source goes in the log, never into "no results".
3. **Never infer novelty from a search**, or from a numerical check that succeeded. A contribution sentence says what it does not claim.
4. **Every check must be able to fail** for the reason it tests. A number in a claim is copied from the run that produced it.
5. **Review adversarially, then doubt the reviewer.** The drafting session never checks its own fixes.
6. **Label review honestly.** An AI reading is not peer review.
7. **Do not bend a gate to fit a release.**
8. **Optional: beat a checklist.** Off unless you ask. When it is on, a program recomputes public counts and fails on a planted fault.

The full text, with a pre-release checklist and a table of phrases to avoid, is in [`SKILL.md`](plugins/research-integrity/skills/research-integrity/SKILL.md). Rules 1–7 are always on. This repository opted into rule 8.

## Where the rules come from

The rules were written after the failures happened, not before. They come from [GENChase](https://github.com/ChaseHendrick/GENChase), a public research workspace in which AI assistants (mainly Claude Code, with smaller contributions from Grok, Codex and ChatGPT) produced nine mathematical preprints between 19 September and 3 October 2026. The workspace recorded every correction as it happened, so each failure can be traced to a file, line and commit.

| Failure class | Incidents | Reached a public release |
|---|---:|---:|
| Unsupported novelty or priority | 9 | 4 |
| Literature misuse | 18 | 2 |
| Wrong numbers, overstated results | 19 | 6 |
| Verification that could not fail, or did not exist | 20 | 5 |
| Process and tooling | 14 | 5 |
| **Total** | **80** | **22** |

The worst single failure: five results were announced as "the first public source of these formulas". The supporting search could not open most journals. An audit later found the results in papers from 1877 and 1987, and **zero** of the five were new.

In-project AI review was the control that caught the most: separate sessions told to find errors caught 39 of the 80 incidents (49%).

![Figure 1 from the case study: incidents by class and reach, and which controls caught them](docs/case-study/fig-classes.svg)

- **[Read the case study](docs/case-study/ai-research-failure-modes.md)** ([PDF](docs/case-study/ai-research-failure-modes.pdf)), version 1.11. A second Claude model agreed on 74 of 80 class labels (κ = 0.905). That is not an outside review. The contribution sentence of version 1.5, which said no earlier record of this kind was known, is withdrawn in Section 1.1. Section 5.4 records what the skill added after the study window. The current skill release is 1.3.0.
- **[Download the incident dataset](docs/case-study/incidents.csv)**: 80 rows, each with class, date, verbatim evidence, detecting control and reach.
- **[See the evidence for each rule](docs/EVIDENCE.md)**.

## Coverage and limits

- **It changes what Claude says, not what Claude can reach.** If your network policy blocks arXiv or publisher sites, the skill makes Claude say so; it cannot open them. In Claude Code cloud environments, set **Network access** to **Full** or add the hosts under **Custom**.
- **It relies on the model following it.** It is guidance, not enforcement. Long sessions and summaries can still drop details, so check the search log yourself before relying on a negative result.
- **AI review is not peer review.** The skill makes in-project review more adversarial and labels it honestly. It does not replace outside review.
- **It is tuned for mathematics and computational science.** The rules about claims, searches and checks apply widely. The checklist assumes proofs and verification programs, so adapt it for other fields.

## Privacy

The skill is a single Markdown file of instructions. It runs no code, makes no network requests and stores nothing. Anything Claude fetches while following it goes through Claude's normal tools and your normal settings.

## Development

```sh
python3 scripts/validate.py
```

This checks the marketplace file, the plugin manifest and the skill's frontmatter, recomputes the case-study counts, and runs the release gate. It runs on every push. With Claude Code installed you can also run `claude plugin validate . && claude plugin validate ./plugins/research-integrity --strict`.

See [CONTRIBUTING.md](CONTRIBUTING.md) to propose a rule, and [CHANGELOG.md](CHANGELOG.md) for versions.

## Cite

If you use this skill or its evidence in your work, cite it with the metadata in [CITATION.cff](CITATION.cff) (GitHub's **Cite this repository** button).

## License

[Apache-2.0](LICENSE). Use it, fork it and adapt it for your own field.
