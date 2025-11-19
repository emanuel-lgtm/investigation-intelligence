"""
TESE V9 - UI Integration Helpers

Gera uma estrutura de quiz para consumo pela UI (por exemplo, para
treinamento ou revisão de incidentes).

Compatibilidade:
    - Expõe a função generate_quiz(analysis_data),
      importada por engine_bridge.create_quiz.
"""

from typing import Any, Dict, List


Question = Dict[str, Any]


def generate_quiz(analysis_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Gera um pequeno quiz baseado no resumo de risco do caso.

    Parâmetro:
        analysis_data: dicionário retornado por run_full_analysis, contendo
            - "risk_summary": {"incident_counts": {...}, ...}
            - opcionalmente "patterns": {...}

    Retorna:
        {
            "title": "TESE Case Review Quiz",
            "questions": [
                {
                    "prompt": "string",
                    "options": ["A", "B", "C", "D"],
                    "answer_index": 0
                },
                ...
            ]
        }
    """
    if not isinstance(analysis_data, dict):
        analysis_data = {}

    risk_summary = analysis_data.get("risk_summary", {}) or {}
    incident_counts = risk_summary.get("incident_counts", {}) or {}

    patterns = analysis_data.get("patterns", {}) or {}
    top_keywords = patterns.get("top_keywords", []) or []
    top_senders = patterns.get("top_senders", []) or []

    questions: List[Question] = []

    # -------------------------------------------------
    # Pergunta 1: distribuição de severidade
    # -------------------------------------------------
    if incident_counts:
        high = incident_counts.get("high", 0)
        medium = incident_counts.get("medium", 0)
        low = incident_counts.get("low", 0)

        prompt = (
            "De acordo com a análise TESE, qual nível de severidade apresentou "
            "o maior número de incidentes?"
        )
        options = [
            f"Alta ({high})",
            f"Média ({medium})",
            f"Baixa ({low})",
            "Todos têm praticamente a mesma contagem",
        ]

        counts = [high, medium, low]
        max_count = max(counts)
        if counts.count(max_count) == 1:
            correct_index = counts.index(max_count)
        else:
            correct_index = 3  # empate → opção "todos parecidos"

        questions.append(
            {
                "prompt": prompt,
                "options": options,
                "answer_index": correct_index,
            }
        )

    # -------------------------------------------------
    # Pergunta 2 (opcional): palavra-chave mais frequente
    # -------------------------------------------------
    if top_keywords:
        # Considera a primeira como a mais relevante
        top_kw, top_kw_count = top_keywords[0]
        prompt = (
            "Qual das seguintes palavras-chave foi destacada como uma das mais "
            "frequentes nos incidentes deste caso?"
        )

        # constrói opções a partir das top keywords (até 4)
        opts = [kw for kw, _ in top_keywords[:4]]
        # garante que a palavra correta esteja na lista
        if top_kw not in opts:
            opts.append(top_kw)

        # remove duplicadas mantendo ordem
        seen = set()
        options = []
        for o in opts:
            if o not in seen:
                seen.add(o)
                options.append(o)

        # índice da resposta correta
        correct_index = options.index(top_kw)

        questions.append(
            {
                "prompt": prompt,
                "options": options,
                "answer_index": correct_index,
            }
        )

    # -------------------------------------------------
    # Pergunta 3 (opcional): participante chave
    # -------------------------------------------------
    if top_senders:
        top_sender, _ = top_senders[0]
        prompt = (
            "Qual participante parece ter papel central nas comunicações "
            "analisadas neste caso?"
        )

        opts = [sender for sender, _ in top_senders[:4]]
        if top_sender not in opts:
            opts.append(top_sender)

        seen = set()
        options = []
        for o in opts:
            if o not in seen:
                seen.add(o)
                options.append(o)

        correct_index = options.index(top_sender)

        questions.append(
            {
                "prompt": prompt,
                "options": options,
                "answer_index": correct_index,
            }
        )

    # Fallback se nada foi gerado
    if not questions:
        questions.append(
            {
                "prompt": "Qual é a principal conclusão em relação aos riscos identificados neste caso?",
                "options": [
                    "Não há sinais claros de risco; uma revisão manual é recomendada.",
                    "Há múltiplos incidentes graves exigindo ação imediata.",
                    "A análise indica apenas problemas menores, sem necessidade de ação.",
                    "O sistema não conseguiu processar os dados do caso.",
                ],
                "answer_index": 0,
            }
        )

    return {
        "title": "TESE Case Review Quiz",
        "questions": questions,
    }
