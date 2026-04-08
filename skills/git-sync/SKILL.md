---
name: git-sync
description: Use when the user wants to set up portable Claude Code configuration — turning ~/.claude into a git repo that auto-syncs settings, skills, and memories across machines. Triggers on backing up claude config, syncing settings, new machine setup, dotfiles for claude, portable configuration.
---

# Dotfiles

Turn `~/.claude` into a git repo that auto-syncs your configuration across machines.

## When to Use

- User wants to back up their Claude Code config
- Setting up a new machine
- Syncing config across multiple machines

## What Gets Tracked

| Tracked | Not tracked |
|---------|-------------|
| `settings.json`, `keybindings.json` | `history.jsonl`, `sessions/` |
| `skills/**` | `cache/`, `plugins/` |
| `projects/*/memory/**` | Session data, UUID dirs |
| `CLAUDE.md`, `hooks/` | `tasks/`, `todos/`, `telemetry/` |

## Setup

### 1. Init git

```bash
cd ~/.claude && git init
```

### 2. Create whitelist .gitignore

```gitignore
*
!.gitignore
!CLAUDE.md
!settings.json
!keybindings.json
!hooks/
!hooks/**
!skills/
!skills/**
!projects/
!projects/*/
!projects/*/memory/
!projects/*/memory/**
```

### 3. Initial commit

Explicit add for the first commit (whitelist gitignore needs help on first run):

```bash
git add .gitignore CLAUDE.md settings.json keybindings.json 2>/dev/null
git add skills/ hooks/ 2>/dev/null
for d in projects/*/memory; do [ -d "$d" ] && git add "$d"; done
git commit -m "initial config backup"
```

After this, `git add -A` works correctly.

### 4. Auto-sync Stop hook

Add to `hooks.Stop` in `~/.claude/settings.json` (append, never replace):

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

### 5. Connect remote

```bash
cd ~/.claude
git remote add origin git@github.com:<user>/claude-config.git
git push -u origin main
```

## New Machine

```bash
git clone git@github.com:<user>/claude-config.git ~/.claude
claude plugins add ...   # reinstall plugins
```

Done. Skills, settings, and memories are all in place.

## Manual sync

Use `/sync` anytime to commit + pull + push.
