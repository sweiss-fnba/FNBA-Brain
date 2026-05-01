# FNBAbrain — Claude Instructions

This repository is a **session memory store**. It captures summaries of Claude Code sessions so that context can be recalled and carried forward across conversations.

---

## Directory Structure

```
FNBAbrain/
├── CLAUDE.md              ← this file
├── README.md
├── summarize.py           ← stop hook + manual summarization script
├── .env                   ← ANTHROPIC_API_KEY for manual script use (gitignored)
├── .gitignore
└── conversations/         ← session summaries, one file per save
    └── YYYY-MM-DD_HHmmss.md
```

---

## Slash Commands

### `/save`

**Trigger:** User types `/save`

Summarizes the current conversation and writes a markdown file to `conversations/` using the filename format `YYYY-MM-DD_HHmmss.md`. No API key required — runs through Claude directly.

File format:
```markdown
# Conversation Summary

**Date:** YYYY-MM-DD HH:MM
**Saved by:** save

---

## Topic / Goal
## Key Decisions & Findings
## Action Items
```

### `/load`

**Trigger:** User types `/load`

Reads all files in `conversations/` in chronological order (oldest first) and loads them as context for the current session. After reading, gives a brief recap of ongoing threads and open action items.

---

## summarize.py

Dual-mode script used as both a **stop hook** and an optional **manual tool**.

**Stop hook mode** (automatic): Claude Code pipes a JSON payload to stdin when a session ends. The script summarizes the transcript via the Anthropic API and writes to `conversations/`.

**Manual mode**: Run `python summarize.py` from the project root. Reads the most recent session JSONL from `~/.claude/projects/-home-sweiss-workspace-FNBAbrain/`, then calls the Anthropic API to summarize it. Requires `ANTHROPIC_API_KEY` to be set in `.env`.

Stop hook is configured in `~/.claude/settings.json`:
```json
"Stop": [{ "hooks": [{ "type": "command", "command": "/path/to/.venv/bin/python /path/to/summarize.py" }] }]
```

---

## Guidelines

- `conversations/` is the source of truth for session history. Don't edit files there manually.
- `.env` is gitignored — never commit it.
- `/save` is the preferred way to capture a session mid-conversation. The stop hook captures it automatically on exit.
- `/load` at the start of a new session restores continuity from prior work.
