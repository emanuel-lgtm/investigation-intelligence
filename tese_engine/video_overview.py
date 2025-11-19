"""
TESE V9 - Video Overview Script Generator

Gera um roteiro em texto para um vídeo-resumo do caso,
a partir dos dados agregados de análise.

Compatibilidade:
    - Expõe a função generate_video_script(analysis_data),
      importada por engine_bridge.create_video_overview.
"""

from typing import Any, Dict


def generate_video_script(analysis_data: Dict[str, Any]) -> str:
    """
    Gera um roteiro textual simples para um vídeo de overview.

    Usa principalmente:
        - risk_summary["incident_counts"]
        - patterns["top_keywords"]
        - patterns["top_senders"]

    Parâmetro:
        analysis_data: dicionário retornado por run_full_analysis, contendo
            {
                "messages": [...],
                "patterns": {...},
                "correlation": {...},
                "timeline": [...],
                "risk_summary": {...},
                ...
            }

    Retorna:
        Uma string com o script do vídeo.
    """
    if not isinstance(analysis_data, dict):
        analysis_data = {}

    messages = analysis_data.get("messages", []) or []
    total_messages = len(messages)

    risk_summary = analysis_data.get("risk_summary", {}) or {}
    incident_counts = risk_summary.get("incident_counts", {}) or {}

    patterns = analysis_data.get("patterns", {}) or {}
    top_keywords = patterns.get("top_keywords", []) or []
    top_senders = patterns.get("top_senders", []) or []

    # Começa o script
    lines = []

    lines.append("Olá, este é um overview automático gerado pelo TESE.")
    lines.append(
        f"Nesta investigação foram analisadas aproximadamente {total_messages} mensagens em múltiplas plataformas."
    )

    # Bloco de incidentes
    if incident_counts:
        high = incident_counts.get("high", 0)
        medium = incident_counts.get("medium", 0)
        low = incident_counts.get("low", 0)
        lines.append(
            f"Foram identificados {high} incidentes de alta severidade, "
            f"{medium} de severidade média e {low} de baixa severidade."
        )

    # Bloco de palavras-chave / flags
    if top_keywords:
        keywords_str = ", ".join([kw for kw, _ in top_keywords])
        lines.append(
            f"As principais palavras-chave e sinais de risco encontrados incluem: {keywords_str}."
        )

    # Bloco de remetentes / participantes
    if top_senders:
        senders_str = ", ".join([sender for sender, _ in top_senders])
        lines.append(
            f"Os participantes que mais se destacam nas comunicações são: {senders_str}."
        )

    # Encerramento
    lines.append(
        "Este resumo não substitui a leitura integral do relatório, "
        "mas oferece uma visão rápida dos principais riscos identificados."
    )
    lines.append("Para mais detalhes, consulte o relatório forense completo gerado pelo TESE.")

    return "\n".join(lines)
