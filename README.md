# awesome-claude

A collection of open-source skills for Claude Code.

## Install

```bash
claude plugins add github:<your-user>/awesome-claude
```

All skills become available immediately.

## Skills

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
| `/claude-config-backup` | Set up a portable, auto-syncing backup of your Claude Code configuration (skills, settings, memories) as a GitHub repo. |
| `/config-export` | Manually snapshot your current Claude Code config to the backup repo. |
| `/config-restore` | Restore Claude Code config on a new machine with interactive path remapping. |

## Contributing

PRs welcome. Each skill lives in `skills/<skill-name>/SKILL.md`. See the [agentskills.io spec](https://agentskills.io/specification) for the skill format.
