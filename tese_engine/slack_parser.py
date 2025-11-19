"""
tese_engine.slack_parser

Minimal, defensive Slack parser for TESE V9.

This module exposes:

    parse_slack(file_obj) -> list[dict]

It is designed to **never crash** and to work with common Slack export formats:

1. JSON exports (standard Slack export: one JSON file per channel)
2. CSV-like exports (with headers such as "ts", "text", "user", etc.)
3. Fallback: treats each non-empty line as a message

Returned message schema (normalized):

Each message is a dict with at least:

    {
        "platform": "slack",
        "message_id": str,
        "user": str or None,
        "user_id": str or None,
        "channel": str or None,
        "text": str,
        "timestamp": str,  # ISO-8601 when possible, otherwise original
        "raw": dict or str  # original row/object/line
    }

This should be compatible with a generic TESE engine pipeline that expects:
- a "text" field for content,
- a "timestamp" field for ordering,
- some kind of user/channel metadata when available.
"""

from __future__ import annotations

import csv
import json
import io
import os
from datetime import datetime
from typing import Any, Dict, List, Optional


SlackMessage = Dict[str, Any]


def _safe_read(file_obj) -> str:
    """
    Safely reads the entire content of file_obj as UTF-8 text.

    Works with:
    - Streamlit UploadedFile
    - File-like objects (BytesIO, TextIO)
    - Open file handles
    """
    # Try to read bytes, then decode
    try:
        data = file_obj.read()
    except Exception:
        return ""

    # If we got bytes, decode; if already str, return as-is
    if isinstance(data, bytes):
        try:
            text = data.decode("utf-8", errors="ignore")
        except Exception:
            text = data.decode(errors="ignore")
    else:
        text = str(data)

    # Reset cursor so other parts of the system can re-use the file if needed
    try:
        file_obj.seek(0)
    except Exception:
        pass

    return text


def _guess_channel_from_name(file_obj) -> Optional[str]:
    """
    Tries to guess the Slack channel name from the file object name, if present.

    Example:
        "general.json" -> "general"
        "random.csv"   -> "random"
    """
    name = getattr(file_obj, "name", None)
    if not name:
        return None

    base = os.path.basename(name)
    channel, _sep, _ext = base.partition(".")
    return channel or None


def _parse_ts_to_iso(ts: Any) -> str:
    """
    Converts Slack-style timestamps to ISO-8601 when possible.

    Slack timestamps are often strings like:
        "1609459200.000100"
    or just integer seconds.

    If parsing fails, returns the original string.
    """
    if ts is None:
        return ""

    ts_str = str(ts).strip()
    if not ts_str:
        return ""

    # Try Unix epoch with optional fractional part
    try:
        # "1609459200.000100" -> float -> seconds since epoch
        seconds = float(ts_str)
        dt = datetime.fromtimestamp(seconds)
        return dt.isoformat()
    except Exception:
        # Not a numeric timestamp, return raw
        return ts_str


def _normalize_json_message(
    msg: Dict[str, Any],
    idx: int,
    channel: Optional[str],
) -> SlackMessage:
    """
    Normalizes a single JSON Slack message object into the standard schema.
    """
    text = (
        msg.get("text")
        or msg.get("body")
        or msg.get("message")
        or ""
    )

    user_id = msg.get("user") or msg.get("user_id")
    username = (
        # Typical Slack export: user_profile.display_name / real_name
        (msg.get("user_profile") or {}).get("display_name")
        or (msg.get("user_profile") or {}).get("real_name")
        or msg.get("username")
        or msg.get("user_name")
        or user_id
        or "unknown"
    )

    ts = msg.get("ts") or msg.get("timestamp") or msg.get("date")
    iso_ts = _parse_ts_to_iso(ts)

    message_id = (
        msg.get("client_msg_id")
        or msg.get("id")
        or ts
        or f"slack_{idx}"
    )

    return {
        "platform": "slack",
        "message_id": str(message_id),
        "user": str(username) if username is not None else None,
        "user_id": str(user_id) if user_id is not None else None,
        "channel": channel,
        "text": str(text),
        "timestamp": iso_ts,
        "raw": msg,
    }


def _parse_json_export(content: str, channel: Optional[str]) -> List[SlackMessage]:
    """
    Attempts to parse `content` as a standard Slack JSON export.

    Slack JSON export for a channel is typically:
        [
          {"type": "message", "user": "U123", "text": "...", "ts": "123..."},
          ...
        ]
    """
    messages: List[SlackMessage] = []

    try:
        data = json.loads(content)
    except Exception:
        return []

    # Export might be a list of messages or an object with a "messages" key
    if isinstance(data, dict):
        if "messages" in data and isinstance(data["messages"], list):
            data_list = data["messages"]
        else:
            # Unexpected format, but try to treat values as messages
            data_list = list(data.values())
    else:
        data_list = data

    if not isinstance(data_list, list):
        return []

    for idx, raw_msg in enumerate(data_list):
        if not isinstance(raw_msg, dict):
            # Skip non-dict entries
            continue

        # Some Slack exports include non-message events (joins, leaves, etc.)
        msg_type = raw_msg.get("type", "message")
        if msg_type not in ("message", "file_share", "bot_message", None):
            # Keep it conservative; still possible to include all if desired
            # but we skip clearly non-message events.
            pass  # We don't hard-skip by type; TESE might still want events.

        normalized = _normalize_json_message(raw_msg, idx, channel)
        messages.append(normalized)

    return messages


