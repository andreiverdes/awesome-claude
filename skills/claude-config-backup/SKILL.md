---
name: claude-config-backup
description: Use when the user wants to back up, sync, or make portable their Claude Code configuration (skills, settings, memories) across machines. Triggers on mentions of backing up claude config, syncing settings, new machine setup, dotfiles for claude, or portable claude configuration.
---

# Claude Config Backup

Set up a portable, auto-syncing backup of your entire Claude Code configuration as a single GitHub repo that doubles as a plugin.

## When to Use

- User wants to back up their Claude Code config
- User is setting up a new machine and needs to restore their setup
- User wants to sync config across multiple machines
- User mentions dotfiles, portable config, or backup for Claude

## Architecture

One git repo that serves three purposes:

1. **Plugin** — `claude plugins add github:<user>/<repo>` installs all skills instantly
2. **Config backup** — settings, keybindings, and project memories stored with path-agnostic names
3. **Auto-sync** — a `Stop` hook silently commits and pushes after every session

```
claude-config/
├── skills/                     # All custom skills (plugin-installable)
│   ├── config-export/          # Manual export skill
│   ├── config-restore/         # Restore on new machine
│   └── <user's skills>/
├── hooks/
│   └── skill-sync.sh           # Auto-syncs skills on Write/Edit
├── config/
│   ├── settings.json           # Claude Code settings
│   ├── keybindings.json        # Key customizations (if any)
│   ├── project-map.json        # friendly-name ↔ path-encoded-name mappings
│   └── projects/               # Memory files with path-agnostic names
│       ├── my-project/
│       └── other-project/
├── sync.sh                     # Auto-sync script (runs on Stop hook)
├── .gitignore
└── README.md
```

## Setup Process

### Step 1: Ask the user for repo location and name

Default: `~/Developer/AI/claude-config`. Ask the user to confirm or provide an alternative.

### Step 2: Create repo structure

```bash
mkdir -p <repo>/skills <repo>/config/projects
cd <repo> && git init
```

### Step 3: Copy existing skills

Copy all skills from `~/.claude/skills/` into `<repo>/skills/`. Skip any that are already there.

### Step 4: Copy settings

```bash
cp ~/.claude/settings.json <repo>/config/settings.json
cp ~/.claude/keybindings.json <repo>/config/keybindings.json 2>/dev/null
```

### Step 5: Copy project memories with path-agnostic names

For each dir under `~/.claude/projects/` that has a `memory/` subdirectory with files:

1. Derive a friendly name by stripping common path segments (Users, username, Developer, Volumes, projects, etc.) and keeping the meaningful parts
2. Copy memory files to `<repo>/config/projects/<friendly-name>/`
3. Record the mapping in `<repo>/config/project-map.json`:
   ```json
   { "friendly-name": "-Original-Path-Encoded-Name" }
   ```

**Show the user the derived names and let them adjust before proceeding.**

### Step 6: Create the sync script

Create `<repo>/sync.sh` that:

1. Copies `~/.claude/settings.json` → `<repo>/config/settings.json`
2. Copies all skills from `~/.claude/skills/` → `<repo>/skills/` (skipping config-export/config-restore)
3. For each project with memory files, copies to `<repo>/config/projects/` using the friendly name from project-map.json (or derives a new one for new projects)
4. Updates `project-map.json` with any new mappings
5. Runs `git add -A && git commit && git push` silently

**Critical sync.sh requirements:**
- Must be executable (`chmod +x`)
- Must run silently — no stdout, no prompts
- Must be best-effort — if push fails (no remote, no network), exit cleanly
- Must run fast — it fires after every session
- Must background the push (`git push -q &` or run the whole script with `&`)
- New project memories should auto-derive friendly names without user interaction

### Step 7: Wire the Stop hook

Add to `~/.claude/settings.json` under `hooks.Stop`:

```json
{
  "hooks": [
    {
      "type": "command",
      "command": "$HOME/<path-to-repo>/sync.sh &"
    }
  ]
}
```

Append to the existing Stop hooks array — never replace existing hooks.

### Step 8: Create the skill-sync hook

Create `<repo>/hooks/skill-sync.sh` — a PostToolUse hook that fires on Write/Edit and detects changes to `~/.claude/skills/`:

