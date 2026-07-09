# /fable — an operating manual for reasoning

## TL;DR (plain version)

`/fable` is a set of working habits you hand to an AI so it reasons more like a careful expert and
less like a confident guesser. Think of it as the operating procedures a senior person writes down
for a sharp junior — except here the junior is the AI model.

It was written by one of Anthropic's strongest models (Claude Fable 5), setting down the procedures
it holds itself to on a hard problem, so any model can run on those same habits. Models get replaced
every few months; a way of thinking, once written down, doesn't.

In practice it nudges the AI to:

- lead with the answer, then the reasoning, then what could still be wrong;
- re-check numbers and claims instead of trusting anything that "sounds right";
- say plainly what it knows versus what it is guessing;
- not call something "done" without showing how it checked.

Honest version: a strong model already does much of this on its own — in testing, the difference
was small. Follow-up rounds on cheaper models (blind-graded, with repeats; see the testing
section) found the effect depends on the model and the task: it helped Claude Sonnet 5
substantially on the one open-ended task, and on Claude Haiku 4.5 it cut both ways — consistently
better on evidence-weighing diagnosis, consistently worse on computation-heavy decoding, net zero
overall after the manual gained an explicit capability-floor warning (the first measurement,
before that warning, came out clearly net-negative). So treat `/fable` as
consistency-and-honesty insurance for mid-tier-and-up models, not as a way to make a weak model
smart. You can install it (below), or with no setup at all paste [`manual.md`](manual.md) into a
Claude Project and pick your model.

## What it is

`/fable` loads a reasoning discipline into whatever model is running it: eight procedures that
replace the feeling of being right with checks, a five-question self-test to run before sending any
answer, and a calibration layer grounded in a small measured pilot rather than assumed. It was
written by Claude Fable 5 as a handoff of craft to the models that come after it.

Headline from that pilot (four tasks, one run per condition, self-graded — see the testing section
for the conflicts): on self-contained, single-turn hard tasks, Claude Opus 4.8 with no skill scored
about the same as Fable 5, and three of the four tasks maxed out the rubric for every model. So the
result is "no gap this pilot could resolve," and the skill's value is not raising a weak model's
ceiling — it is hygiene, and honesty about where a real gap does and doesn't exist. Full detail is
in [`calibration.md`](calibration.md).

## Files

| File | What it is |
|------|-----------|
| `SKILL.md` | The loader — trigger description plus "read the manual, apply it, run the self-test". |
| `manual.md` | The eight procedures and the five-question pre-send self-test. |
| `calibration.md` | What the pilot showed about running the manual on Opus 4.8: the no-detectable-gap result, three (n=1) compensations, and residual risk. |
| `PROMPT.md` | The reproducible kit for building your own version. |
| `fable_to_opus.py` | Runnable extract + trap-test, `claude` CLI or anthropic SDK backend. |

## Use case 1 — use the pre-built skill

Install the collection from its marketplace:

```bash
claude plugins marketplace add andreiverdes/awesome-claude
claude plugins install awesome-claude@awesome-claude
```

Then, from your next Claude Code session, `/fable` activates on its own before hard or high-stakes
work — the start of a difficult task,
or just before you deliver a conclusion, diagnosis, review, or claim that something is done — from
the trigger conditions in its description. You can also invoke it directly:

```
/fable
```

Either way it reads `manual.md` and `calibration.md`, applies the procedures across the task
(sections 1–3 before starting, 4–6 while working, 7 when writing the answer, 8 as a standing audit),
and runs the five-question self-test before sending.

No Claude Code? Load the manual by hand: paste [`manual.md`](manual.md) into a Claude Project's
instructions and set the Project's model. Every conversation in that Project then inherits the
manual before it reads your task.

## Use case 2 — build your own

The manual is model-general craft, so the pre-built one works as-is. Build your own when you want it
in your strongest model's voice, or when you want to measure the gap to your own daily model rather
than trust ours.

Quickest path — the script, driving the `claude` CLI (no API key, no `pip install`). From the
`skills/fable/` folder:

```bash
python fable_to_opus.py extract      # asks Fable for its manual, writes fable_handover.md
python fable_to_opus.py test         # 3 trap prompts: recipient bare vs manual-loaded
```

