# FNBAbrain — Claude Instructions

This repository is a **session memory store**. It captures summaries of Claude Code sessions so that context can be recalled and carried forward across conversations.

---

## Directory Structure

```
FNBAbrain/
├── CLAUDE.md              ← this file
├── README.md
├── summarize.py           ← manual summarization script (requires ANTHROPIC_API_KEY)
├── .env                   ← ANTHROPIC_API_KEY for summarize.py (gitignored)
├── .gitignore
├── .venv/                 ← Python venv for summarize.py dependencies
└── conversations/         ← session summaries, one file per save
    └── YYYY-MM-DD_HHmmss.md   ← written by /save
    └── YYYY-MM-DD_<id8>.md    ← written by summarize.py
```

Slash command files live globally at `~/.claude/commands/` (not in this repo):
- `~/.claude/commands/save.md`
- `~/.claude/commands/load.md`

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

Optional manual summarization script. Run from the project root to summarize the most recent session without being inside an active conversation.

**Manual mode**: Detects that stdin is a TTY, reads the most recent session JSONL from `~/.claude/projects/-home-sweiss-workspace-FNBAbrain/`, calls the Anthropic API to summarize, and writes to `conversations/` as `YYYY-MM-DD_{session_id[:8]}.md`.

Requires `ANTHROPIC_API_KEY` to be set in `.env` (loaded automatically by the script).

```bash
python summarize.py
```

The script also contains dead stop-hook code (reads a JSON payload from stdin) but the hook is **not currently wired up** — summarization is fully user-controlled.

---

## Guidelines

- `conversations/` is the source of truth for session history. Don't edit files there manually.
- `.env` is gitignored — never commit it.
- `/save` is the preferred way to capture a session mid-conversation.
- `/load` at the start of a new session restores continuity from prior work.
