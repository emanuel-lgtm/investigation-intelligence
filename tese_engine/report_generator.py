"""
TESE V8 / V9 - Report Generator
Entry 13: Forensic report generator

Gera relatórios forenses estruturados com base na análise de risco.

Compatibilidade:
    - Mantém a classe ReportGenerator (estilo TESE V8).
    - Adiciona a função generate_report(analysis_data) (estilo TESE V9),
      usada por engine_bridge.create_report.
"""

from typing import Dict, Any


class ReportGenerator:
    """
    Generates structured forensic reports based on the enriched
    risk analysis pipeline.
    """

    def __init__(self) -> None:
        pass

    def generate_summary(self, analysis: Dict[str, Any]) -> str:
        """
        Generate summary report from analysis.

        Args:
            analysis: Analysis dictionary with at least:
                      - "messages": list
                      - "patterns": dict
                      - optionally "risk_summary": dict

        Returns:
            Formatted report string.
        """
        messages = analysis.get("messages", []) or []
        patterns = analysis.get("patterns", {}) or {}
        risk_summary = analysis.get("risk_summary", {}) or {}

        total_messages = len(messages)

        summary_lines = [
            "TESE FORENSIC REPORT",
            "=====================",
            f"Total Messages Analysed: {total_messages}",
            "",
        ]

        # --- Incident counts (se vierem do orchestrate_risk) ---
        incident_counts = risk_summary.get("incident_counts", {})
        if incident_counts:
            summary_lines.append("Incident Severity Breakdown:")
            for level in ("high", "medium", "low"):
                count = incident_counts.get(level, 0)
                summary_lines.append(f"- {level.capitalize()}: {count}")
            summary_lines.append("")

        # --- Top keywords / flags ---
        summary_lines.append("Top Keywords / Flags:")
        for kw, count in patterns.get("top_keywords", []):
            summary_lines.append(f"- {kw}: {count} occurrences")
        if not patterns.get("top_keywords"):
            summary_lines.append("- (none detected)")
        summary_lines.append("")

        # --- Top senders ---
        summary_lines.append("Top Senders / Users:")
        for sender, count in patterns.get("top_senders", []):
            summary_lines.append(f"- {sender}: {count} messages")
        if not patterns.get("top_senders"):
            summary_lines.append("- (none detected)")
        summary_lines.append("")

        # --- Optional final note ---
        summary_lines.append("End of TESE report.")
        return "\n".join(summary_lines)


# ---------------------------------------------------------------------------
# Função funcional TESE V9 - usada pelo engine_bridge
# ---------------------------------------------------------------------------

def generate_report(analysis_data: Dict[str, Any]) -> str:
    """
    TESE V9 expected API:

        report_text = generate_report(analysis_data)

    Onde `analysis_data` é o dicionário retornado por run_full_analysis, ou
    um dicionário compatível contendo pelo menos:
        - "messages": list
        - "patterns": dict
        - opcionalmente "risk_summary": dict

    Esta função é um wrapper fino em cima de ReportGenerator.generate_summary.
    """
    if not isinstance(analysis_data, dict):
        analysis_data = {}

    generator = ReportGenerator()
    try:
        return generator.generate_summary(analysis_data)
    except Exception as e:
        # Fallback extremamente defensivo para nunca quebrar o app
        return f"TESE report could not be generated due to an internal error: {e}"