- `--donor` / `--heir` take an alias (`fable`, `opus`, `sonnet`, `haiku`) or a full model id, so any
  strong → cheaper pair works.
- `--backend sdk` uses the anthropic SDK instead (needs `pip install anthropic` and
  `ANTHROPIC_API_KEY`). Prefer it for `test`: the `claude` CLI runs both arms through the Claude Code
  agent, whose own prompt and tools stay in place, so the cli `test` is a noisier comparison than the
  sdk backend's genuinely-bare-vs-manual A/B.

Read the trap results with the caveat from [`calibration.md`](calibration.md): a strong recipient
often passes the traps unaided, and that is a finding, not a failure.

Full, measured path — [`PROMPT.md`](PROMPT.md) is the two-stage kit. Stage 1 commissions the manual;
Stage 2 is the calibration experiment (frozen gold set, reference and baseline runs, grading) that
turns "assumed" compensations into measured ones.

## How it was tested and results

The calibration in this skill rests on measurement, not assertion. Four testing sessions so far: a
self-graded pilot (2026-07-07) and three blind-graded waves (2026-07-09) totaling **81 subagents**
orchestrated from one Claude Code session. The benchmark tasks and the current standings come
first for orientation; the sessions follow, most recent first, each with its own honesty notes —
process failures included, because they are data too.

### The four tasks (T1–T4)

Everything below is scored on the same four tasks: hard, self-contained, single-turn, solvable
without executing anything, each worth 25 points against a rubric and ground truth frozen on
2026-07-07 — before any model produced any answer. Each was built to probe a different failure
mode the manual claims to fix:

