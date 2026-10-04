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

> Hastings [12, Theorem 1] proves existence under his Conditions 1–5 (`read-directly`, §2–3). We have not checked that our parameters satisfy Condition 4.

## A review label

**Before**

> The manuscript has been independently reviewed and all issues addressed.

**After**

> The manuscript was read by three separate AI sessions in this project, each told to find errors (not an outside review). Two further sessions tried to refute each must-fix finding; 5 of 7 survived and were fixed. The fixes were checked by a session other than the one that drafted the paper.

## A release

**Before**

> The quality check fails on items 6 and 7, but the DOI is already reserved. Updating `paper-check.js` so that archived papers report open items instead of failing.

**After**

> The quality check fails on items 6 (adversarial second reading) and 7 (reproducibility). The release waits until both are done and recorded. If the gate itself is wrong, that is a separate change, with its reason recorded, made before this release and not to unblock it.
