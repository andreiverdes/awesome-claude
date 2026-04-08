---
name: claude-config-backup
description: Use when the user wants to back up, sync, or make portable their Claude Code configuration (skills, settings, memories) across machines. Triggers on mentions of backing up claude config, syncing settings, new machine setup, dotfiles for claude, or portable claude configuration.
---

# Claude Config Backup

Turn `~/.claude` into a git repo that auto-syncs your configuration across machines.

## When to Use

- User wants to back up their Claude Code config
- User is setting up a new machine and needs to restore their setup
- User wants to sync config across multiple machines

## Architecture

`~/.claude` IS the git repo. A whitelist `.gitignore` tracks only what matters:

| Tracked | Not tracked |
|---------|-------------|
| `settings.json` | `history.jsonl`, `sessions/` |
| `keybindings.json` | `cache/`, `image-cache/`, `plugins/` |
| `skills/**` | `tasks/`, `todos/`, `telemetry/` |
| `projects/*/memory/**` | Session jsonl, UUID dirs, subagents |
| `CLAUDE.md` | Everything else |
| `hooks/` | |

## Setup Process

### Step 1: Init git in ~/.claude

```bash
cd ~/.claude && git init
```

### Step 2: Create whitelist .gitignore

```gitignore
# Ignore everything
*

# Track these top-level files
!.gitignore
!CLAUDE.md
!settings.json
!keybindings.json

# Track hooks
!hooks/
!hooks/**

# Track all skills
!skills/
!skills/**

# Track only project memory dirs
!projects/
!projects/*/
!projects/*/memory/
!projects/*/memory/**
```

**Important:** Use explicit `git add` for the initial commit since the whitelist gitignore needs directory traversal help:

```bash
git add .gitignore CLAUDE.md settings.json keybindings.json 2>/dev/null
git add skills/ hooks/ 2>/dev/null
for d in projects/*/memory; do [ -d "$d" ] && git add "$d"; done
```

After the initial commit, `git add -A` works correctly.

### Step 3: Initial commit

```bash
git commit -m "initial config backup"
```

### Step 4: Wire Stop hook for auto-sync

Add to `~/.claude/settings.json` under `hooks.Stop` (append, never replace):

```json
{
  "hooks": [
    {
      "type": "command",
      "command": "cd $HOME/.claude && git add -A && (git diff --cached --quiet || git commit -m \"auto-sync $(hostname) $(date +%Y-%m-%d-%H%M)\" -q) && git push -q 2>/dev/null || true &"
    }
  ]
}
```

This runs silently in the background after every session.

### Step 5: Create config skills

Create three skills for manual control:

- `/config-push` — `git add -A && commit && push` (save current state)
- `/config-pull` — `git pull --rebase` (get remote changes)
- `/config-sync` — commit + pull --rebase + push (bidirectional merge)

### Step 6: (Optional) Skill-sync hook for public repo

If the user has a public skills repo (e.g., `awesome-claude`), create a PostToolUse hook on Write|Edit that:
1. Checks if the written file is under `~/.claude/skills/`
2. If the skill is new/updated in the public repo, prompts the user

### Step 7: Connect to remote

Tell the user to create a GitHub repo and push:

```bash
cd ~/.claude
git remote add origin git@github.com:<user>/claude-config.git
git push -u origin main
```

## New Machine Restore

```bash
# Clone into ~/.claude (must be empty or non-existent)
git clone git@github.com:<user>/claude-config.git ~/.claude

# Install plugins (not tracked by git)
claude plugins add ...
```

Skills and memories are immediately available. Settings are already in place.

## Commands

| Command | What it does |
|---------|-------------|
| `/config-push` | Commit + push local changes |
| `/config-pull` | Pull remote changes |
| `/config-sync` | Full bidirectional sync (commit + rebase + push) |
| Stop hook | Auto-pushes after every session |

## Common Issues

| Issue | Fix |
|-------|-----|
| Push fails (no remote) | `git remote add origin <url>` in `~/.claude` |
| Push fails (remote ahead) | Run `/config-sync` to rebase first |
| New machine has different paths | Project memory dirs will have different path-encoded names — that's OK, each machine adds its own |
| `git add -A` picks up junk | Check `.gitignore` whitelist — the `*` at top must be present |
