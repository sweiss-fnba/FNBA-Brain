#!/usr/bin/env python3
"""Claude Code Stop hook: summarize the transcript and save to conversations/."""
import json
import os
import sys
from datetime import datetime
from pathlib import Path


def extract_text(content) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, dict):
                t = block.get("type", "")
                if t == "text":
                    parts.append(block.get("text", ""))
                elif t == "tool_use":
                    parts.append(f"[Tool call: {block.get('name', '?')}]")
                elif t == "tool_result":
                    parts.append(f"[Tool result: {extract_text(block.get('content', ''))}]")
            elif isinstance(block, str):
                parts.append(block)
        return "\n".join(p for p in parts if p)
    return str(content)


def build_transcript(messages: list) -> str:
    lines = []
    for msg in messages:
        role = msg.get("role", "unknown").upper()
        text = extract_text(msg.get("content", "")).strip()
        if text:
            # Cap each turn at 3000 chars to keep the summarization prompt reasonable
            lines.append(f"**{role}:** {text[:3000]}")
    return "\n\n".join(lines)


def summarize(transcript: str) -> str:
    import anthropic

    client = anthropic.Anthropic()

    system = (
        "You are a concise technical note-taker. Given a conversation transcript, "
        "produce a brief markdown summary with three sections:\n\n"
        "## Topic / Goal\n"
        "One or two sentences on what the conversation was about.\n\n"
        "## Key Decisions & Findings\n"
        "Bullet list of the most important things decided or discovered. "
        "Omit this section if there is nothing noteworthy.\n\n"
        "## Action Items\n"
        "Bullet list of follow-up tasks or next steps. "
        "Omit this section if none were mentioned.\n\n"
        "Rules: be concise, use bullet points, do not include preamble, "
        "do not repeat the rules back."
    )

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        system=[
            {
                "type": "text",
                "text": system,
                "cache_control": {"type": "ephemeral"},
            }
        ],
        messages=[
            {
                "role": "user",
                "content": f"Summarize this conversation transcript:\n\n{transcript}",
            }
        ],
    )

    for block in response.content:
        if block.type == "text":
            return block.text
    return "*(no summary generated)*"


def load_dotenv(path: Path) -> None:
    """Load KEY=value pairs from a .env file into os.environ (no-op if missing)."""
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def load_latest_session() -> tuple[str, list]:
    """Find and parse the most recent session JSONL for the current project."""
    cwd = Path.cwd()
    path_encoded = cwd.as_posix().replace("/", "-")  # /foo/bar -> -foo-bar
    projects_dir = Path.home() / ".claude" / "projects" / path_encoded

    if not projects_dir.exists():
        return "unknown", []

    jsonl_files = sorted(
        projects_dir.glob("*.jsonl"),
        key=lambda f: f.stat().st_mtime,
        reverse=True,
    )
    if not jsonl_files:
        return "unknown", []

    latest = jsonl_files[0]
    session_id = latest.stem

    messages = []
    with latest.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except Exception:
                continue
            if entry.get("isSidechain"):
                continue
            msg = entry.get("message")
            if not isinstance(msg, dict):
                continue
            role = msg.get("role")
            if role in ("user", "assistant"):
                messages.append({"role": role, "content": msg.get("content", "")})

    return session_id, messages


def main():
    manual = sys.stdin.isatty()

    if manual:
        load_dotenv(Path(__file__).parent / ".env")
        session_id, messages = load_latest_session()
        if not messages:
            print("No session found for this project.", file=sys.stderr)
            sys.exit(1)
        print(f"Summarizing session {session_id[:8]} ({len(messages)} messages)…")
    else:
        try:
            raw = sys.stdin.read()
            if not raw.strip():
                sys.exit(0)
            payload = json.loads(raw)
        except Exception:
            sys.exit(0)
        session_id = payload.get("session_id", "unknown")
        messages = payload.get("transcript", [])

    if not messages:
        if manual:
            print("Transcript is empty.", file=sys.stderr)
            sys.exit(1)
        sys.exit(0)

    transcript = build_transcript(messages)
    if not transcript.strip():
        if manual:
            print("No readable text in transcript.", file=sys.stderr)
            sys.exit(1)
        sys.exit(0)

    try:
        summary = summarize(transcript)
    except Exception as exc:
        if manual:
            print(f"Summarization failed: {exc}", file=sys.stderr)
            sys.exit(1)
        sys.exit(0)

    conversations_dir = Path(__file__).parent / "conversations"
    try:
        conversations_dir.mkdir(exist_ok=True)
        date_str = datetime.now().strftime("%Y-%m-%d")
        session_prefix = session_id[:8] if len(session_id) >= 8 else session_id
        output_path = conversations_dir / f"{date_str}_{session_prefix}.md"
        header = (
            f"# Conversation Summary\n\n"
            f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
            f"**Session:** {session_id}\n\n---\n\n"
        )
        output_path.write_text(header + summary + "\n", encoding="utf-8")
        if manual:
            print(f"Saved: {output_path}")
    except Exception as exc:
        if manual:
            print(f"Failed to write output: {exc}", file=sys.stderr)
            sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
