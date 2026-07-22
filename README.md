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
