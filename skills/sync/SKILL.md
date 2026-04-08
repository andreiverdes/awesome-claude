---
name: sync
description: Use when the user wants to sync their Claude Code config (settings, skills, memories) with the remote repo. One command that commits local changes, pulls remote changes, rebases, and pushes.
---

# Git Sync

Syncs `~/.claude` with the remote repo. Commits local, pulls remote, pushes result. One command.

## Steps

### 1. Check repo

```bash
cd ~/.claude && git remote -v
```

If no remote, ask the user for the repo URL:
```bash
git remote add origin <url>
```

### 2. Commit local changes

```bash
cd ~/.claude
git add -A
git diff --cached --quiet || git commit -m "sync $(hostname) $(date +%Y-%m-%d-%H%M)"
```

### 3. Pull + rebase

```bash
git pull --rebase
```

If conflicts:
1. Show conflicting files
2. For `settings.json` — show diff, ask which to keep
3. For `memory/*.md` — keep both versions if different files, ask if same file
4. For `skills/**` — show diff, ask which is correct
5. Resolve and `git rebase --continue`

### 4. Push

```bash
git push
```

### 5. Report

```bash
git log --oneline -5
```

Show what changed in one line.
