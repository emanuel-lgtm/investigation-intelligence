"""
TESE V8 / V9 - Pattern Aggregator
Entry 9: Pattern aggregation engine

Responsabilidade:
    - Agregar padrões ao longo de múltiplas mensagens.
    - Contar remetentes mais frequentes e flags / palavras-chave mais frequentes.

Compatibilidade:
    - Mantém a classe PatternAggregator (estilo TESE V8).
    - Adiciona a função aggregate_patterns(messages) (estilo TESE V9),
      usada pelo engine_bridge.run_full_analysis.
"""

from collections import defaultdict
from typing import Dict, List, Any


Message = Dict[str, Any]


class PatternAggregator:
    """
    Aggregates patterns over multiple messages.
    """

    def __init__(self) -> None:
        # Contagem de palavras-chave/flags
        self.keyword_counts = defaultdict(int)
        # Contagem de remetentes/usuários
        self.sender_counts = defaultdict(int)

    def _get_sender(self, msg: Message) -> str:
        """
        Obtém o "remetente" da mensagem de forma tolerante.

        Prioridade:
            1) msg["sender"]
            2) msg["user"]
            3) "unknown"
        """
        sender = msg.get("sender")
        if not sender:
            sender = msg.get("user", "unknown")
        return str(sender)

    def aggregate(self, messages: List[Message]) -> Dict[str, Any]:
        """
        Aggregate patterns across messages.

        Args:
            messages: List of message dictionaries

        Returns:
            Dictionary with aggregated patterns:
                {
                    "top_senders": [(sender, count), ...],
                    "top_keywords": [(keyword, count), ...],
                }
        """
        for msg in messages:
            if not isinstance(msg, dict):
                continue

            sender = self._get_sender(msg)
            self.sender_counts[sender] += 1

            flags = msg.get("flags") or []
            if not isinstance(flags, list):
                flags = [flags]

            for flag in flags:
                self.keyword_counts[str(flag)] += 1

        top_senders = sorted(
            self.sender_counts.items(), key=lambda x: -x[1]
        )[:5]
        top_keywords = sorted(
            self.keyword_counts.items(), key=lambda x: -x[1]
        )[:5]

        return {
            "top_senders": top_senders,
            "top_keywords": top_keywords,
        }


# ---------------------------------------------------------------------------
# Função funcional para TESE V9 - usada pelo engine_bridge
# ---------------------------------------------------------------------------

def aggregate_patterns(messages: List[Message]) -> Dict[str, Any]:
    """
    Função de alto nível usada pela pipeline TESE V9:

        patterns = aggregate_patterns(flagged_messages)

    Responsabilidade:
        - Instanciar PatternAggregator
        - Agregar padrões sobre a lista de mensagens
        - Retornar o dicionário de padrões agregados

    Comportamento:
        - Não levanta exceções em caso de entrada inesperada; devolve
          estrutura vazia quando necessário.
    """
    if not isinstance(messages, list):
        return {"top_senders": [], "top_keywords": []}

    aggregator = PatternAggregator()
    try:
        return aggregator.aggregate(messages)
    except Exception:
        # Fallback extremamente defensivo
        return {"top_senders": [], "top_keywords": []}
