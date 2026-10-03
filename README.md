# awesome-claude

A collection of open-source skills for Claude Code.

## Install

```bash
claude plugins marketplace add andreiverdes/awesome-claude
claude plugins install awesome-claude@awesome-claude
```

The skills become available in your next Claude Code session. Update later with
`claude plugins marketplace update awesome-claude`.

## Skills

### Reasoning Discipline

| Skill | Description |
|-------|-------------|
| [`/fable`](skills/fable/README.md) | An operating manual for reasoning, written by Claude Fable 5 as a handoff of craft to successor models: eight procedures that replace the feeling of being right with checks, a five-question pre-send self-test, and a calibration layer grounded in a small self-graded pilot rather than assumed — on four single-turn hard tasks, Opus 4.8 with no skill showed no gap the pilot could resolve, with three (n=1) compensations for the gaps that did appear. |

Usage for both paths — installing and using the skill, the no-code Claude Project route, and building your own with runnable samples — is in [`skills/fable/README.md`](skills/fable/README.md).

### Writing & Communication

| Skill | Description |
|-------|-------------|
| [`/crisp`](skills/crisp/SKILL.md) | A writing protocol for humans and LLMs: say the useful thing once, as clearly as possible, then stop. Ten checkable rules, three depth levels, a crispify pass, and an installer that puts the directive in `AGENTS.md`/`CLAUDE.md`. Benchmarked blind against a no-prompt baseline on 10 prompts × 3 samples: −47% tokens, 21/30 pairings won, 97% of required facts kept ([dashboard](https://andreiverdes.github.io/crisp/), [full protocol + research](https://github.com/andreiverdes/crisp)). |

### App Development

| Skill | Description |
|-------|-------------|
| `/mobile-app-builder` | Production-ready mobile app scaffolding (iOS, Android, cross-platform). Covers SwiftUI, Jetpack Compose, Flutter, Compose Multiplatform, and Expo + HeroUI. Includes validation, onboarding, monetization, and go-to-market strategy. |
| `/web-dev` | Full-stack web development assistant. React, Vue, Next.js, APIs, design-to-code conversion. |

### UI & Design

| Skill | Description |
|-------|-------------|
| `/shadcn` | Build UIs with shadcn/ui and Tailwind CSS. |
| `/shadcn-dashboard-template` | Dashboard and landing page templates with shadcn. |

### IDE & Tooling

| Skill | Description |
|-------|-------------|
| `/intellij-plugin` | IntelliJ platform plugin development guide. |

### Architecture & Documentation

| Skill | Description |
|-------|-------------|
| `/mosby` | Turn any codebase into an interactive 3D architecture visualization — a Three.js city where buildings are components, traffic is flows, with a toggle to a clean UML-style diagram. Ships a complete working template (dual themes, flow player, city/diagram modes) plus the recon → content model → adapt → browser-verify workflow. Single self-contained HTML, zero network. |

### Claude Code Config

| Skill | Description |
|-------|-------------|
| `/git-sync` | Turn `~/.claude` into a git repo with auto-sync. Full setup guide for portable config across machines. |
| `/sync` | One command to sync config: commit local + pull remote + rebase + push. |

### Local Inference & Cost

| Skill | Description |
|-------|-------------|
| [`/local-worker`](skills/local-worker/README.md) | Offload bounded grunt work (scouting, summaries, docstrings, mechanical edits) from Claude Code to a local model under LM Studio or Ollama via the `pi` agent — cutting frontier tokens. The worker runs strictly local: isolated config, pinned provider, scrubbed environment, no frontier credentials. |

## Contributing

PRs welcome. Each skill lives in `skills/<skill-name>/SKILL.md`. See the [agentskills.io spec](https://agentskills.io/specification) for the skill format.
