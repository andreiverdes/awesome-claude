# /fable — an operating manual for reasoning

## TL;DR (plain version)

`/fable` is a set of working habits you hand to an AI so it reasons more like a careful expert and
less like a confident guesser. Think of it as the operating procedures a senior person writes down
for a sharp junior — except here the junior is the AI model.

It was written by one of Anthropic's strongest models (Claude Fable 5) describing how it actually
works through a hard problem, so any model can run on those same habits. Models get replaced every
few months; a way of thinking, once written down, doesn't.

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
answer, and a calibration layer that was measured — not assumed — against a frozen gold set. It was
written by Claude Fable 5 as a handoff of craft to the models that come after it.

Measured headline: on self-contained, single-turn hard tasks, Claude Opus 4.8 scored 98/100 against
Fable 5's 98.5 — parity within noise. So the skill's value is not raising a weak model's ceiling; it
is hygiene, calibration, and honesty about where a real gap does and doesn't exist. Full detail is
in [`calibration.md`](calibration.md).

## Files

| File | What it is |
|------|-----------|
| `SKILL.md` | The loader — trigger description plus "read the manual, apply it, run the self-test". |
| `manual.md` | The eight procedures and the five-question pre-send self-test. |
| `calibration.md` | The measured layer for running the manual on Opus 4.8: the parity headline, three compensations, and residual risk. |
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

The calibration in this skill is a measurement, not a claim. The setup and the result follow.

### How it was tested

A set of four hard, self-contained tasks were used, each paired with a grading rubric and a known
answer written before any model saw it:

- a concurrency-and-correctness review of real code (find every defect);
- a protocol reverse-engineering task from a captured trace, with an exact, generated ground truth;
- a systems-design task under ten hard constraints, with a deadlock trap planted where two of the
  constraints collide;
- a multi-hop incident diagnosis with one real root cause and three plausible decoys planted to
  mislead.

Each task was run three ways, each in a fresh context with no memory of the others: Claude Fable 5
(the reference answer), Claude Opus 4.8 with no skill (the baseline), and Opus 4.8 with this skill's
manual loaded. Every run was graded blind against the frozen rubric — baselines before references,
to avoid anchoring — and each run's identity was confirmed up front by having the model report which
model it was before starting.

### The scores

| Task | Fable 5 (reference) | Opus 4.8, no skill | Opus 4.8 + /fable |
|------|:---:|:---:|:---:|
| Concurrency review | 23.5 | 23 | 22 |
| Protocol inference | 25 | 25 | 25 |
| Systems design | 25 | 25 | 25 |
| Incident diagnosis | 25 | 25 | 25 |
| **Total (/100)** | **98.5** | **98** | **97** |

### What was found

- Near-parity. On these well-specified, single-turn hard tasks, Opus 4.8 with no help scored within
  noise of Fable 5. The large capability gap expected going in did not appear at this profile.
  This is the headline, and it is deliberately not flattering to the skill.
- The one real spread was on the open-ended task — "find every defect." Fable surfaced 13 issues,
  bare Opus 7 (it covered the most severe and stopped), and Opus-with-skill 15 (the widest coverage
  of any run). Where a task rewards not stopping early, differences show up; where a task has a
  single clean answer, everyone reaches it.
- Two of the clearest reasoning slips in the whole experiment were the strong model's own — Fable
  asserted a context-dependent risk as a flat certainty, and talked itself past an inconsistency
  that bare Opus decoded correctly. The discipline in this manual exists because these mistakes are
  general, not because the weaker model is worse.
- The skill did not raise the scores — with three of four tasks already at the ceiling and the rest
  inside noise, there was no headroom to raise. What it changed, measurably, was how the answers
  were written: every skill-loaded answer led with its verdict, labeled what it had verified versus
  what depended on unseen context, and named the check that would confirm each uncertain claim. None
  of the baselines did this consistently. It also broadened coverage on the open-ended hunt. Its one
  measurable cost: with a fixed length budget, more findings meant slightly shallower treatment of
  each.
- Three habits earned their place by showing a measured effect, and are what the calibration layer
  keeps: sweep for one more issue after you think you are done; check for risks that depend on
  context you cannot see; and attach the certainty label to the claim itself, not to a footnote.

### What this does not measure

Be skeptical in the right places. This was four tasks, one run per cell, so a gap of a point or two
is noise, not signal. Every task was single-turn and fully specified — exactly the profile where a
strong model needs the least help. The tests could not touch the situations where a real difference
is most likely to live: long tasks where the thread drifts, work spread across many turns, deciding
to check something nobody asked about, and holding discipline under time or sunk-cost pressure. Read
the near-parity result as evidence about clean, single-shot analysis only.

The task set itself stays private (it embeds real code), so it is kept as an internal regression
check rather than published. The method is fully reproducible on your own tasks — that is what
[`PROMPT.md`](PROMPT.md) Stage 2 is.

## The honest boundary

The manual transfers between models unchanged — it is craft, not weights. The calibration does not:
it is specific to your donor/recipient pair and your work, which is exactly why you measure it
instead of copying ours. If you build your own and skip the measurement, say so — an unmeasured
calibration is worse than a labeled absent one.
