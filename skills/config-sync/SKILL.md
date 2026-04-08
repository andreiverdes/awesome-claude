---
name: config-sync
description: Use when the user wants to bidirectionally sync their Claude Code config — commits local changes, pulls remote changes from other machines, merges, and pushes the result. Use this when multiple machines may have made changes.
---

# Config Sync

Full bidirectional sync: commit local changes, pull remote, rebase, push. Handles the case where multiple machines have made changes.

## When to Use

- Syncing config across multiple machines
- When both local and remote have changes
- When `/config-push` fails because remote is ahead
- General "make everything match everywhere"

## Steps

### 1. Check for changes

```bash
cd ~/.claude && git status --short
```

### 2. Commit local changes (if any)

```bash
cd ~/.claude
git add -A
git diff --cached --quiet || git commit -m "config sync $(hostname) $(date +%Y-%m-%d-%H%M)"
```

### 3. Pull with rebase

```bash
git pull --rebase
```

This replays local commits on top of whatever the other machine pushed. No merge commits.

### 4. Handle conflicts

If rebase conflicts occur:

1. List conflicting files: `git diff --name-only --diff-filter=U`
2. For each file, show both versions
3. **Resolution strategy by file type:**
   - `settings.json` — Show diff, ask user which version to keep (or merge manually)
   - `memory/*.md` — Usually additive. If both machines added different memories, keep both. If same file edited, show diff and ask.
   - `skills/**` — Show diff, ask user which version is correct
4. After resolving all conflicts:
   ```bash
   git add -A
   git rebase --continue
   ```

### 5. Push

```bash
git push
```

### 6. Report

```bash
echo "=== Local changes pushed ===" && git log --oneline origin/main..HEAD 2>/dev/null
echo "=== Remote changes pulled ===" && git log --oneline HEAD..origin/main 2>/dev/null
git diff HEAD~1 --stat 2>/dev/null
```

## Silent Mode (for Stop hook)

When running as a hook, execute the same steps but silently:

```bash
cd ~/.claude
git add -A
git diff --cached --quiet || git commit -m "auto-sync $(hostname) $(date +%Y-%m-%d-%H%M)" -q
git pull --rebase -q 2>/dev/null
git push -q 2>/dev/null || true
```

If rebase fails silently, leave it for the user to resolve manually next session.
