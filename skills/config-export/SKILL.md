---
name: config-export
description: Use when you want to back up or snapshot your current Claude Code configuration (settings, memories, skills) to the claude-config git repo for syncing across machines.
---

# Config Export

Snapshots your current Claude Code configuration into the `claude-config` repo, commits, and pushes.

## What It Exports

1. **Settings** — `~/.claude/settings.json` → `config/settings.json`
2. **Project memories** — All project memory dirs that contain files → `config/projects/<friendly-name>/`
3. **Skills** — All skills from `~/.claude/skills/` → `skills/`
4. **Project map** — Updates `config/project-map.json` with current path-to-name mappings

## How to Run

When the user invokes `/config-export`, execute these steps:

### Step 1: Locate the repo

Find the `claude-config` repo. Check these locations in order:
1. `~/Developer/AI/claude-config`
2. Any directory that is a git remote containing `claude-config` in the URL

If not found, ask the user where it is.

### Step 2: Export settings

```bash
cp ~/.claude/settings.json <repo>/config/settings.json
```

### Step 3: Export project memories

For each directory under `~/.claude/projects/` that contains a `memory/` subdirectory with files:

1. Derive a friendly name from the path-encoded dir name:
   - Strip leading `-`
   - Take the last meaningful segment(s) (e.g., `-Users-andrei-Developer-AI-hired` → `hired`)
   - For ambiguous names, use enough segments to be unique (e.g., `greenely-app` not just `app`)
2. Copy the memory dir contents to `<repo>/config/projects/<friendly-name>/`
3. Update `<repo>/config/project-map.json` with the mapping: `"friendly-name": "original-path-encoded-name"`

### Step 4: Export skills

```bash
# Copy all skills except config-export and config-restore (they live in the repo already)
for skill in ~/.claude/skills/*/; do
  name=$(basename "$skill")
  if [ "$name" != "config-export" ] && [ "$name" != "config-restore" ]; then
    cp -R "$skill" <repo>/skills/
  fi
done
```

### Step 5: Commit and push

```bash
cd <repo>
git add -A
git commit -m "config export $(date +%Y-%m-%d-%H%M)"
git push
```

If push fails (no remote, auth issue), inform the user but don't fail — the local commit is still valuable.

## Important

- Never export `~/.claude/history.jsonl`, `sessions/`, `cache/`, or other ephemeral data
- Always preserve the existing `project-map.json` entries — merge, don't overwrite
- If a skill in the repo is newer than the one in `~/.claude/skills/`, warn before overwriting
