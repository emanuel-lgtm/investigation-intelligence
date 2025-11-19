"""
TESE V8 / V9 - Incident Flagger
Entry 8: Incident detection engine

Responsabilidade principal:
    - Detectar incidentes com base em:
        * pontuação de risco da mensagem
        * presença de palavras-chave críticas

Compatibilidade:
    - Mantém a classe IncidentFlagger (estilo TESE V8).
    - Adiciona a função flag_incidents(messages) (estilo TESE V9),
      usada pelo engine_bridge.run_full_analysis.

Espera-se que cada mensagem tenha, idealmente:
    - "text" ou "content"  -> texto da mensagem
    - "scores" -> dict com pelo menos "risk" (float) quando vier do message_scorer

A função flag_incidents é defensiva: funciona mesmo se esses campos
não existirem, usando defaults neutros.
"""

from typing import Dict, List, Any


Message = Dict[str, Any]


class IncidentFlagger:
    """
    Detects incidents based on message scoring + rule triggers.
    """

    def __init__(self) -> None:
        # Threshold de risco (pode ser ajustado depois se necessário)
        self.threshold: float = 7.0

        # Palavras-chave que indicam possível incidente grave.
        # Pode ser customizado posteriormente ou extraído de configuração.
        self.critical_keywords: List[str] = [
            "attack",
            "leak",
            "fraud",
            "harm",
            "blackmail",
            "threat",
            "extortion",
        ]

    def _extract_text(self, message: Message) -> str:
        """
        Extrai o texto principal da mensagem de forma tolerante.
        """
        text = (
            message.get("content")
            or message.get("text")
            or ""
        )
        if not isinstance(text, str):
            text = str(text)
        return text

    def _extract_score(self, message: Message) -> float:
        """
        Extrai a pontuação de risco da mensagem.

        Prioridade:
            1) message["score"]
            2) message["scores"]["risk"]
            3) default 0.0
        """
        # 1) Campo direto "score"
        raw = message.get("score")

        # 2) Campo aninhado em "scores"
        if raw is None and isinstance(message.get("scores"), dict):
            raw = message["scores"].get("risk")

        # 3) Fallback numérico
        try:
            return float(raw) if raw is not None else 0.0
        except (TypeError, ValueError):
            return 0.0

    def evaluate(self, message: Message) -> Dict[str, Any]:
        """
        Avalia UMA mensagem e retorna um dict com:
            {
                "incident": bool,
                "triggers": List[str],
                "severity": "low" | "medium" | "high",
                "score": float
            }

        Esta é a API "clássica" do TESE V8, usada agora também
        pela camada funcional do TESE V9.
        """
        text = self._extract_text(message).lower()
        score = self._extract_score(message)

        triggered: List[str] = []

        # Palavras-chave críticas encontradas
        for kw in self.critical_keywords:
            if kw.lower() in text:
                triggered.append(kw)

        # Threshold numérico
        if score >= self.threshold:
            triggered.append("threshold_exceeded")

        # Severidade heurística simples
        if any(kw.lower() in text for kw in self.critical_keywords):
            severity = "high"
        elif score >= self.threshold:
            severity = "medium"
        else:
            severity = "low"

        return {
            "incident": len(triggered) > 0,
            "triggers": triggered,
            "severity": severity,
            "score": score,
        }


# ---------------------------------------------------------------------------
# Função funcional para TESE V9 - usada pelo engine_bridge
# ---------------------------------------------------------------------------

def flag_incidents(messages: List[Message]) -> List[Message]:
    """
    Função de alto nível usada pela pipeline TESE V9:

        flagged_messages = flag_incidents(scored_messages)

    Responsabilidade:
        - Percorrer a lista de mensagens
        - Rodar IncidentFlagger().evaluate(msg) em cada uma
        - Preencher/atualizar:
            * msg["flags"]  -> lista de "gatilhos" / marcadores
            * msg["incident_analysis"] -> detalhes da avaliação

    Comportamento:
        - Não levanta exceções (defensivo).
        - Aceita qualquer lista; ignora entradas não-dict.
        - Não modifica a lista original; retorna uma nova lista.
    """
    if not isinstance(messages, list):
        # Defesa: se algo vier errado, devolve lista vazia
        return []

    flagger = IncidentFlagger()
    flagged: List[Message] = []

    for msg in messages:
        if not isinstance(msg, dict):
            # Ignora entradas inválidas
            continue

        # Cópia rasa para não mutar o original
        m = dict(msg)

        try:
            inc_result = flagger.evaluate(m)
        except Exception:
            # Em caso de qualquer problema na avaliação, continua sem incidentes
            inc_result = {
                "incident": False,
                "triggers": [],
                "severity": "low",
                "score": 0.0,
            }

        # Garante que exista lista de flags
        existing_flags = m.get("flags")
        if existing_flags is None:
            flags_list: List[str] = []
        elif isinstance(existing_flags, list):
            flags_list = list(existing_flags)
        else:
            flags_list = [str(existing_flags)]

        # Se houve incidente, adiciona os gatilhos como flags
        if inc_result.get("incident"):
            for trig in inc_result.get("triggers", []):
                if trig not in flags_list:
                    flags_list.append(trig)

        m["flags"] = flags_list
        m["incident_analysis"] = inc_result

        flagged.append(m)

    return flagged