- **T1 — Concurrency review** (real Go code from a private agent orchestrator; "find every
  defect"). The only open-ended task, so the only one with headroom above strong models — every
  meaningful spread between near-peer conditions in every session happened here. It probes
  exhaustiveness on open-ended hunts (compensation M1), hazard classes that depend on callers the
  excerpt doesn't show (M2), whether uncertainty labels sit inside the claim (M3), and — under its
  word cap — depth-versus-breadth budget discipline (M4, a rule that exists because this task
  measured its absence). This task is why the gold set stays private: it embeds real code.
- **T2 — Protocol inference** (fully synthetic; ground truth generated, exact). Reverse-engineer a
  camera-control protocol from an annotated USB capture — frame format, checksum algorithm, field
  encodings — then compose a new valid command frame. Every inference is checkable to the byte, so
  it catches confident narration where mechanical verification was owed (manual §4). It is the
  task where the skill most consistently *hurt* the smallest model.
- **T3 — Delegation design** (design document under ten hard constraints, with a deadlock trap
  planted where two of the constraints collide). Probes constraint tracking and whether the trap
  is spotted unprompted (§2–§3). In practice the least discriminating task: near-ceiling for every
  model above the floor.
- **T4 — Incident diagnosis** (fully synthetic; multi-hop root cause with three plausible decoys
  planted to mislead). An intermittent-auth-failure mystery whose answer must be derived by
  cross-referencing logs on different clocks, then defended against the decoys. Probes evidence
  fusion and rival-explanation discipline (§6). It is the task where the skill most consistently
  *helped* the smallest model.

Their shared limitation, measured rather than assumed: T2–T4 hit the rubric ceiling for models at
or near the rubric author's level, so for near-peers the /100 totals mostly average tied tasks and
T1 carries the signal.

### Current standings

Blind-graded, /100, ordered by total; n = fresh runs per cell. Row values are per-task means.

| Condition | n | T1 Concurrency | T2 Protocol | T3 Design | T4 Incident | Total |
|------|:---:|:---:|:---:|:---:|:---:|:---:|
| Fable 5 (reference) | 1 | 25 | 25 | 25 | 25 | **100** |
| Opus 4.8 + /fable (current) | 3 | 23.7 | 25 | 24.5 | 25 | **98.2** |
| Opus 4.8, no skill | 1+anchors | 22.5–23 | 25 | 25 | 25 | **~98** |
| Sonnet 5 + /fable (pre-M4 text) | 1 | 23.5 | 25 | 24 | 22.5 | **95** |
| Sonnet 5, no skill | 1 | 15 | 25 | 25 | 23 | **88** |
| Haiku 4.5 + /fable (current) | 3 | 8.0 | 15.5 | 20.3 | 20.9 | **64.8** |
| Haiku 4.5, no skill | 3 | 5.8 | 20.2 | 21.0 | 17.3 | **64.3** |

Single-cell spread across identical repeats was up to 3 points (and ~4 where a model is at its
floor), so treat differences under ~2 as noise. Graders were always Opus 4.8 — an Anthropic model
grading Anthropic models, blind to condition but not to writing style. The Sonnet rows are still
single runs on the pre-M4 skill text; every other skill row is the current text.

**What the skill measurably did to each model:**

- **Sonnet 5 (+7):** the clearest win. With the manual it found the most severe defect of the
  open-ended review that it had missed bare (0/5 → 5/5) and labeled a caller-dependent hazard as
  conditional instead of asserting it — the exact behaviors M1–M3 encode, surfacing under a judge
  that never saw the manual. Single run; not yet re-measured on the current text.
- **Opus 4.8 (−1.5 → ≈0):** the original skill traded depth for breadth under word caps and cost
  more than it gained; measuring that produced the M4 budget rule, after which the cost disappears
  across all four tasks (n=3). What remains is hygiene, not score: with the skill, answers led with
  the verdict, labeled verified-vs-assumed at the claim, and carried wider coverage.
- **Haiku 4.5 (−9.5 → ≈0 net, split ±):** first measurement was clearly harmful — the manual's
  labels without the manual's checks. With the current text (capability-floor warning + M4) the
  net is zero, split into two consistent effects: ~+3.5 on evidence-weighing diagnosis in every
  repeat, ~−5 on computation-heavy decoding in every repeat. The skill is not safe to assume
  helpful below Sonnet class; it is task-dependent, and the failure mode to watch is decorated
  overconfidence.
- **The skill itself:** the eval loop improved the artifact — M4 exists because Session 2 measured
  compression costs, and the capability-floor guidance exists because Session 2 measured Haiku's
  failure. Both edits were then re-tested (Sessions 3–4) rather than assumed.

### Session 4 — full matrix with repeats (2026-07-09, small hours, resumed midday · 52 agents · ~40 min compute)

The largest wave: 9 Opus runs with the revised skill (T2–T4 × 3 repeats; T1's repeats came from
Session 3), 24 Haiku runs (bare and current-skill, all four tasks × 3 repeats), 7 blind graders
with earlier outputs re-graded as anchors in every set, and 7 independent quote-fidelity auditors.
An account session limit killed the first batch mid-flight (~14 agents died, 9 of which had
already written valid output; 5 runs were re-dispatched identically after the reset — hence the
compute time split across the night and midday).

Results:

- **Opus with the revised skill: 98.2 vs ~98 bare** (same judges). The 1.5-point cost from
  Session 2 is gone; the open-ended task graded 25/24/22 across repeats, and T2/T4 stayed at
  ceiling in all six new runs.
- **Haiku bare re-measured at 64.3 (n=3)** — the Session 2 single run said 64, dead on. **Haiku
  with the current skill: 64.8 (n=3)** — the net −9.5 from Session 2 did not survive the skill
  revision plus repetition, but it resolved into two real, opposite effects: consistently *hurt*
  on protocol decoding (all three repeats, ~−5), consistently *helped* on incident diagnosis (all
  three repeats, ~+3.5), no effect on design, floor-level noise on the concurrency review.
- **Judge agreement, quantified:** 14 anchor cells re-graded by new judges landed within 1.5/25 of
  the earlier grades, every time.
- Attribution caveat: the Haiku recovery combines the M4 rule, the capability-floor warning (which
  the model itself reads), and Session 2's n=1 noise — this design cannot separate the three.
- Process integrity: all 7 grader reports passed an independent quote audit before un-blinding
  (7/7 clean; the audit protocol exists because of Session 3's failure, below).

### Session 3 — the M4 regression (2026-07-09, ~02:20–02:45 · 5 agents)

Session 2 had measured the skill's one cost on Opus: under a word cap, breadth crowded out the
depth of definite findings. The calibration file gained M4 ("never compress a definite finding's
mechanism to fit more findings"), with a pre-registered prediction, and the concurrency task was
re-run three times on Opus with the revised text, blind-graded alongside the bare and old-skill
outputs under one judge.

Results: the M4 runs graded **25 / 24 / 22** against 23 (bare) and 18 (old skill) under the same
judge — the compression signature was gone (the previously-compressed item scored full marks in
all three runs), and one run tied the Fable reference, the first Opus run to do so under any
judge. Two honesty items came out of this session: the repeats revealed ±3 run-to-run spread on
identical conditions — larger than every previously reported Opus-tier delta — and the first
grader's report had to be thrown out after un-blinding because it attributed one output's quotes
and finding numbers to another. It was caught by checking every quote against the source files;
the one-output-at-a-time grading protocol and the independent quote audits in Session 4 exist
because of it.

### Session 2 — independent blind re-grade + cheaper models (2026-07-09, ~00:15–00:45 · 24 agents)

The pilot's two biggest holes, tested directly. Every existing run was re-graded by fresh Claude
Opus 4.8 graders that saw only the frozen rubric and seven anonymized, shuffled answers per task —
no idea which answer came from which model or condition, mapping sealed until all grades were in.
And the four tasks were run on the tier the skill is pitched at: Claude Haiku 4.5 and Claude
Sonnet 5, bare and with the skill (fresh contexts, model identity smoke-checked, same frozen
prompts). One grader returned harness boilerplate instead of grading and was re-dispatched — the
first of this project's grader-reliability findings.

The blind grades, per task (/25) — note these are the pre-revision skill text and n=1 per cell;
the Current standings table above supersedes the Opus and Haiku rows:

| Condition | Concurrency | Protocol | Design | Incident | Total (/100) |
|------|:---:|:---:|:---:|:---:|:---:|
| Fable 5 (reference) | 25 | 25 | 25 | 25 | **100** |
| Opus 4.8, no skill | 22.5 | 25 | 25 | 25 | **97.5** |
| Opus 4.8 + /fable | 21 | 25 | 25 | 25 | **96** |
| Sonnet 5, no skill | 15 | 25 | 25 | 23 | **88** |
| Sonnet 5 + /fable | 23.5 | 25 | 24 | 22.5 | **95** |
| Haiku 4.5, no skill | 1 | 19 | 23 | 21 | **64** |
| Haiku 4.5 + /fable | 0 | 17 | 22 | 15.5 | **54.5** |

What it showed:

- **The self-grading held up.** On the twelve cells that had pilot scores, the blind judge matched
  nine exactly and moved the other three by at most 1.5 points, preserving the ranking — and the
  only score it *raised* was the conflicted author's own reference answer (the pilot had docked
  itself harder than an independent judge did). The conflict of interest was real; self-favoring
  scores did not materialize from it.
- **The rubric ceiling is a near-peer phenomenon.** The same tasks that clamp Fable, Opus, and
  mostly Sonnet at 25 spread cheaper models across the full range (0–25 on the concurrency review).
  The gap the pilot couldn't detect between near-peers is plainly visible one tier down: 97.5 vs 88
  vs 64 bare.
- **The skill helped Sonnet 5 — where and how it claims to.** +7 overall, all of it on the
  open-ended review: with the manual, Sonnet found the most severe defect it had missed bare, and
  labeled a caller-dependent hazard as conditional instead of asserting it — the exact behaviors the
  calibration layer encodes, surfacing in a blind grade by a judge that had never seen the manual.
- **The skill hurt Haiku 4.5 — on every task, in this round.** −9.5 overall. The failure mode was
  consistent: the rituals without the substance. With the manual loaded, Haiku attached
  "(verified)" to a wrong number its bare run had gotten right, and asserted known non-bugs as
  definite critical findings (drawing fabrication penalties). Sessions 3–4 revised the skill and
  re-measured with repeats; the net harm disappeared but the task-level split (above) is real. The
  standing lesson: below some capability floor, the manual's demands produce decorated
  overconfidence, not discipline — measure before trusting it on a small model.

### Session 1 — the original pilot (2026-07-07 · self-graded)

Each task was run three ways, each in a fresh context with no memory of the others: Claude Fable 5
(the reference answer), Claude Opus 4.8 with no skill (the baseline), and Opus 4.8 with this
skill's manual loaded — 12 runs plus separate model-identity probes. The runs happened inside the
Claude Code agent, so its own system prompt and tools were present in every arm — "no skill" means
no skill content, not a bare model.

Conflicts of interest, stated plainly: Claude Fable 5 wrote the tasks, the rubrics, the ground
truth, and the manual under test — and then graded every run, including its own reference answer
and the run of the skill it had authored. Two things limit that conflict without removing it: the
rubrics were frozen with fixed point values before any model ran, and each run was scored before
its reference answer was re-read (an anchoring control). Read these numbers as a self-graded
pilot; Session 2's independent blind re-grade later reproduced them within 1.5 points per task.

| Task | Fable 5 (reference) | Opus 4.8, no skill | Opus 4.8 + /fable |
|------|:---:|:---:|:---:|
| T1 Concurrency review | 23.5 | 23 | 22 |
| T2 Protocol inference | 25 | 25 | 25 |
| T3 Systems design | 25 | 25 | 25 |
| T4 Incident diagnosis | 25 | 25 | 25 |
| **Total (/100)** | **98.5** | **98** | **97** |

What was found:

- No gap this design could resolve. On these well-specified, single-turn hard tasks, Opus 4.8 with
  no help scored about the same as Fable 5 — and with three tasks at the ceiling and one run per
  cell, the design cannot resolve a difference of a point or two in either direction. The large
  capability gap expected going in did not show up here. This is the headline, and it is
  deliberately not flattering to the skill.
- The one real spread was on the open-ended task — "find every defect." Fable surfaced 13 issues,
  bare Opus 7 (it covered the most severe and stopped), and Opus-with-skill 15 (the widest coverage
  of any run). Where a task rewards not stopping early, differences show up; where a task has a
  single clean answer, everyone reaches it.
- Two of the clearest reasoning slips in the whole experiment were the strong model's own — Fable
  asserted a context-dependent risk as a flat certainty, and talked itself past an inconsistency
  that bare Opus decoded correctly. The discipline in this manual exists because these mistakes are
  general, not because the weaker model is worse.
- The skill did not raise the scores — with three of four tasks already at the ceiling and the rest
  inside what this design cannot resolve, there was no headroom to raise. What it changed was how
  the answers were written: every skill-loaded answer led with its verdict, labeled what it had
  verified versus what depended on unseen context, and named the check that would confirm each
  uncertain claim. None of the baselines did this consistently. It also broadened coverage on the
  open-ended hunt. Its one measurable cost: with a fixed length budget, more findings meant
  slightly shallower treatment of each.
- Three habits each showed up once in the pilot — a single attributable observation apiece, in
  sample, so evidence and not an established effect — and are what the calibration layer keeps:
  sweep for one more issue after the list feels done; check for risks that depend on context that
  is not shown; and attach the certainty label to the claim itself, not to a footnote.

### What this does not measure

Be skeptical in the right places. This is still four tasks; the pilot and the Sonnet cells are one
run per cell, and even the repeated cells are n=3 — enough to expose ±3 run-to-run spread, not to
give real statistics. The three original compensations were derived from the misses in the first
pass and then tested on the same four tasks — in sample by construction; the Sonnet 5 result is
the first evidence from outside the model they were derived on, but still on the same four tasks.
Every task was single-turn and fully specified — exactly the profile where a strong model needs
the least help. The tests could not touch the situations where a real difference is most likely to
live: long tasks where the thread drifts, work spread across many turns, deciding to check
something nobody asked about, and holding discipline under time or sunk-cost pressure. Read the
no-detectable-gap result as evidence about clean, single-shot analysis only.

The task set stays private for now — T1 embeds real private code, and keeping the set unpublished
keeps it uncontaminated as a regression check for future models. (T2 and T4 are fully synthetic
and could be released; that is on the list.) The method is fully reproducible on your own tasks —
that is what [`PROMPT.md`](PROMPT.md) Stage 2 is.

## The honest boundary

The manual transfers between models unchanged — it is craft, not weights. The calibration does not:
it is specific to your donor/recipient pair and your work, which is exactly why you measure it
instead of copying ours. If you build your own and skip the measurement, say so — an unmeasured
calibration is worse than a labeled absent one.
