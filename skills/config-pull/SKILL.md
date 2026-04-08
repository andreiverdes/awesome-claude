---
name: config-pull
description: Use when the user wants to pull Claude Code config changes from the remote repo into ~/.claude. Pulls settings, skills, and memories pushed from another machine.
---

# Config Pull

Pulls remote config changes into `~/.claude` without overwriting local-only files.

## When to Use

- Setting up a new machine after cloning the config repo
- Pulling changes another machine pushed

## Steps

### 1. Verify git repo

```bash
cd ~/.claude && git remote -v
```

If no remote is set, ask the user for the repo URL and set it:
```bash
git remote add origin <url>
```

### 2. Pull

```bash
cd ~/.claude && git pull --rebase
```

`--rebase` replays any local commits on top of remote changes, keeping history clean.

### 3. Handle conflicts

If rebase reports conflicts:
1. Show the conflicting files
2. For each conflict, show both versions and ask the user which to keep
3. After resolving: `git rebase --continue`

### 4. Report

Show what changed:
```bash
git diff HEAD~1 --stat
```
