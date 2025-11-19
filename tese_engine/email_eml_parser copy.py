"""
TESE V9 - Mindmap Generator

Gera uma estrutura de mindmap hierárquica (nós e subnós) a partir
dos dados de análise, pronta para ser consumida por um frontend
interativo (por exemplo, um componente de mindmap que permite
expandir/colapsar conexões).

Formato de saída (exemplo):

{
    "title": "Disputas Corporativas do Grupo X",
    "subtitle": "Based on 300 sources",
    "root": {
        "id": "root",
        "label": "Disputas Corporativas do Grupo X",
        "collapsed": False,
        "children": [
            ...
        ]
    }
}
"""

from typing import Any, Dict, List


Node = Dict[str, Any]


def _make_node(
    node_id: str,
    label: str,
    children: List[Node] | None = None,
    collapsed: bool = True,
    meta: Dict[str, Any] | None = None,
) -> Node:
    """
    Helper para criar um nó de mindmap em formato padrão.
    """
    return {
        "id": node_id,
        "label": label,
        "collapsed": collapsed,
        "children": children or [],
        "meta": meta or {},
    }


def generate_mindmap(analysis_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Gera uma estrutura de mindmap de alto nível a partir de analysis_data.
    """
    if not isinstance(analysis_data, dict):
        analysis_data = {}

    messages = analysis_data.get("messages", []) or []
    patterns = analysis_data.get("patterns", {}) or {}
    correlation = analysis_data.get("correlation", {}) or {}
    risk_summary = analysis_data.get("risk_summary", {}) or {}

    total_messages = len(messages)

    case_title = (
        analysis_data.get("case_title")
        or analysis_data.get("case_name")
        or "TESE Case Overview"
    )

    # Incident node
    incident_counts = risk_summary.get("incident_counts") or {}
    incidents_children: List[Node] = []

    high = incident_counts.get("high", 0)
    medium = incident_counts.get("medium", 0)
    low = incident_counts.get("low", 0)

    incidents_children.extend([
        _make_node("incidents-high", f"High: {high}", collapsed=True),
        _make_node("incidents-medium", f"Medium: {medium}", collapsed=True),
        _make_node("incidents-low", f"Low: {low}", collapsed=True),
    ])

    incidents_node = _make_node(
        "incidents",
        "Incidentes e Severidade",
        children=incidents_children,
        collapsed=False,
    )

    # Patterns
    keyword_children = [
        _make_node(f"keyword-{i}", f"{kw} ({count})", collapsed=True)
        for i, (kw, count) in enumerate(patterns.get("top_keywords", []) or [])
    ] or [
        _make_node("keyword-none", "Nenhum padrão relevante detectado", collapsed=True)
    ]

    patterns_node = _make_node(
        "patterns",
        "Padrões e Flags",
        children=keyword_children,
        collapsed=False,
    )

    # Senders
    sender_children = [
        _make_node(f"sender-{i}", f"{sender} ({count} mensagens)", collapsed=True)
        for i, (sender, count) in enumerate(patterns.get("top_senders", []) or [])
    ] or [
        _make_node("sender-none", "Nenhum remetente-chave identificado", collapsed=True)
    ]

    senders_node = _make_node(
        "senders",
        "Entidades / Participantes",
        children=sender_children,
        collapsed=False,
    )

    # Platforms
    counts_by_platform = correlation.get("counts_by_platform", {}) or {}
    platform_children = [
        _make_node(f"platform-{i}", f"{platform}: {count} mensagens", collapsed=True)
        for i, (platform, count) in enumerate(counts_by_platform.items())
    ] or [
        _make_node("platform-none", "Nenhum dado de plataforma", collapsed=True)
    ]

    platforms_node = _make_node(
        "platforms",
        "Plataformas e Canais",
        children=platform_children,
        collapsed=False,
    )

    # Timeline summary node
    timeline = analysis_data.get("timeline", []) or []
    if timeline:
        first_ts = timeline[0].get("timestamp")
        last_ts = timeline[-1].get("timestamp")
        timeline_label = f"Linha do Tempo ({first_ts} → {last_ts})"
    else:
        timeline_label = "Linha do Tempo (sem dados)"

    timeline_node = _make_node(
        "timeline",
        timeline_label,
        children=[],
        collapsed=True,
    )

    root_children = [
        senders_node,
        patterns_node,
        incidents_node,
        platforms_node,
        timeline_node,
    ]

    root_node = _make_node(
        "root",
        case_title,
        children=root_children,
        collapsed=False,
    )

    return {
        "title": case_title,
        "subtitle": f"Based on {total_messages} sources",
        "root": root_node,
    }
