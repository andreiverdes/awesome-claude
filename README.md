# awesome-claude

A collection of open-source skills for Claude Code.

## Install

```bash
claude plugins add github:andreiverdes/awesome-claude
```

All skills become available immediately.

## Skills

### Reasoning Discipline

| Skill | Description |
|-------|-------------|
| `/fable` | An operating manual for reasoning, written by Claude Fable 5 as a handoff of craft to successor models: eight procedures that replace the feeling of being right with checks, a five-question pre-send self-test, and a calibration layer measured (not assumed) against a frozen gold set — Opus 4.8 baselined at parity on single-turn hard tasks, with three measured compensations for the gaps that did appear. |

Not on Claude Code? Load `/fable`'s manual without the plugin: paste [`skills/fable/manual.md`](skills/fable/manual.md) into a Claude Project's instructions and set the Project's model, or load it as a system prompt over the API with [`skills/fable/fable_to_opus.py`](skills/fable/fable_to_opus.py).

Rather grow your own than use this one? [`skills/fable/PROMPT.md`](skills/fable/PROMPT.md) is the reproducible prompt kit that produced this skill — run it against whatever strong model you have, calibrated to whatever model you keep.

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

## Contributing

PRs welcome. Each skill lives in `skills/<skill-name>/SKILL.md`. See the [agentskills.io spec](https://agentskills.io/specification) for the skill format.
