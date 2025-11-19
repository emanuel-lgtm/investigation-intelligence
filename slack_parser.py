from __future__ import annotations

import csv
import json
import io
import os
from datetime import datetime
from typing import Any, Dict, List, Optional


SlackMessage = Dict[str, Any]


def _safe_read(file_obj) -> str:
    try:
        data = file_obj.read()
    except Exception:
        return ""

    if isinstance(data, bytes):
        try:
            text = data.decode("utf-8", errors="ignore")
        except Exception:
            text = data.decode(errors="ignore")
    else:
        text = str(data)

    try:
        file_obj.seek(0)
    except Exception:
        pass

    return text


def _guess_channel_from_name(file_obj) -> Optional[str]:
    name = getattr(file_obj, "name", None)
    if not name:
        return None

    base = os.path.basename(name)
    channel, _sep, _ext = base.partition(".")
    return channel or None


def _parse_ts_to_iso(ts: Any) -> str:
    if ts is None:
        return ""

    ts_str = str(ts).strip()
    if not ts_str:
        return ""

    try:
        seconds = float(ts_str)
        dt = datetime.fromtimestamp(seconds)
        return dt.isoformat()
    except Exception:
        return ts_str


def _normalize_json_message(
    msg: Dict[str, Any],
    idx: int,
    channel: Optional[str],
) -> SlackMessage:
    text = (
        msg.get("text")
        or msg.get("body")
        or msg.get("message")
        or ""
    )

    user_id = msg.get("user") or msg.get("user_id")
    username = (
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
    messages: List[SlackMessage] = []

    try:
        data = json.loads(content)
    except Exception:
        return []

    if isinstance(data, dict):
        if "messages" in data and isinstance(data["messages"], list):
            data_list = data["messages"]
        else:
            data_list = list(data.values())
    else:
        data_list = data

    if not isinstance(data_list, list):
        return []

    for idx, raw_msg in enumerate(data_list):
        if not isinstance(raw_msg, dict):
            continue

        normalized = _normalize_json_message(raw_msg, idx, channel)
        messages.append(normalized)

    return messages


def _normalize_csv_row(
    row: Dict[str, Any],
    idx: int,
    channel: Optional[str],
) -> SlackMessage:
    text = (
        row.get("text")
        or row.get("message")
        or row.get("body")
        or row.get("content")
        or ""
    )

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

    ts = (
        row.get("ts")
        or row.get("timestamp")
        or row.get("date")
        or row.get("time")
    )
    iso_ts = _parse_ts_to_iso(ts)

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
    messages: List[SlackMessage] = []

    if not content.strip():
        return messages

    sio = io.StringIO(content)

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
    try:
        content = _safe_read(file_obj)
        channel = _guess_channel_from_name(file_obj)

        if not content.strip():
            return []

        stripped = content.lstrip()

        if stripped.startswith("{") or stripped.startswith("["):
            messages = _parse_json_export(content, channel)
            if messages:
                return messages

        if "," in content or "\t" in content or ";" in content:
            csv_messages = _parse_csv_export(content, channel)
            if csv_messages:
                return csv_messages

        return _parse_fallback_lines(content, channel)

    except Exception as e:
        print(f"[slack_parser] Failed to parse Slack file: {e}")
        return []
