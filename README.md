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
| `/claude-config-backup` | Turn `~/.claude` into a git repo with auto-sync. Full setup guide for portable config across machines. |
| `/config-push` | Commit and push current config changes to remote. |
| `/config-pull` | Pull config changes from remote (from another machine). |
| `/config-sync` | Bidirectional sync: commit local + pull remote + rebase + push. |

## Contributing

PRs welcome. Each skill lives in `skills/<skill-name>/SKILL.md`. See the [agentskills.io spec](https://agentskills.io/specification) for the skill format.
