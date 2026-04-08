---
name: config-restore
description: Use when setting up Claude Code on a new machine or restoring configuration from the claude-config repo. Handles settings, memories with interactive path remapping, and verifies skills are installed via the plugin.
---

# Config Restore

Restores your Claude Code configuration from the `claude-config` repo onto the current machine. Handles path remapping for project memories interactively.

## When to Use

- Fresh machine setup after `claude plugins add github:<user>/claude-config`
- Restoring config after a reset or reinstall
- Syncing memory from another machine

## How to Run

When the user invokes `/config-restore`, execute these steps:

### Step 1: Locate the repo

Find the `claude-config` repo. Since this skill is installed as a plugin, the repo is in the plugin cache. Check:
1. `~/Developer/AI/claude-config` (if cloned manually)
2. The plugin cache directory for this plugin

If not found, ask the user to clone it first.

### Step 2: Restore settings

```bash
cp <repo>/config/settings.json ~/.claude/settings.json
```

**Before overwriting**, check if `~/.claude/settings.json` already exists with content. If so, show a diff and ask the user to confirm.

### Step 3: Restore project memories (interactive path remapping)

Read `<repo>/config/project-map.json` to understand the original path mappings.

For each project in `<repo>/config/projects/`:

1. Show the user the friendly name and the original path: `"greenely-app" was at /Volumes/greenely/projects/greenely-app`
2. Ask: **"Where is this project on this machine?"**
   - If the user provides a path, encode it the Claude way (replace `/` with `-`, strip leading `-`) and create `~/.claude/projects/<encoded-path>/memory/`
   - If the user says "skip" or "doesn't exist", skip it
   - If the user says "same", use the original encoded path
3. Copy the memory files from `<repo>/config/projects/<friendly-name>/` into the new memory dir

**Path encoding rule:** Claude Code encodes project paths by replacing `/` with `-`. So `/Users/andrei/Developer/AI` becomes `-Users-andrei-Developer-AI`.

### Step 4: Verify skills

Skills should already be available via the plugin. Verify by listing:

```bash
ls ~/.claude/plugins/cache/*/skills/ 2>/dev/null
```

If any skills from the repo are missing, copy them to `~/.claude/skills/` as a fallback.

### Step 5: Summary

Print a summary:
- Settings: restored / skipped
- Memories: N projects restored, M skipped
- Skills: all available via plugin / N copied manually

## Important

- **Never overwrite without asking** — always show what will change
- **Path encoding** — the `-` replacement is how Claude Code maps filesystem paths to project dir names
- **MEMORY.md** — after restoring memories, remind the user that MEMORY.md index files may reference stale paths and should be reviewed
- **Plugins** — don't touch the plugin config. The user installed this repo as a plugin already; skills come from there
