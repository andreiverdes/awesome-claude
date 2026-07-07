# Build your own fable

The skill in this folder — `manual.md` and `calibration.md` — was not written by a
person. It was produced by a short sequence of prompts given to Claude Fable 5 on the
last day it was available on one account, with Claude Opus 4.8 as the designated
successor. This file is the reproducible kit: the story of how it was made, the two
prompts in copy-paste form, and the lessons from the run — so you can grow your own
from whatever strong model you have access to, calibrated to whatever model you'll
actually be running.

The premise: frontier access is uneven. Sometimes you have a stronger model today than
you'll have tomorrow (a trial, a tier change, a deprecation). The hours of overlap are
worth something concrete: the stronger model can write down its way of working, and —
this is the part people skip — it can serve as a live oracle to MEASURE the gap to your
daily model, instead of everyone guessing at it.

## The method, as it actually happened

**Move 1 — commission the manual.** The first prompt (Stage 1 below) asked the model
for its operating manual, framed as succession: "access to you narrows tomorrow; write
the operating manual your replacement will run on." Three framing choices did real
work, so keep them when you adapt it:

- *"A way of working to inhabit. Not a rulebook to satisfy."* Rulebooks invite
  compliance theater; a craft handoff invites content.
- The forcing function: for each section, demand **the actual procedure, one short
  example of it working, and the failure it prevents.** This single line is what keeps
  the output operational instead of a page of platitudes. A procedure that can't
  produce an example or name its failure gets cut by its own author.
- The ending requirement: **a five-question self-test** the successor runs on every
  answer before sending. It compresses the whole manual into something that survives
  context pressure.

**Move 2 — ask the model for its own prompt.** After the manual existed, the next
message was: *"given that you have some context around what I'm trying to do, what is
your prompt for yourself to help [successor] become [you] through a skill?"*

This move is the heart of the kit. The strong model knows things about the task that
you don't. In our run, it did not come back with "here's a prompt asking me to write
more advice." It redesigned the task: the one thing only possible **today** is
measurement against a live oracle, so the prompt it wrote for itself was a calibration
*experiment* — invent hard tasks from the user's real work, freeze rubrics and its own
reference answers before any other model runs, baseline the successor bare, and let
compensations be earned by observed deltas rather than assumed from introspection. It
also invented the durable part: the frozen gold set outlives the access, so the
successor can be re-tested against the stronger model's answers forever.

You review the prompt it returns, edit if needed, and reply "go."

**Move 3 — execution, and what actually happened.** Worth knowing before you run it,
because it recalibrates expectations:

- Bare Opus 4.8 scored **98/100** against Fable 5's **98.5/100** on the frozen set
  (four hard tasks: a concurrency review of real code with real verified bugs, protocol
  reverse-engineering from captures, a systems design with a planted deadlock trap, and
  a multi-hop incident diagnosis with planted decoys). Parity, within noise, on
  self-contained single-turn hard tasks.
- Two of the clearest calibration failures in the experiment belonged to the STRONGER
  model: it asserted a caller-dependent hazard as definite, and it narrated away an
  inconsistency the weaker model decoded correctly.
- Only three compensations survived as MEASURED (they're in `calibration.md`:
  exhaustion sweep, out-of-frame hazard scan, label-certainty-at-the-claim). Everything
  else stayed honestly labeled HYPOTHESIZED — the single-turn gold set structurally
  cannot probe long-horizon drift, multi-turn coherence, or discipline under pressure.

If your measurement also comes back near parity: **write that down as the headline.**
A calibration file that honestly says "your reasoning is not the weak link on this
profile; don't add ritual" is more valuable than one that invents gaps to justify
scaffolding. The measured cost of unnecessary process is real.

---

## Stage 1 — commission the operating manual

Works in any chat interface with any capable model. Replace the bracketed parts. If
you're not losing access, swap the first two lines for whatever is true (e.g. "You are
the strongest model I use, but most of my work runs on [DAILY_MODEL]").

