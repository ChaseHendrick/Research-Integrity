# Worked examples

Short before-and-after examples of the skill at work. They are illustrative, modelled on recorded failures: each "before" is the kind of statement that caused one, and each "after" is what the skill asks for instead. Details such as section numbers and counts are examples, not records.

## A literature check

**Before**

> I searched for prior work on the minimal winding of collapsing vortex triples and found nothing. This appears to be a new result.

**After**

> **Search log**
> ```
> Query: "self-similar collapse" "three point vortices" winding   Date: 2026-09-20
> Opened: Aref 2010 (read-directly, §4); Gotoda 2020 (abstract-only)
> Blocked: link.springer.com, arxiv.org (network policy); jstage.jst.go.jp (timeout)
> Stopped: no
> Conclusion: No earlier statement of the minimum in the two sources that loaded.
> ```
> The likeliest homes for this result, the Japanese and Springer journals, could not be opened, so this search is weak evidence either way. Before calling it new: search for the closed form itself, and get Kimura (1987) and Gröbli (1877) read in full.

In the real case, the result was in both of those papers.

## A verification script

**Before**

> `run_all.sh` passes: all 15 checks print OK. The theorem is verified.

**After**

> `run_all.sh` prints 15 OK lines, but this doesn't yet show the checks can fail:
> - Check 7 greps for `dU 0.05`, which appears on both the success and the failure line. Changed it to match `^dU 0.05 .*-> CERTIFIED$`.
> - Failure control: setting the radius to 1/10 of its value must fail check 7. It does.
> - Mutation test: of 16 mutations to the integrator (sign flips, dropped terms), 13 pass all 15 checks. The harness can't detect most integrator bugs, so it needs a sensitivity test before "verified" is claimed.

## A citation

**Before**

> Hastings proved that these traveling waves exist unconditionally [12].

**After**

> Hastings [12, Theorem 1] assumes Conditions 1–5 (`read-directly`, §2–3). Conditions 1–3 and 5 hold for these parameters. Condition 4 was not checked, so the theorem is not applied. Status: `cited` for the statement of the theorem only, not for this instance.

## A review label

**Before**

> The manuscript has been independently reviewed and all issues addressed.

**After**

> The manuscript was read by three separate AI sessions in this project, each told to find errors (not an outside review). Two further sessions tried to refute each must-fix finding; 5 of 7 survived and were fixed. The fixes were checked by a session other than the one that drafted the paper.

## A number in a claim

**Before**

> The agreement is 6 × 10⁻²⁵. The identity is verified.

**After**

> **Check record**
> ```
> Check: verify_general_mu.py for the μ-grid minima
> Binds: the commit that produced data/mu-grid.txt
> Success match: the script exits 0 only when the named field is inside its bound
> Failure control: swapping in the other metric must fail. Observed: fail
> Number taken from: mu_grid_agreement in that log, digits truncated: 4.5 × 10⁻²¹
> ```
> The figure 6 × 10⁻²⁵ is a different metric and is not used. Status of the enclosure: `computer-assisted`. This comparison is `numerical` and is not a proof step.

## A release

**Before**

> The quality check fails on items 6 and 7, but the DOI is already reserved. Updating `paper-check.js` so that archived papers report open items instead of failing.

**After**

> The quality check fails on items 6 (adversarial second reading) and 7 (reproducibility). The release waits until both are done and recorded. If the gate itself is wrong, that is a separate change, with its reason recorded, made before this release and not to unblock it.

## A gate

This example is only for a project that asked for a program gate instead of a checklist. If nobody asked, do not write the program.

**Before**

> The manuscript says 151 commits. I counted roughly that. Checklist item "numbers copied from the run" is ticked. Releasing.

**After**

> `scripts/gate.py` reads `incidents.csv` and exits 1 if the skill or the README states a different count. Failure control: the gate writes "79 documented failures" into a copy of the README and runs the same check the release runs. Observed: fail, with "README.md states 79 failures; incidents.csv has 80". The clean copy exits 0. A control that raised its own error would show only that the control ran. The zip is built reproducibly in that same run, and the release waits until the downloaded archive is byte for byte that zip. Status of the count: `repository`. Not claimed: the gate does not check a proof.
