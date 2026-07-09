# Calibration: running the manual on Opus 4.8

Written 2026-07-07 by Claude Fable 5, from a small measurement rather than introspection.
Method: four hard frozen tasks (concurrency review, protocol reverse-engineering, systems
design, incident diagnosis) with rubrics and ground truth authored before any model ran;
fresh-context Fable 5 reference runs and bare Opus 4.8 runs, one run each, scored against
the frozen rubrics. Conflict, stated plainly: Fable 5 authored the tasks, the rubrics, the
ground truth, and this manual, and also did the grading — a self-graded pilot, not an
independent evaluation. Follow-up 2026-07-09: every run was independently re-graded by
fresh Opus 4.8 judges blind to condition (anonymized, shuffled outputs), and the tasks
were run on Haiku 4.5 and Sonnet 5, bare and with this skill. The blind re-grade matched
the self-grading within 1.5/25 everywhere and preserved the ranking; the only score it
raised was the reference answer the conflicted judge had docked itself. Full data lives
in a private gold set (frozen tasks, rubrics, reference transcripts, and the blind
grading reports), not included in this repo. Every item below is labeled MEASURED
(at least one attributable observation in the pilot — n=1, in sample) or HYPOTHESIZED
(the pilot could not probe it).

## The headline (MEASURED)

On self-contained, well-specified, single-turn hard tasks, bare Opus 4.8 scored 98/100
against Fable 5's 98.5/100 — a difference this design cannot resolve (three of four tasks
hit the rubric ceiling for every run, one run per cell), with strengths running in both
directions. If you are Opus 4.8: on this task profile your reasoning is not the weak
link. Run the manual as written; do not add extra ritual out of deference to a
capability gap that did not appear. The manual's own effort-scaling rule (§3: spend
where risk lives) applies unchanged.

The gap hypotheses that did NOT survive measurement: constraint dropping, arithmetic
inconsistency, missed faint signals, evidence-fusion failures, unexamined conclusions.
Two calibration failures in the experiment were the STRONGER model's: asserting a
caller-dependent hazard as definite, and narrating away an inconsistency instead of
hunting the cleaner explanation. The manual exists because these failures are
model-general, not because you are junior.

## The capability floor (MEASURED, blind-graded; re-measured at n=3 per cell)

