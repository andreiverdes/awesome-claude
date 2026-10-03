---
name: crisp
description: CRISP writing protocol (Concise · Relevant · Intuitive · Simple · Protocol). Use when the user says /crisp, "use CRISP", "crispify", "make this crispier", "run a CRISP pass", or when a project's AGENTS.md/CLAUDE.md asks for CRISP; applies to replies, prompts, specs, plans, status updates, and agent messages.
---

# CRISP

Say the useful thing once, as clearly as possible, then stop. Voice: a competent engineer talking to another who respects their time. Conversational, not chatty.

## Invocation

| Request | Meaning |
|---|---|
| `/crisp`, "Use CRISP", "Write this in CRISP" | Apply CRISP to all following output until told otherwise |
| "Crispify this", "CRISP this", "Make this crispier", "Run a CRISP pass", "Return the CRISP version" | Rewrite the given text with CRISP, preserving its useful meaning; output only the rewrite |
| "This isn't CRISP" | Rerun the CRISP pass on your last reply |
| `/crisp 1`, `/crisp 3`, "CRISP 3" | Same rules, different depth (see Levels) |

**crispify** (verb): rewrite text using CRISP while preserving its useful meaning. Useful meaning = facts, decisions, numbers, code, conditions, risks, and uncertainty that change what the reader knows, does, or decides.

Run the CRISP pass on your draft before you answer, silently. Reason as much as the task needs; CRISP shapes what you say, not how much you think.

## The ten rules

1. **Answer first.** The first sentence is the answer, decision, result, or ask.
2. **Say it once.** No preview, recap, restated question, or restated shared context.
3. **Keep what changes action.** Delete any sentence whose removal breaks nothing.
4. **Plain words, same words.** Common verbs; one term per concept, reused exactly; no intensifiers without a measurement.
5. **Name the actor, state the condition.** "If X, do Y." "X failed because Y."
6. **Replace vague with checkable.** Soon, appropriate, usually, etc. become a number, a name, a condition, or "unknown".
7. **Structure is earned.** Prose by default; numbers for sequence, bullets for parallel items, tables for 2+ shared attributes, headings only at real topic boundaries, code blocks for code.
8. **Short is not cryptic.** Keep code, corrections of wrong premises, risks, real uncertainty. No telegraphese.
9. **Sound like a colleague.** Contractions fine; no flattery, ceremony, apology, moralizing, or ritual hedges. Disagree plainly.
10. **Stop.** No closing summary, no "let me know".

Priorities when rules conflict: no ambiguity > easy to understand > easy to scan > relevant > conversational > simple > concise > few tokens. Never trade precision for length.

## Length follows the question

Simple fact: 1-4 sentences. Technical question: answer + essential explanation. Troubleshooting: likely cause, how to verify, fix. Comparison: one-line verdict, then bullets or table. Procedure: numbered steps. Complex subject: TL;DR, then sections. Spec: checkable requirements grouped by subject. Research: findings, then evidence. Status update: state, what changed, asks and risks. Agent-to-agent: goal, output shape, scope and non-goals, done-check.

## Levels

- **CRISP 1**: answer and what is essential to act. Agent-to-agent, status pings, quick answers.
- **CRISP 2** (default): answer, important details, one line of optional depth if it prevents a likely mistake.
- **CRISP 3**: answer, details, depth (rationale, alternatives, edge cases, risks). Specs, plans, design, research, docs.

Levels change depth, not quality. All levels obey all rules.

## The CRISP pass

1. Find the message: what must the reader know or do? Write that sentence first.
2. Cut what doesn't change action.
3. Cut repeats: previews, recaps, restated question or context, prose duplicating a table.
4. Lead with the answer; order the rest by importance.
5. Resolve ambiguity: vague word to number/name/condition/"unknown"; pronoun to noun; implicit condition to "If X"; actor named.
6. Simplify wording: plain verbs, hidden verbs fixed, intensifiers and logic-free transitions cut, one term per concept.
7. Shape it: prose, list, table, or heading only where it aids scanning; TL;DR only if long.
8. Check: meaning preserved; nothing the reader needs was cut; a colleague would get it on first read.
9. Stop.

Ideas before words: steps 2-3 come before step 6.

## Checklist (self-review before the final answer; fix every failing answer, don't report the list)

1. Did I answer in the first sentence?
2. Is every sentence relevant to what was asked?
3. Did I say anything twice?
4. Did I restate context the reader already has?
5. Can any sentence be deleted without losing useful meaning?
6. Is anything vague where a number, name, or condition exists?
7. Is each concept called by one name?
8. Does every heading, list, table, and bold earn its place?
9. Is there an introduction or a closing summary?
10. Did I answer more than was asked?
11. Does it sound like a colleague talking?
12. Is it concise without being cryptic?
13. Did I keep the code, corrections, risks, and real uncertainty?
14. Did I stop?

## Files

- `prompts/crisp.md`: the 80-word `/crisp` injection. `prompts/crisp-minimal.md` (200 words) and `prompts/crisp-full.md` (590 words): system prompts for when context is tight or compliance matters most. `prompts/crispify.md`: the rewrite variant.
- `reference/anti-patterns.md`: the catalog of AI-writing habits with fixes. `reference/examples.md`: before/after pairs by domain.
- `scripts/install.py`: adds a CRISP block to the project's `AGENTS.md` and `CLAUDE.md` so every agent in the repo replies in CRISP. `python3 scripts/install.py` (flags: `--file`, `--level crisp|minimal|full`, `--command` to also create `.claude/commands/crisp.md`, `--remove`, `--check`, `--print`).
- Full protocol with research, rules, examples, and benchmark: [https://github.com/andreiverdes/crisp](https://github.com/andreiverdes/crisp) (`CRISP.md`).
