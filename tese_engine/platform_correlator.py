"""
TESE V8 / V9 - Platform Correlator
Entry 10: Cross-platform correlation engine

Compatibilidade:
    - Mantém a classe PlatformCorrelator (estilo TESE V8).
    - Adiciona a função correlate_platforms(messages) (estilo TESE V9),
      usada pelo engine_bridge.run_full_analysis.
"""

from datetime import datetime
from typing import Dict, List, Any


Message = Dict[str, Any]


class PlatformCorrelator:
    """
    V8 Engine – correlates user identities and message timelines across platforms.
    """

    def __init__(self):
        # Mapeamento opcional para alias de usuários.
        # Pode ser expandido no futuro.
        self.aliases = {}

    def normalize_sender(self, sender: str) -> str:
        """
        Normalize sender name across platforms.
        """
        if not sender:
            return "unknown"
        sender = str(sender).lower().strip()
        return self.aliases.get(sender, sender)

    def correlate(self, platform_messages: Dict[str, List[Dict]]) -> List[Dict]:
        """
        Merges messages from multiple platforms into a single
        time-ordered list of normalized messages.
        """
        merged = []

        for platform, msgs in platform_messages.items():
            if not isinstance(msgs, list):
                continue

            for m in msgs:
                merged.append({
                    "platform": platform,
                    "timestamp": m.get("timestamp"),
                    "sender": self.normalize_sender(m.get("sender") or m.get("user")),
                    "content": m.get("content") or m.get("text", ""),
                    "score": m.get("score", 0),
                    "flags": m.get("flags", []),
                })

        # Ordenação temporal – tolerante a timestamps ausentes
        def sort_key(msg):
            ts = msg.get("timestamp")
            try:
                return ts or datetime.min
            except Exception:
                return datetime.min

        merged.sort(key=sort_key)
        return merged


# ---------------------------------------------------------------------------
# Função funcional TESE V9
# ---------------------------------------------------------------------------

def correlate_platforms(messages: List[Message]) -> Dict[str, Any]:
    """
    TESE V9 expected API:
        correlated = correlate_platforms(flagged_messages)

    Responsabilidades:
        - Agrupar mensagens por plataforma.
        - Chamar o correlator V8.
        - Devolver resumo estruturado para o upstream (engine_bridge).

    Formato de retorno:
        {
            "merged": [...],
            "counts_by_platform": {"whatsapp": 10, "slack": 4, ...},
            "unique_senders": ["john", "maria", ...]
        }
    """
    if not isinstance(messages, list):
        return {"merged": [], "counts_by_platform": {}, "unique_senders": []}

    # Agrupamento V9 -> V8
    grouped: Dict[str, List[Message]] = {}

    for m in messages:
        if not isinstance(m, dict):
            continue

        platform = m.get("platform", "unknown")
        grouped.setdefault(platform, []).append(m)

    # Chamada do motor V8
    correlator = PlatformCorrelator()

    try:
        merged = correlator.correlate(grouped)
    except Exception:
        merged = []

    # Estatísticas simples (úteis para o relatório)
    counts_by_platform = {
        platform: len(msgs) for platform, msgs in grouped.items()
    }

    senders = sorted({
        msg.get("sender") or msg.get("user") or "unknown"
        for msg in merged
    })

    return {
        "merged": merged,
        "counts_by_platform": counts_by_platform,
        "unique_senders": senders,
    }