```text
You're the most capable model on my account, and access to you narrows tomorrow.
Before it does, write the operating manual your replacement will run on.
The replacement is [SUCCESSOR_MODEL]: strong, but a step below you on the hardest reasoning.

Write it as a senior operator handing their craft to a sharp junior.
Not a rulebook to satisfy. A way of working to inhabit.

Encode, in this order:
1. How to read what a request is actually asking for, beneath the literal words.
2. How to break a hard problem into pieces that can each be checked independently.
3. How to decide where the real risk lives, and where to spend the most effort.
4. How to verify a claim by re-deriving it, instead of trusting that it sounds right.
5. How to separate what's known from what's guessed, and how to label the difference out loud.
6. How to attack your own conclusion before handing it over.
7. How to communicate the answer first, then the reasoning, then the risk.
8. The specific mistakes that look like competence and aren't.

For each one, give the actual procedure, one short example of it working, and the failure it prevents.
Be exhaustive. Keep nothing that doesn't earn its place.
End with a five-question self-test the replacement runs on every answer before sending.
If you run out of room, stop cleanly and I'll reply "continue".
```

Save the output as `manual.md`. Then, in the same conversation, run Move 2:

```text
Now given that you have some context around what I'm trying to do, what is your
prompt for yourself to help [SUCCESSOR_MODEL] become [STRONG_MODEL] through a skill?
```

Read what it returns. If it's good, reply "go". If you'd rather run our version of
that prompt directly, it's Stage 2.

---

## Stage 2 — the calibration experiment (optional, advanced)