def _normalize_csv_row(
    row: Dict[str, Any],
    idx: int,
    channel: Optional[str],
) -> SlackMessage:
    """
    Normalizes one CSV row into the SlackMessage schema.
    """
    # Try common column names for text
    text = (
        row.get("text")
        or row.get("message")
        or row.get("body")
        or row.get("content")
        or ""
    )

    # Common column names for user info
    user_id = (
        row.get("user_id")
        or row.get("user")
        or row.get("uid")
    )
    username = (
        row.get("user_name")
        or row.get("username")
        or row.get("name")
        or row.get("display_name")
        or user_id
        or "unknown"
    )

    # Common timestamp columns
    ts = (
        row.get("ts")
        or row.get("timestamp")
        or row.get("date")
        or row.get("time")
    )
    iso_ts = _parse_ts_to_iso(ts)

    # Common ID columns
    message_id = (
        row.get("message_id")
        or row.get("id")
        or ts
        or f"slack_{idx}"
    )

    csv_channel = (
        row.get("channel")
        or row.get("channel_name")
        or channel
    )

    return {
        "platform": "slack",
        "message_id": str(message_id),
        "user": str(username) if username is not None else None,
        "user_id": str(user_id) if user_id is not None else None,
        "channel": str(csv_channel) if csv_channel is not None else None,
        "text": str(text),
        "timestamp": iso_ts,
        "raw": row,
    }


def _parse_csv_export(content: str, channel: Optional[str]) -> List[SlackMessage]:
    """
    Attempts to parse `content` as a CSV with message rows.

    This is purposely tolerant:
    - Uses csv.Sniffer when possible
    - Assumes first row is header
    """
    messages: List[SlackMessage] = []

    if not content.strip():
        return messages

    sio = io.StringIO(content)

    # Try to sniff dialect; fall back to default
    try:
        sample = content[:1024]
        dialect = csv.Sniffer().sniff(sample)
        sio.seek(0)
        reader = csv.DictReader(sio, dialect=dialect)
    except Exception:
        sio.seek(0)
        reader = csv.DictReader(sio)

    if not reader.fieldnames:
        return messages

    for idx, row in enumerate(reader):
        if not row:
            continue
        messages.append(_normalize_csv_row(row, idx, channel))

    return messages


def _parse_fallback_lines(content: str, channel: Optional[str]) -> List[SlackMessage]:
    """
    Fallback parser: treat each non-empty line as a separate message.

    This ensures the parser **never** returns an error, even for unknown formats.
    """
    messages: List[SlackMessage] = []

    lines = content.splitlines()
    for idx, line in enumerate(lines):
        text = line.strip()
        if not text:
            continue

        messages.append(
            {
                "platform": "slack",
                "message_id": f"slack_line_{idx}",
                "user": "unknown",
                "user_id": None,
                "channel": channel,
                "text": text,
                "timestamp": "",
                "raw": line,
            }
        )

    return messages


def parse_slack(file_obj) -> List[SlackMessage]:
    """
    Public entry point for Slack parsing.

    Args:
        file_obj: File-like object (e.g., Streamlit UploadedFile, open file)
                  containing a Slack export (JSON, CSV, or plain text).

    Returns:
        List[SlackMessage] – an array of normalized message dicts.

    This function is **defensive**:
    - It never raises an exception intentionally.
    - On unknown or malformed input, it falls back to line-based parsing.
    - It is safe to call even on non-Slack files (it will just produce
      generic line-based messages or an empty list).

    This should be enough to unblock the TESE V9 backend and remove the
    ImportError for `parse_slack`.
    """
    try:
        content = _safe_read(file_obj)
        channel = _guess_channel_from_name(file_obj)

        if not content.strip():
            return []

        stripped = content.lstrip()

        # 1) Try JSON first if it looks like JSON
        if stripped.startswith("{") or stripped.startswith("["):
            messages = _parse_json_export(content, channel)
            if messages:
                return messages
            # If JSON attempt fails or returns empty, continue to CSV / fallback

        # 2) Try CSV if there are obvious separators
        if "," in content or "\t" in content or ";" in content:
            csv_messages = _parse_csv_export(content, channel)
            if csv_messages:
                return csv_messages

        # 3) Fallback: one message per line
        return _parse_fallback_lines(content, channel)

    except Exception as e:
        # Absolutely last resort: never crash the pipeline
        # We print the error for debugging, but still return an empty list
        print(f"[slack_parser] Failed to parse Slack file: {e}")
        return []
