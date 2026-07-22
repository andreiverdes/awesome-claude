---
name: local-worker
description: Use when you want to offload well-bounded grunt work — codebase scouting, file summaries, docstrings, boilerplate, simple tests, mechanical/codemod edits — from Claude Code to a local model under LM Studio or Ollama, to cut frontier token usage. Triggers on "delegate to my local model", "use lm studio / ollama for this", "run it on the local LLM", "offload to local", "reduce tokens with a local sub-agent".
---

# local-worker

## Overview

Claude Code stays the orchestrator and hands bounded "dumb work" to a strictly-local coding agent (`pi`) pointed at a local model server (LM Studio or Ollama). One direction only: the local model drafts, Claude reviews — never the reverse. The delegated call is pinned to the local provider/model and runs under an isolated config with no frontier credentials, so it has no credentialed path to a paid model through pi (see [README.md](README.md) for the exact boundary).

## When to use

- Bounded, low-judgment work: scouting/grep synthesis, file/dir summaries, docstrings, boilerplate, simple tests, mechanical or codemod edits.
- You want the local GPU to absorb grunt work and keep frontier tokens for orchestration.

When NOT to use:
- Ambiguous, cross-cutting, or high-stakes work — keep that on Claude.
- Anything you won't verify — local output is draft quality.

## Prerequisites (one-time)

- `pi` CLI installed (`@earendil-works/pi-coding-agent`).
- A local server: LM Studio (`lms`) or Ollama (`ollama`).

See [README.md](README.md) for install and the strict-local rationale.

## Terms

- `<model-key>` — what you **load**: the model as listed by `lms ls` (LM Studio) or `ollama list` (Ollama).
- `<api-id>` — what you **call** via `pi --model`: LM Studio → `worker` (the `--identifier` set below); Ollama → the `ollama list` tag (e.g. `qwen2.5-coder:32b`).
- Backend → pi provider: `lms` → `lmstudio`; `ollama` → `ollama`.

## Procedure

### 0. Reuse if already configured

```bash
cat ~/.pi-worker/local-worker.json 2>/dev/null
```

If it exists and the user did not pass `--reconfigure`: read the saved backend/provider/model, run **Ensure engine up** (in step 2), then go to step 3. Otherwise run full Setup (steps 1–2).

### 1. Parse args

`[--backend lms|ollama] [--tools LIST] [--write] [--think] [--reconfigure] <task>`

Flags may appear anywhere. Everything else, in original order, is the task.

### 2. Setup — ASK, do not assume

Ask one question at a time and **wait for the user's answer** — never pick for them:

1. Backend — LM Studio or Ollama (skip if `--backend` given).
2. Model — enumerate, then let them pick one:
   - LM Studio: `lms ls`
   - Ollama: `ollama list`

**Ensure engine up** — the skill owns the worker's load config. `<model-key>` is the model picked in setup, or `modelKey` from saved state on reuse.

On Setup or `--reconfigure`, unload whatever is resident and load fresh with the skill's settings (a pre-existing GUI instance of the same model would otherwise double-load its weights and keep its own load config instead of the skill's):

```bash
# LM Studio  (provider: lmstudio · api-id: worker)
lms server start
lms unload --all 2>/dev/null
lms load "<model-key>" --gpu max --context-length 32768 --parallel 2 --identifier worker --ttl 1800 -y
```

On the reuse path (step 0), keep the warm worker; reload only if the ttl already unloaded it:

```bash
lms server start
curl -sf http://localhost:1234/v1/models | grep -q '"worker"' || \
  lms load "<model-key>" --gpu max --context-length 32768 --parallel 2 --identifier worker --ttl 1800 -y
```

Ollama (either path; loads the tag on first request):

```bash
# provider: ollama · api-id: the tag
curl -sf http://localhost:11434/api/tags >/dev/null || (ollama serve >/dev/null 2>&1 &)
for i in $(seq 1 30); do curl -sf http://localhost:11434/api/tags >/dev/null && break; sleep 1; done
```

`lms unload --all` reclaims the GPU for a clean, skill-defined worker — by design it also unloads any other models you had loaded in LM Studio. A fresh `lms load` uses LM Studio's default load settings, which may include KV-cache quantization: sliding-window MLX models throw under it (see Troubleshooting), so set K/V Cache Quantization to Off in LM Studio (or pick a standard-attention model).

Write the isolated, local-only config (no frontier credentials anywhere):

```bash
mkdir -p ~/.pi-worker
```

- `~/.pi-worker/models.json` — copy ONLY the chosen provider block from [models.example.json](models.example.json); set the model `id` to `<api-id>`. Do NOT create an `auth.json` with any frontier key.
- `~/.pi-worker/local-worker.json` — save the choice, including the load key so reuse can reload after a ttl unload, e.g. `{ "backend": "lms", "provider": "lmstudio", "model": "worker", "modelKey": "<model-key>" }` (for Ollama, `model` and `modelKey` are both the tag).

### 3. Compose the briefing (fresh, every delegation)

YOU write a 2–6 sentence system-prompt briefing per task, ≤150 words:
- a role tailored to this specific task;
- session context pi cannot discover from files (decisions/constraints from this conversation, what the user cares about now);
- expected output format and audience.

