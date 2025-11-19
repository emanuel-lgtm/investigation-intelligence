"""
tese_engine.message_scorer

Scorer simples / neutro para TESE V9.

Objetivo:
- Evitar ImportError no engine_bridge.
- Permitir que o pipeline rode mesmo sem modelos de IA conectados.
- Cada mensagem ganha um campo "scores" com valores neutros.
"""

from typing import List, Dict, Any


def score_messages(messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Recebe uma lista de mensagens normalizadas e devolve a MESMA lista,
    adicionando um campo "scores" neutro em cada mensagem.

    Formato esperado de cada mensagem de entrada (flexível):
        {
            "platform": "whatsapp" | "slack" | ...,
            "timestamp": "2025-11-18T14:30:00" (opcional),
            "sender": "...",
            "content" ou "text": "...",
            ...
        }

    Saída:
        mesma lista, mas com:
        msg["scores"] = {
            "risk": 0.0,
            "sentiment": "neutral",
            "flags": [],
        }
    """
    scored: List[Dict[str, Any]] = []

    for msg in messages:
        # cópia rasa pra não mexer no objeto original por referência
        m = dict(msg)

        # se já tiver scores (no futuro), não sobrescreve
        if "scores" not in m:
            m["scores"] = {
                "risk": 0.0,
                "sentiment": "neutral",
                "flags": [],
            }

        scored.append(m)

    return scored
