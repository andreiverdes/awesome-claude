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
was small. So treat `/fable` as consistency-and-honesty insurance, not as a way to make a weak model
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

Install the collection as a Claude Code plugin:

```bash
claude plugins add github:andreiverdes/awesome-claude
```

Then `/fable` activates on its own before hard or high-stakes work — the start of a difficult task,
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

The calibration in this skill rests on a small measurement, not on assertion. The setup, the result,
and the conflicts of interest follow.

### How it was tested

A set of four hard, self-contained tasks were used, each paired with a grading rubric and a known
answer fixed before any model ran:

- a concurrency-and-correctness review of real code (find every defect);
- a protocol reverse-engineering task from a captured trace, with an exact, generated ground truth;
- a systems-design task under ten hard constraints, with a deadlock trap planted where two of the
  constraints collide;
- a multi-hop incident diagnosis with one real root cause and three plausible decoys planted to
  mislead.

Each task was run three ways, each in a fresh context with no memory of the others: Claude Fable 5
(the reference answer), Claude Opus 4.8 with no skill (the baseline), and Opus 4.8 with this skill's
manual loaded. The runs happened inside the Claude Code agent, so its own system prompt and tools
were present in every arm — "no skill" means no skill content, not a bare model.

Conflicts of interest, stated plainly: Claude Fable 5 wrote the tasks, the rubrics, the ground
truth, and the manual under test — and then graded every run, including its own reference answer and
the run of the skill it had authored. Two things limit that conflict without removing it: the
rubrics were frozen with fixed point values before any model ran, and each run was scored before its
reference answer was re-read (an anchoring control). That the model overrides really delivered
Fable 5 and Opus 4.8 was checked beforehand with separate identity probes, not by anything in the
runs themselves. Read the numbers below as a self-graded pilot; an independent re-grade by a
different model is the obvious next step.

### The scores

| Task | Fable 5 (reference) | Opus 4.8, no skill | Opus 4.8 + /fable |
|------|:---:|:---:|:---:|
| Concurrency review | 23.5 | 23 | 22 |
| Protocol inference | 25 | 25 | 25 |
| Systems design | 25 | 25 | 25 |
| Incident diagnosis | 25 | 25 | 25 |
| **Total (/100)** | **98.5** | **98** | **97** |

Three of the four tasks scored 25/25 for every model — there, the rubric's ceiling set the top, not
the models. Only the open-ended concurrency review separated the runs at all. So the /100 totals
mostly average tied tasks; the per-task column is the honest view, and any model at or above the
rubric author's level is clamped to 25 by construction.

### What was found

- No gap this design could resolve. On these well-specified, single-turn hard tasks, Opus 4.8 with
  no help scored about the same as Fable 5 — and with three tasks at the ceiling and one run per
  cell, the design cannot resolve a difference of a point or two in either direction. The large
  capability gap expected going in did not show up here. This is the headline, and it is deliberately
  not flattering to the skill.
- The one real spread was on the open-ended task — "find every defect." Fable surfaced 13 issues,
  bare Opus 7 (it covered the most severe and stopped), and Opus-with-skill 15 (the widest coverage
  of any run). Where a task rewards not stopping early, differences show up; where a task has a
  single clean answer, everyone reaches it.
- Two of the clearest reasoning slips in the whole experiment were the strong model's own — Fable
  asserted a context-dependent risk as a flat certainty, and talked itself past an inconsistency
  that bare Opus decoded correctly. The discipline in this manual exists because these mistakes are
  general, not because the weaker model is worse.
- The skill did not raise the scores — with three of four tasks already at the ceiling and the rest
  inside what this design cannot resolve, there was no headroom to raise. What it changed was how the
  answers
  were written: every skill-loaded answer led with its verdict, labeled what it had verified versus
  what depended on unseen context, and named the check that would confirm each uncertain claim. None
  of the baselines did this consistently. It also broadened coverage on the open-ended hunt. Its one
  measurable cost: with a fixed length budget, more findings meant slightly shallower treatment of
  each.
- Three habits each showed up once in the pilot — a single attributable observation apiece, in
  sample, so evidence and not an established effect — and are what the calibration layer keeps: sweep
  for one more issue after the list feels done; check for risks that depend on context that is not
  shown; and attach the certainty label to the claim itself, not to a footnote.

### What this does not measure

Be skeptical in the right places. This was four tasks, one run per cell, with no repeated runs — so
there is no error estimate here, and a gap of a point or two is below what this design can resolve,
not signal. The three compensations were derived from the misses in the first pass and then tested
on the same four tasks — in sample by construction. The one model pair measured is Fable 5 to
Opus 4.8; the cheaper models the skill is actually pitched to help are untested. Every task was
single-turn and fully specified — exactly the profile where a strong model needs the least help. The
tests could not touch the situations where a real difference is most likely to live: long tasks
where the thread drifts, work spread across many turns, deciding to check something nobody asked
about, and holding discipline under time or sunk-cost pressure. Read the no-detectable-gap result as
evidence about clean, single-shot analysis only.

The task set stays private for now — one task embeds real private code, and keeping the set
unpublished keeps it uncontaminated as a regression check for future models. (Two of the four, the
protocol task and the incident diagnosis, are fully synthetic and could be released; that is on the
list.) The method is fully reproducible on your own tasks — that is what [`PROMPT.md`](PROMPT.md)
Stage 2 is.

## The honest boundary

The manual transfers between models unchanged — it is craft, not weights. The calibration does not:
it is specific to your donor/recipient pair and your work, which is exactly why you measure it
instead of copying ours. If you build your own and skip the measurement, say so — an unmeasured
calibration is worse than a labeled absent one.
