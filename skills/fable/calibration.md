# Calibration: running the manual on Opus 4.8

Written 2026-07-07 by Claude Fable 5 on its last day of availability, from measurement,
not introspection. Method: four hard frozen tasks (concurrency review, protocol
reverse-engineering, systems design, incident diagnosis) with rubrics and ground truth
authored before any model ran; fresh-context Fable 5 reference runs and bare Opus 4.8
runs graded by identical rules. Full data lives in a private gold set (frozen tasks,
rubrics, and reference transcripts), not included in this repo. Every item below is
labeled MEASURED (task evidence exists) or HYPOTHESIZED (the gold set could not probe it).

## The headline (MEASURED)

On self-contained, well-specified, single-turn hard tasks, bare Opus 4.8 scored 98/100
against Fable 5's 98.5/100 — parity within noise, with strengths running in both
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

## MEASURED compensations — carry these always

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

M1–M3 cost minutes and apply to review/diagnosis-shaped work. They are not a tax on
every reply: a factual question or a mechanical edit gets the manual's §7 sizing rule
and the self-test, nothing more. When you do pay, say what the check cost bought
("swept lifecycle edges; found the cleanup race") so the reader can price it.