1. Extract `file_path` from the `$TOOL_INPUT` JSON
2. If the path is NOT under `~/.claude/skills/`, exit silently
3. Extract the skill name (first directory segment after `skills/`)
4. Skip config skills (`config-export`, `config-restore`, `claude-config-backup`) — they already live in the repo
5. **Always** copy the skill to `<repo>/skills/` (private backup, no questions asked)
6. If the user also has a **public skills repo** (e.g., `awesome-claude`):
   - If the skill is **new** to the public repo: output `NEW_SKILL_DETECTED: "<name>" has been synced to claude-config. Ask the user if it should be added to the public repo.`
   - If the skill **exists but was updated**: output `SKILL_UPDATED: "<name>" has been synced to claude-config. The public repo copy is outdated. Ask the user if it should be updated.`

**Critical requirements:**
- Must be executable (`chmod +x`)
- Must exit 0 on non-skill files (silent, no output)
- Output text only when user action is needed (new/updated skill for public repo)
- The public repo path should be configurable at the top of the script

Wire it into `~/.claude/settings.json` under `hooks.PostToolUse`:

```json
{
  "matcher": "Write|Edit",
  "hooks": [
    {
      "type": "command",
      "command": "$HOME/<path-to-repo>/hooks/skill-sync.sh"
    }
  ]
}
```

Append to the existing PostToolUse hooks array — never replace existing hooks.

### Step 9: (Optional) Set up a public skills repo

If the user wants to open-source some skills, create a separate repo (e.g., `awesome-claude`) containing only the generic, non-personal skills. The skill-sync hook from Step 8 will prompt for each new/updated skill whether it should be added to the public repo.

```bash
mkdir -p <public-repo>/skills
cd <public-repo> && git init
```

Copy only the skills the user approves for open-sourcing. Add a README listing available skills and install instructions (`claude plugins add github:<user>/<repo>`).

### Step 10: Create config-export skill

Create `<repo>/skills/config-export/SKILL.md` — a manual trigger that does the same as sync.sh but:
- Runs interactively (shows what changed)
- Lets the user review before committing
- Useful for first-time setup or when the user wants to verify

### Step 11: Create config-restore skill

Create `<repo>/skills/config-restore/SKILL.md` — for new machine setup:
- Restores settings.json (with diff confirmation if one already exists)
- For each project memory, asks the user where that project lives on this machine
- Remaps the path-encoded directory name accordingly
- Verifies skills are available via the plugin

**Path encoding rule:** Claude Code encodes `/Users/foo/bar` as `-Users-foo-bar` for project directory names.

### Step 12: Create .gitignore and README

**.gitignore:**
```
.DS_Store
*.swp
*~
```

**README.md:** Brief explanation with new-machine setup instructions:
```
claude plugins add github:<user>/<repo>
claude → /config-restore
```

### Step 13: Initial commit

```bash
cd <repo>
git add -A
git commit -m "initial config export"
```

Tell the user to create a GitHub repo and push:
```bash
git remote add origin git@github.com:<user>/<repo>.git
git push -u origin main
```

## What Gets Backed Up

| Item | Location | Backed Up? |
|------|----------|------------|
| Custom skills | `~/.claude/skills/` | Yes — as plugin |
| Settings + hooks | `~/.claude/settings.json` | Yes |
| Keybindings | `~/.claude/keybindings.json` | Yes (if exists) |
| Project memories | `~/.claude/projects/*/memory/` | Yes — path-agnostic |
| Session history | `~/.claude/history.jsonl` | No — ephemeral |
| Sessions | `~/.claude/sessions/` | No — ephemeral |
| Caches | `~/.claude/cache/`, `image-cache/`, etc. | No — ephemeral |
| Plugin cache | `~/.claude/plugins/cache/` | No — reinstalled via plugin |

## New Machine Restore Flow

```
1. Install Claude Code
2. claude plugins add github:<user>/<repo>     ← skills available
3. claude
4. > /config-restore                            ← settings + memories restored
5. Done
```

## Common Issues

| Issue | Fix |
|-------|-----|
| Push fails silently | Check `git remote -v` in the repo, ensure SSH keys are set up |
| New project memories not syncing | sync.sh auto-derives names; check project-map.json for the mapping |
| Settings overwritten by sync | sync.sh copies FROM ~/.claude TO repo, never the reverse (that's config-restore) |
| Duplicate skills after plugin install | Skills in `~/.claude/skills/` take precedence over plugin skills; remove local copies if using plugin |