Name file paths — never paste file contents. Do not restate `AGENTS.md`/`CLAUDE.md`; pi discovers them. In scout mode, add one line: treat this as read-only — report, do not modify files.

### 4. Resolve the tool allowlist (explicit allowlist, never a denylist)

- `--tools <list>` → verbatim (`--tools read` = pure reader, no bash).
- `--write` → `read,bash,edit,write`.
- default (scout) → `read,bash` — explore and report. Note: bash can still write; the briefing is the guardrail. Use `--tools read` for mechanically read-only.

Thinking level: `--think` → `--thinking medium` (only meaningful if the configured model supports reasoning); otherwise `--thinking off`.

### 5. Delegate (strictly local)

```bash
env -u ANTHROPIC_API_KEY -u OPENAI_API_KEY -u GEMINI_API_KEY -u GOOGLE_API_KEY \
    -u GOOGLE_APPLICATION_CREDENTIALS -u OPENROUTER_API_KEY -u XAI_API_KEY \
    -u GROQ_API_KEY -u MISTRAL_API_KEY -u DEEPSEEK_API_KEY \
  PI_CODING_AGENT_DIR="$HOME/.pi-worker" \
  pi -p --provider <lmstudio|ollama> --model "<api-id>" \
     --tools <allowlist> --thinking <level> \
     --append-system-prompt "<briefing>" \
     "<task>"
```

- `--provider` is `lmstudio` for the `lms` backend, `ollama` for Ollama; `--model` is `<api-id>` (`worker`, or the Ollama tag).
- Use a Bash timeout of at least 300000 ms — the first call after a (re)load JIT-loads the model (~20s).
- What makes this local: `--provider`/`--model` pin the call to the local model (`-p` mode never switches models), the isolated `PI_CODING_AGENT_DIR` holds no frontier auth, and the `env -u …` scrub removes standing frontier keys so pi's built-in catalog can't resolve one. The scrub list covers the common providers — extend it to any provider key you actually hold. This is not a network firewall; see the README boundary.

### 6. After the run

- `--write`: always run `git diff --stat`, summarize what the local model changed, and recommend `git diff` review before committing.
- Present pi's final answer to the user.
- If pi exits non-zero or reports the provider/model unavailable: relay the error verbatim and do NOT auto-retry — the engine is likely down. Re-run **Ensure engine up**, or `--reconfigure`.

## Model strategy

- Use one fast, non-reasoning coder as the worker (a Qwen coder / agent-tuned model like Qwen3-Coder or Devstral) — boilerplate, docstrings, summaries, simple edits. Keep tasks short and self-contained.
- Tool-calling reliability varies widely and does NOT track reputation — benchmark a candidate with one small tool task (a single `ls` + report) before trusting it. Some well-regarded models loop and never return; a bigger agent-tuned coder often beats a smaller general one on both speed and reliability.
- One direction only: local drafts, Claude reviews — never the reverse.

## Extension points

The tool-specific steps — enumerate models, start engine, wire config, delegate — are the adapter seam. This skill ships the `pi` adapter.

- Another coding tool (e.g. `opencode`): research its headless `run` / `--model` and `OPENCODE_CONFIG` provider wiring; keep the same isolated, local-only, env-scrubbed pattern.
- A second escalation tier (a resident reasoning model): register a second `models[]` entry and load it under its own `--identifier` (LM Studio) or tag (Ollama), then select it per call. Left out of v1 to keep one worker resident and RAM predictable.

## Common mistakes

| Mistake | Fix |
|--------|-----|
| Pasting file contents into the briefing | Name paths; pi reads them itself. |
| Re-reading the full diff to verify (defeats the token savings) | Trust for bounded tasks; add a test/build gate before trusting `--write` broadly. |
| Delegating ambiguous or high-stakes work | Keep judgment on Claude; local is draft-only. |
| Assuming "strictly local" without the env scrub | pi resolves frontier keys straight from your shell env even under an isolated dir — keep `env -u …`. |
| Reusing later and hitting an unloaded/absent model | Always run **Ensure engine up** on the reuse path, not just first-run. |
| Auto-retrying on an "unavailable" error | The engine is down. Bring it up, don't loop. |
| Using a reasoning / "thinking" model as the worker | It generates reasoning tokens at every step of the tool loop and is slow (a multi-file scout can blow past minutes). Use a fast non-reasoning coder. |

## Troubleshooting

| Symptom | Cause and fix |
|---------|---------------|
| `NotImplementedError: RotatingKVCache Quantization NYI` (pi exits 1) | The model uses a sliding-window (rotating) KV cache and LM Studio has KV-cache quantization enabled — unimplemented for rotating caches. Short prompts pass; real agentic prompts rotate the cache and throw. Fix: in LM Studio set K/V Cache Quantization to Off (F16) in the model's load settings and reload — `lms load` has no flag for this. Or pick a standard-attention model. |
| Delegation runs for minutes with no output | Worker is a reasoning model (see Common mistakes), or the task needs too many tool turns. Use a non-reasoning coder and keep tasks small. |
| First call after a (re)load is slow (~20s) | JIT model load. Keep the Bash timeout ≥ 300000 ms. |
