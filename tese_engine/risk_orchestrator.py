"""
TESE V8 / V9 - Risk Orchestrator
Entry 12: Risk orchestration engine

Compatibilidade:
    - Mantém a classe RiskOrchestrator (V8).
    - Adiciona função orchestrate_risk(...) (V9) esperada pelo engine_bridge.
"""

from typing import Dict, List, Any


Message = Dict[str, Any]


class RiskOrchestrator:
    """
    V8 orchestration engine.
    Orchestrates scorer, flagger, and aggregator components.
    """

    def __init__(self, scorer, flagger, aggregator):
        self.scorer = scorer
        self.flagger = flagger
        self.aggregator = aggregator

    def process_messages(self, messages: List[Dict]) -> Dict[str, Any]:
        """
        Full orchestration pipeline (V8 style).
        """
        enriched = []

        for msg in messages:
            # Scoring step
            score_info = self.scorer.score_message(msg.get("content", "") or msg.get("text", ""))
            msg.update(score_info)

            # Flagging step
            flag_info = self.flagger.evaluate(msg)
            msg.update(flag_info)

            enriched.append(msg)

        # Pattern aggregation
        aggregation = self.aggregator.aggregate(enriched)

        return {
            "messages": enriched,
            "patterns": aggregation,
        }


# ----------------------------------------------------------------------------
# Função funcional TESE V9
# ----------------------------------------------------------------------------

def orchestrate_risk(
    flagged_messages: List[Message],
    pattern_data: Dict[str, Any],
    correlation_data: Dict[str, Any],
    timeline_data: List[Message]
) -> Dict[str, Any]:
    """
    TESE V9 expected API:

        risk_summary = orchestrate_risk(
            flagged_messages,
            patterns,
            correlated,
            timeline
        )

    Responsibilities:
        - Produce a high-level risk summary derived from already-processed data.
        - V9 does NOT run scorer/flagger again (already done earlier).
        - This wrapper does NOT use the V8 RiskOrchestrator.process_messages(),
          because V9 pipeline already performed scoring/flagging/aggregation.
        - Instead, this summarizes final risk signals.

    Returns:
        Dictionary with risk summary structure.
    """

    risk_summary = {}

    # Count high-severity incidents
    high = 0
    medium = 0
    low = 0

    for msg in flagged_messages:
        severity = (
            msg.get("incident_analysis", {}).get("severity")
            or "low"
        )
        if severity == "high":
            high += 1
        elif severity == "medium":
            medium += 1
        else:
            low += 1

    # High-level summary dictionary
    risk_summary["incident_counts"] = {
        "high": high,
        "medium": medium,
        "low": low,
    }

    # Patterns summary
    risk_summary["patterns"] = pattern_data or {}

    # Platform correlation summary
    risk_summary["platform_correlation"] = correlation_data or {}

    # Timeline summary
    risk_summary["timeline"] = timeline_data or []

    return risk_summary
