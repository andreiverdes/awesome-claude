# /local-worker — delegate grunt work to a strictly-local model

Claude Code stays the orchestrator; well-bounded "dumb work" gets handed to a local model running on
your own machine, so frontier tokens go to the thinking instead of the grunt work.

## TL;DR

`/local-worker <task>` sends a bounded task — scouting a codebase, summaries, docstrings, boilerplate,
mechanical edits — to the [`pi`](https://github.com/badlogic/pi-mono) agent pointed at a local model
served by [LM Studio](https://lmstudio.ai) or [Ollama](https://ollama.com). Claude writes the briefing
and reviews the result. The worker runs **strictly local**: the call is pinned to the local model, its
config carries no frontier credentials, and its environment is scrubbed of frontier API keys — so it
has no credentialed path to a paid model through pi. (It is not a network firewall — see the Honest
boundary below.)

First run asks which backend and model to use, brings up the inference engine, and wires everything;
later runs reuse that setup.

## Why strictly local

Routers/proxies that repoint Claude Code's model endpoint corrupt tool calls and need API-key billing;
Claude Code subagents can't target another provider ([anthropics/claude-code#38698](https://github.com/anthropics/claude-code/issues/38698)).
The pattern that works: the frontier model composes a briefing and shells out to a local executor that
speaks its own protocol natively. This skill adapts that approach (the
[`local-llm`/`pi-local`](https://github.com/yorrick/claude-code-plugins/pull/17) pattern) and hardens
the isolation so "local only" is enforced by construction, not by a sentence in a prompt.

"Strictly local" is three layers:

1. **Isolated config** — the worker runs under `PI_CODING_AGENT_DIR=~/.pi-worker`, whose `models.json`
   defines only the local provider. No `auth.json` with a frontier key.
2. **Pinned provider/model** — every call passes `--provider <local> --model <local-id>`; in `-p` mode
   there is no model switching.
3. **Scrubbed environment** — `env -u ANTHROPIC_API_KEY …` at launch, because `pi` would otherwise
   resolve a frontier key straight from your shell env even under an isolated config dir. This is the
   layer most setups miss.

**Honest boundary:** this blocks credentialed frontier access through `pi`'s config/auth/env paths. It
is **not** a network firewall — it does not stop a tool that curls an API directly or a hand-set proxy
`baseUrl`. A filesystem/network jail (worktree or container) is a separate concern, out of scope here.

## Prerequisites

```bash
# pi
npm install -g @earendil-works/pi-coding-agent

# one local server
#   LM Studio: https://lmstudio.ai  (ships the `lms` CLI; MLX + llama.cpp engines)
#   Ollama:    https://ollama.com
```

No `~/.pi-worker` config is needed up front — the skill creates it on first run from
[`models.example.json`](models.example.json).

## Use

```
/local-worker list the test functions in chat_app/tests and what each verifies
/local-worker --tools read summarize what main.py does
/local-worker --write add docstrings to chat_app/main.py
/local-worker --backend ollama --think find race conditions in the websocket layer
/local-worker --reconfigure            # re-pick backend/model
```

Modes:

- **scout (default)** — `--tools read,bash`: explore and report; edit/write are off.
- **`--write`** — expands to `read,bash,edit,write`; Claude shows `git diff --stat` afterward.
- **`--tools <list>`** — your own allowlist (`--tools read` = pure reader, no bash).

## Tools & backends

| | LM Studio | Ollama |
|---|---|---|
| **pi** | shipped | shipped |
| **opencode** | extension point | extension point |

`pi` is the shipped adapter. The tool-specific steps (enumerate models, start engine, wire config,
delegate) are a clean seam so an `opencode` adapter can drop in later without reworking the flow.

## Reducing permission prompts

The skill shells out to `pi`, `lms`, and `ollama`. To avoid a prompt each time, allowlist them in your
Claude Code settings (or run the `fewer-permission-prompts` skill).

## Files

| File | What it is |
|------|-----------|
| `SKILL.md` | The procedure Claude follows: reuse-or-setup, briefing, allowlist, delegate, review. |
| `models.example.json` | The `pi` provider templates for LM Studio and Ollama — copy one block into `~/.pi-worker/models.json`. |
