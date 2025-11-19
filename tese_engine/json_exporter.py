"""
TESE V9 - JSON Exporter

Gera JSONs amigáveis para integrações e frontends:

1) Summary compacto (case_summary.json):
    - incident_counts
    - top_keywords
    - top_senders
    - platform_counts
    - timeline_summary
    - mindmap (já gerado por mindmap_generator)

2) Mensagens completas (messages.json):
    - lista de mensagens normalizadas (id, plataforma, timestamp, user, text, flags, scores)
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional


def _get_project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _ensure_dir(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def build_case_summary_payload(
    analysis_data: Dict[str, Any],
    mindmap: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Monta o payload enxuto de resumo de caso.

    Espera analysis_data no formato de run_full_analysis:
        "messages", "patterns", "correlation", "timeline", "risk_summary"
    """
    if not isinstance(analysis_data, dict):
        analysis_data = {}

    messages = analysis_data.get("messages", []) or []
    patterns = analysis_data.get("patterns", {}) or {}
    correlation = analysis_data.get("correlation", {}) or {}
    risk_summary = analysis_data.get("risk_summary", {}) or {}
    timeline = analysis_data.get("timeline", []) or []

    incident_counts = risk_summary.get("incident_counts", {}) or {}
    platform_counts = correlation.get("counts_by_platform", {}) or {}

    # Timeline summary simples: só timestamps + plataforma
    timeline_summary = [
        {
            "timestamp": m.get("timestamp"),
            "platform": m.get("platform"),
            "severity": (m.get("incident_analysis") or {}).get("severity", "low"),
        }
        for m in timeline
    ]

    return {
        "meta": {
            "total_messages": len(messages),
        },
        "incident_counts": incident_counts,
        "top_keywords": patterns.get("top_keywords", []),
        "top_senders": patterns.get("top_senders", []),
        "platform_counts": platform_counts,
        "timeline_summary": timeline_summary,
        "mindmap": mindmap or {},
    }


def build_messages_payload(analysis_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Normaliza lista de mensagens para export (messages.json).
    """
    if not isinstance(analysis_data, dict):
        analysis_data = {}

    messages = analysis_data.get("messages", []) or []

    normalized: List[Dict[str, Any]] = []
    for i, m in enumerate(messages):
        if not isinstance(m, dict):
            continue

        normalized.append(
            {
                "id": m.get("id") or m.get("message_id") or f"msg_{i}",
                "platform": m.get("platform", "unknown"),
                "timestamp": m.get("timestamp"),
                "user": m.get("user") or m.get("sender"),
                "text": m.get("text") or m.get("content", ""),
                "flags": m.get("flags", []),
                "scores": m.get("scores", {}),
                "incident_analysis": m.get("incident_analysis", {}),
            }
        )

    return normalized


def export_case_summary_json(
    analysis_data: Dict[str, Any],
    mindmap: Optional[Dict[str, Any]],
    output_path: Path,
) -> Path:
    """
    Gera e salva case_summary.json no caminho indicado.
    """
    _ensure_dir(output_path)
    payload = build_case_summary_payload(analysis_data, mindmap)
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    return output_path


def export_messages_json(
    analysis_data: Dict[str, Any],
    output_path: Path,
) -> Path:
    """
    Gera e salva messages.json no caminho indicado.
    """
    _ensure_dir(output_path)
    payload = build_messages_payload(analysis_data)
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    return output_path
