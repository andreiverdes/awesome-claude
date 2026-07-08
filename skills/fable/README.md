# /fable — an operating manual for reasoning

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

## The honest boundary

The manual transfers between models unchanged — it is craft, not weights. The calibration does not:
it is specific to your donor/recipient pair and your work, which is exactly why you measure it
instead of copying ours. If you build your own and skip the measurement, say so — an unmeasured
calibration is worse than a labeled absent one.
