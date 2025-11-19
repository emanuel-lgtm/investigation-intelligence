"""
TESE V8 / V9 - Timeline Builder
Entry 11: Master timeline builder

Compatibilidade:
    - Mantém a classe TimelineBuilder (V8).
    - Adiciona função build_timeline(messages) (V9) esperada pelo engine_bridge.
"""

from datetime import datetime
from typing import Dict, List, Any


Message = Dict[str, Any]


class TimelineBuilder:
    """
    Builds a unified chronological timeline from correlated messages.
    """

    def __init__(self):
        pass

    def build(self, merged_messages: List[Dict]) -> List[Dict]:
        """
        Build chronological timeline from messages.

        V8-style ordering and normalization.
        """
        ordered = sorted(
            merged_messages,
            key=lambda x: x.get("timestamp") or datetime.min
        )

        timeline = []
        for msg in ordered:
            timeline.append({
                "timestamp": msg.get("timestamp"),
                "platform": msg.get("platform"),
                "sender": msg.get("sender") or msg.get("user"),
                "content": msg.get("content") or msg.get("text", ""),
                "score": msg.get("score", 0),
                "flags": msg.get("flags", []),
            })

        return timeline


# ---------------------------------------------------------------------------
# Função funcional TESE V9
# ---------------------------------------------------------------------------

def build_timeline(messages: List[Message]) -> List[Message]:
    """
    TESE V9 expected API:

        timeline = build_timeline(flagged_messages)

    Responsibilities:
        - Defensive wrapper around V8 TimelineBuilder
        - Accepts flat list of messages (from engine_bridge)
        - Returns sorted timeline with normalized fields
    """
    if not isinstance(messages, list):
        return []

    builder = TimelineBuilder()

    try:
        return builder.build(messages)
    except Exception:
        return []
