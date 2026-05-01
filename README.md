# FNBAbrain

A session memory store for Claude Code. Captures conversation summaries so context can be recalled and carried forward across sessions.

## How it works

- `/save` — summarize the current conversation and write it to `conversations/`
- `/load` — read all prior summaries into context at the start of a new session
- `python summarize.py` — manual fallback to summarize the most recent session outside of an active conversation (requires `ANTHROPIC_API_KEY` in `.env`)

Summaries are stored as markdown files in `conversations/`, one per save, named by date and time.

## Setup

Slash commands (`/save`, `/load`) are global and live at `~/.claude/commands/`. They are not part of this repo.

To use `summarize.py`:
1. Create a `.env` file at the project root with `ANTHROPIC_API_KEY=sk-...`
2. Run `python summarize.py` from the project root