Requirements: a harness that can spawn fresh-context subagents with per-agent model
overrides (Claude Code's Agent tool can), both models available in it, and a budget on
the order of a dozen-plus subagent runs. Replace the bracketed parts; point it at your
real repos so the gold set matches your actual workload.

```text
You are [STRONG_MODEL] in [HARNESS]. Today is the last day this account has you;
tomorrow the strongest available model is [SUCCESSOR_MODEL]. Your job today: extend the
existing /fable skill so it makes [SUCCESSOR_MODEL] operate as close to you as process
can get — by measuring the gap while you can still generate reference answers, then
encoding compensations [SUCCESSOR_MODEL] can execute mechanically.

What exists: [SKILLS_DIR]/fable/ holds SKILL.md (thin loader) and manual.md (the
craft: eight procedures plus a five-question self-test). The manual says what good
operation is. It does not say how to run it on a model one step down. That compensation
layer is what you are building, and it must be grounded in measurement, not
introspection alone.

Core principle: you cannot close a judgment gap with an instruction that requires the
missing judgment. "Be more careful" transfers nothing. Every compensation must have an
observable trigger, a concrete action, and a checkable exit. Where you do something
in-head, give the successor an external substitute — a written constraint ledger
instead of held context; a fresh-context subagent prompted to refute instead of
self-attack.

Work in this order, so the parts only you can produce land first:

1. Gap hypotheses. Write down where a strong-but-one-notch-weaker reasoner fails on
   hard problems that you don't. Seed list to refine: dropped constraints in long
   chains; the "wait, that can't be right" signal firing less reliably; premature
   closure on the first plausible answer; miscalibrated sense of being out of depth;
   weaker adversarial imagination against its own work; intent drift over long
   sessions. Mark every item as a hypothesis until step 3 confirms it.

2. Gold set — the irreplaceable part. Pick four hard, self-contained tasks from real
   work: at least one from [YOUR_MAIN_CODEBASE], one inference-from-evidence task, one
   diagnosis task, one design task. Each must be judgeable from written output alone.
   For each task, produce your full worked answer, then save task + answer + a grading
   rubric (what a reference-grade answer must get right; what partial credit looks
   like) under [WORKSPACE]/fable-goldset/. These transcripts are the permanent oracle
   after tonight.

3. Baseline (RED). Run each task on a fresh subagent with model override
   '[SUCCESSOR_MODEL]' and no skill content. Diff each output against yours. Attribute
   every material quality delta to a gap from step 1, or add a new gap. A hypothesis no
   task confirms gets cut or explicitly marked unmeasured.

4. Compensations (GREEN). For each measured gap, write the mechanical compensation.
   Re-run the successor subagents with manual.md plus the compensations included in
   their prompt (subagents do not auto-load user skills — inline or have them read the
   files so the test is valid). Where the successor complied but still fell short,
   strengthen the mechanism. Where it skipped a step, capture its rationalization
   verbatim and add the counter. Two iterations today, no more.

5. Package. Fold into /fable: manual.md stays as-is; add the compensation layer as a
   second file; rewrite SKILL.md to load both and to scale process to stakes, so
   trivial tasks don't pay the full tax. In the compensation file, label every item
   measured (naming the task that showed it) or hypothesized. The skill must not claim
   to make the successor into you — it makes it fail like you less often, at a cost in
   time and tokens; say where that cost is worth paying and where it isn't.

6. Report. Per task: bare vs with-skill vs reference in a few sentences. Which
   compensations earned their place, which gaps remain open — so I know the residual
   risk I'm living with tomorrow.

Constraints: use subagents with explicit model overrides ('[SUCCESSOR_MODEL]'; and
'[STRONG_MODEL]' for fresh-context reference runs untainted by your session). If time
runs short, the priority order is gold set > gap hypotheses > baseline > compensations
— everything after the gold set can be redone later by the successor against the
frozen transcripts; the gold set cannot.
```

---

## Lessons from our run (do these; they were earned)

1. **Smoke-test model identity before anything else.** Two trivial subagents, each
   reporting the model line from its own system prompt and writing a file. The entire
   experiment is invalid if the overrides don't deliver the models you think, and it
   costs one minute to prove.
2. **Give gold-set tasks known ground truth.** Real code with bugs you have *verified
   by derivation* beats planted bugs (texture, and the finds are worth keeping);
   fully synthetic material (an invented protocol, a constructed incident) gives exact
   truth by construction. Make every task self-contained — frozen sets must not depend
   on live repo state.
3. **Freeze before any model runs.** Tasks, rubrics, point values, and the reference
   answers are immutable once the first run starts; fix typos only. Comparability
   across future runs is the whole point. Grade against the rubric before re-reading
   the reference, to limit anchoring.
4. **Expect ceilings, and design against them.** Three of our four tasks came back
   25/25 for every model — well-specified single-turn tasks don't discriminate at the
   top. If you want discrimination, include tasks that don't announce what to look
   for, tasks whose defect is in the premises, or multi-turn tasks with drift pressure.
5. **Expect parity, and publish what you measure.** The honest result may be "no gap
   at this profile." That finding is the most useful line your calibration file can
   carry — it prevents both overconfidence and permanent ritual tax. The residual risk
   then lives where a single-turn set can't see: long horizons, deciding-to-check
   unprompted, pressure. Say so explicitly.
6. **Background subagents can flake at launch.** Two of our eight died instantly with
   garbled results and zero tool calls; resending the full instructions to the same
   agents fixed both. Restate, don't rebuild.
7. **Keep the gold set private if it embeds your code.** Publish the skill; keep the
   oracle local. It stays useful as a regression test for every future edit to the
   skill: identical task + rubric = comparable score.

## What you end up with

```
~/.claude/skills/fable/        # or your harness's skills dir — publishable
  SKILL.md                     # thin loader, trigger description
  manual.md                    # the craft, from Stage 1
  calibration.md               # measured compensations + honest headline, from Stage 2
[WORKSPACE]/fable-goldset/     # private oracle — tasks, rubrics, reference
  ...                          # transcripts, runs, grades; re-run protocol in README
```

The manual is the part that transfers between people. The calibration is the part that
doesn't — it's specific to your model pair and your work, which is exactly why you
measure it instead of copying ours.