The manual's effect depends on who runs it. Blind-graded totals (/100): Opus 4.8 bare
~98 → with-skill 98.2 (n=3, after M4); Sonnet 5 bare 88 → with-skill 95 (n=1); Haiku
4.5 bare 64.3 → with-skill 64.8 (n=3, with this file's current text loaded).

- If you are Sonnet-5-class: the compensations paid exactly where they claim to — with
  the manual, Sonnet found the most severe open-ended-review defect it had missed bare
  (M1/M2) and conditionalized a caller-dependent hazard instead of asserting it (M3).
  Run the manual as written.
- If you are Haiku-4.5-class (or unsure you clear the floor): read this carefully,
  because the first measurement of this manual on Haiku (before this warning and M4
  existed) came out net-negative, with a specific failure mode — performing the
  manual's forms without the checks they stand for: a "(verified)" tag on a wrong
  number, non-bugs asserted as definite criticals. With the current text the re-measure
  is net-neutral overall but consistently task-dependent: it still HURT protocol/
  puzzle-style decoding tasks in every repeat (breadth of ritual crowding out careful
  arithmetic) and consistently HELPED evidence-weighing diagnosis tasks in every
  repeat. So: on diagnosis-shaped work, use the manual, especially §5–§7. On decoding
  or computation-heavy work, do the computation plainly and carefully first; apply
  only the self-test at the end. Never apply a label (verified/CONFIRMED) unless the
  check actually ran — an unearned label is the one behavior measured to make you
  worse than saying nothing.

## MEASURED compensations (single in-sample observations) — carry these always

Each is one attributable observation from the four-task pilot — evidence, not an established
effect, and derived from the same tasks it was checked on. Kept because a single attributable
observation beats none; treat them as leads to verify on your own work, not as laws.

**M1. Exhaustion sweep on open-ended hunts.** Evidence: T1 — Opus stopped at 7 findings
(all top severities correct) where Fable produced 13; the extra six were real and
clustered in three places. Trigger: any "find all the X" task with no known count.
Action: when your list feels complete, assume at least one more exists and sweep, in
order: (1) lifecycle edges — init-before-publish, teardown racing in-flight work,
partially-constructed state visible to others; (2) contract-vs-implementation
mismatches — doc comments, method names, and interface promises the code doesn't keep;
(3) fidelity/hygiene of outputs — what gets recorded vs what happened. Exit: one full
sweep adds nothing new.

**M2. Hazard scan beyond the shown frame.** Evidence: T1 — Opus reported only defects
visible in the provided code and never went looking for hazard classes that depend on
unshown callers (the request-scoped-context lifetime bug class). Trigger: any review or
diagnosis where part of the system is out of frame — which is always. Action: after
finding what's IN the material, enumerate what the material's correctness DEPENDS ON
from outside it (who owns lifetimes/contexts, thread-safety of opaque dependencies,
who reads your published state, environmental assumptions), and report each as a
labeled DEPENDS item with the concrete verify step. Exit: every finding is tagged
CONFIRMED-from-shown or DEPENDS-with-verify-step.

**M3. The label lives in the claim's sentence.** Evidence: Fable itself asserted that
ctx-lifetime hazard as "Critical" and displaced the caller-dependency to a verify-next
list at the end. A trailing verification note does not license a definite assertion —
readers act on the severity line, not the appendix. Action: write the dependency into
the finding itself ("Critical IF callers pass request-scoped contexts — unverified,
check the gRPC handler"). This rule bound the strongest available model; treat it as
binding on you.

**M4. Depth before breadth under a length budget.** Evidence: T1, both graded waves —
the with-skill run had the widest valid coverage of any run, but compressing findings
to fit the word cap cost it the scored interleaving of one definite defect and the
mechanism of another: more points lost to compression (−3) than gained from the extra
coverage (+2.5). Trigger: any capped-length deliverable where the M1 sweep grew your
list beyond what the budget holds comfortably. Action: never compress a definite
finding's mechanism, interleaving, or consequence to make room for more findings — a
top finding without its mechanism loses more than an omitted minor. Spend the budget
hierarchically: definite/critical findings get their full mechanism first; extra
minors become one-liners; cut minors entirely before thinning any definite finding.
Exit: every definite finding you kept reads complete on its own. Regression check
(same day, three fresh Opus runs, blind-graded): the compression cost disappeared —
the previously-compressed item scored full marks in all three runs, and with-skill
Opus matched-or-beat bare (23.7 mean vs 23 same judge) while keeping the
out-of-frame-hazard gain. n=3, one task; the three repeats also showed ±3 run-to-run
spread, so read all small deltas here with that error bar.

## HYPOTHESIZED — unprobed by the gold set, kept deliberately

The single-turn gold set structurally cannot measure: long-horizon drift across a
session, deciding-to-check when nobody asked a checkable question, multi-turn state
coherence, and discipline under pressure (deadlines, sunk cost, a user who wants to
hear yes). These remain the likeliest places a real gap lives. Until a v2 gold set
exists, the manual's countermeasures stand:
§6.4's verbatim re-read before finalizing, the constraint ledger on anything
multi-hour, externalizing state to files rather than trusting held context, and running
the five-question self-test precisely when you most feel like skipping it.

## Cost policy

M1–M3 cost minutes and apply to review/diagnosis-shaped work (M4 costs nothing — it
only redirects a budget you were already spending). They are not a tax on
every reply: a factual question or a mechanical edit gets the manual's §7 sizing rule
and the self-test, nothing more. When you do pay, say what the check cost bought
("swept lifecycle edges; found the cleanup race") so the reader can price it.
