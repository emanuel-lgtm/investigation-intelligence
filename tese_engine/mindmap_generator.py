"""
tese_engine.mindmap_generator

Simple, V9-compatible mindmap generator.

This is a functional wrapper that takes the unified TESE analysis_data
(dict returned by engine_bridge.run_full_analysis / analysis_runner)
and returns a JSON-serializable tree structure that can be rendered
as a mindmap or inspected via st.json in the UI.

It does NOT depend on the old TESE V8 OO classes.
"""

from collections import Counter
from typing import Any, Dict, List


def _safe_get_patterns(analysis_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Helper to safely extract the 'patterns' dict from analysis_data.
    """
    patterns = analysis_data.get("patterns", {})
    if not isinstance(patterns, dict):
        return {}
    return patterns


def _safe_get_messages(analysis_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Helper to safely extract the 'messages' list from analysis_data.
    """
    messages = analysis_data.get("messages", [])
    if not isinstance(messages, list):
        return []
    return messages


def generate_mindmap(analysis_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Gera uma estrutura simples de mindmap a partir do analysis_data unificado.

    Estrutura retornada (exemplo):

    {
        "id": "case_root",
        "label": "Case overview",
        "children": [
            {
                "id": "participants",
                "label": "Participants",
                "type": "group",
                "children": [
                    {"id": "participant:Alice", "label": "Alice (123)", "type": "participant"},
                    ...
                ],
            },
            {
                "id": "keywords",
                "label": "Keywords",
                "type": "group",
                "children": [
                    {"id": "keyword:violence", "label": "violence (42)", "type": "keyword"},
                    ...
                ],
            },
            ...
        ],
    }

    A UI atual (ui_studio_panel.py) simplesmente faz `st.json(mindmap)`,
    então não há um esquema rígido a obedecer – apenas precisa ser
    JSON-serializável e razoavelmente interpretável.
    """
    patterns = _safe_get_patterns(analysis_data)
    messages = _safe_get_messages(analysis_data)
    risk_summary = analysis_data.get("risk_summary", {})

    # ------------------------------------------------------------------
    # 1) Participants (top_senders)
    # ------------------------------------------------------------------
    top_senders = patterns.get("top_senders", [])
    participants_children: List[Dict[str, Any]] = []

    for sender, count in top_senders:
        participants_children.append(
            {
                "id": f"participant:{sender}",
                "label": f"{sender} ({count})",
                "type": "participant",
                "count": count,
            }
        )

    participants_node: Dict[str, Any] = {
        "id": "participants",
        "label": "Participants",
        "type": "group",
        "children": participants_children,
    }

    # ------------------------------------------------------------------
    # 2) Keywords (top_keywords)
    # ------------------------------------------------------------------
    top_keywords = patterns.get("top_keywords", [])
    keyword_children: List[Dict[str, Any]] = []

    for kw, count in top_keywords:
        keyword_children.append(
            {
                "id": f"keyword:{kw}",
                "label": f"{kw} ({count})",
                "type": "keyword",
                "count": count,
            }
        )

    keywords_node: Dict[str, Any] = {
        "id": "keywords",
        "label": "Keywords",
        "type": "group",
        "children": keyword_children,
    }

    # ------------------------------------------------------------------
    # 3) Platforms (agregado a partir das mensagens)
    # ------------------------------------------------------------------
    platform_counter = Counter()
    for msg in messages:
        platform = msg.get("platform") or msg.get("source") or "unknown"
        platform_counter[platform] += 1

    platform_children: List[Dict[str, Any]] = [
        {
            "id": f"platform:{name}",
            "label": f"{name} ({count})",
            "type": "platform",
            "count": count,
        }
        for name, count in platform_counter.most_common()
    ]

    platforms_node: Dict[str, Any] = {
        "id": "platforms",
        "label": "Platforms",
        "type": "group",
        "children": platform_children,
    }

    # ------------------------------------------------------------------
    # 4) Risk summary (apenas chaves simples)
    # ------------------------------------------------------------------
    risk_children: List[Dict[str, Any]] = []
    if isinstance(risk_summary, dict):
        for key, value in risk_summary.items():
            # ignorar sub-dicts complexos; isso aqui é só overview
            if isinstance(value, (dict, list)):
                continue
            risk_children.append(
                {
                    "id": f"risk:{key}",
                    "label": f"{key}: {value}",
                    "type": "risk_metric",
                }
            )

    risk_node: Dict[str, Any] = {
        "id": "risk",
        "label": "Risk overview",
        "type": "group",
        "children": risk_children,
    }

    # ------------------------------------------------------------------
    # 5) Root node
    # ------------------------------------------------------------------
    root: Dict[str, Any] = {
        "id": "case_root",
        "label": "Case overview",
        "type": "root",
        "children": [
            participants_node,
            keywords_node,
            platforms_node,
            risk_node,
        ],
    }

    return root
