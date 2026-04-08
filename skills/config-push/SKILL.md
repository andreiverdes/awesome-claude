---
name: config-push
description: Use when the user wants to push their current Claude Code config (settings, skills, memories) to the remote repo from ~/.claude.
---

# Config Push

Commits and pushes current `~/.claude` config changes to the remote repo.

## When to Use

- Saving current config state to the remote
- After making skill/settings/memory changes you want backed up
- The Stop hook runs this automatically, but you can trigger it manually

## Steps

### 1. Check for changes

```bash
cd ~/.claude && git status --short
```

If no changes, report "Nothing to push" and stop.

### 2. Stage and commit

```bash
cd ~/.claude
git add -A
git commit -m "config push $(hostname) $(date +%Y-%m-%d-%H%M)"
```

### 3. Push

```bash
git push
```

If push fails due to remote changes, suggest running `/config-sync` instead.

### 4. Report

Show what was pushed:
```bash
git diff HEAD~1 --stat
```
