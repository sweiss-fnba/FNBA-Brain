# FNBAbrain

An LLM-maintained wiki / second brain. Claude writes and maintains the wiki; you curate sources and ask questions.

## How it works

1. **Drop a source** into `raw/` (article, PDF, notes, etc.)
2. **Say "ingest raw/filename"** — Claude reads it, discusses key points, and updates the wiki: summary page, entity pages, concept pages, cross-references, index, log
3. **Ask questions** — Claude reads the wiki and synthesizes answers with citations. Good answers can be filed back as synthesis pages
4. **Say "lint"** periodically — Claude health-checks the wiki for contradictions, orphans, missing links, and gaps

## Structure

```
raw/          ← your source documents (immutable)
wiki/         ← Claude-maintained wiki
  index.md    ← master catalog of all pages
  log.md      ← chronological record of all activity
  overview.md ← high-level synthesis; start here
  sources/    ← one summary per source
  entities/   ← people, orgs, products, places
  concepts/   ← ideas, themes, frameworks
  synthesis/  ← analyses, comparisons, filed answers
conversations/ ← auto-generated session summaries
```

## Configuration

`CLAUDE.md` is the schema file — it tells Claude how the wiki is structured and what workflows to follow. Edit it to customize conventions for your domain.

## Tools used

- [Obsidian](https://obsidian.md) — browse the wiki, graph view, Dataview queries
- [Obsidian Web Clipper](https://obsidian.md/clipper) — clip web articles to markdown
- Claude Code — the LLM that maintains the wiki
