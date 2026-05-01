---
name: FNBAbrain session memory store
description: Current project architecture — summarize.py stop hook, /save and /load slash commands, conversations/ dir
type: project
---

FNBAbrain is a session memory store. It captures and reloads summaries of Claude Code conversations so context persists across sessions.

**Why:** Avoids re-explaining prior decisions and context at the start of every new conversation.

**Structure:**
- `conversations/` — session summaries, one markdown file per save, named `YYYY-MM-DD_HHmmss.md`
- `summarize.py` — dual-mode script: stop hook (auto, via stdin payload) and manual (`python summarize.py`, needs `ANTHROPIC_API_KEY` in `.env`)
- `.env` — holds `ANTHROPIC_API_KEY` for manual script use (gitignored)
- `CLAUDE.md` — project instructions and workflow reference

**Slash commands (global, at `~/.claude/commands/`):**
- `/save` — summarizes current conversation and writes to `conversations/`; no API key needed
- `/load` — reads all `conversations/` files chronologically and restores context for the session

**Stop hook:** `summarize.py` is configured in `~/.claude/settings.json` under `Stop`. It receives the session transcript via stdin, calls Haiku to summarize, and writes to `conversations/`.

**Note:** The project-level `.claude/commands` is a broken device file — all commands live globally at `~/.claude/commands/`.

**How to apply:** At session start, expect the user to type `/load` to restore context. During or after a session, `/save` captures the conversation. The stop hook runs automatically on exit.
