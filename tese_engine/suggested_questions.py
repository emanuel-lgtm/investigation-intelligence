"""
TESE V9 - Suggested Questions / Flashcards

Gera um conjunto de flashcards (perguntas e respostas curtas)
para apoiar entrevistas e revisão de incidentes.

Compatibilidade:
    - Expõe a função generate_flashcards(analysis_data),
      importada por engine_bridge.create_flashcards.
"""

from typing import Any, Dict, List


Flashcard = Dict[str, str]


def generate_flashcards(analysis_data: Dict[str, Any]) -> List[Flashcard]:
    """
    Gera flashcards simples a partir de padrões e do resumo de risco.

    Parâmetro:
        analysis_data: dicionário retornado por run_full_analysis, contendo
            - "patterns": {"top_keywords": [...], "top_senders": [...]}
            - "risk_summary": {"incident_counts": {...}, ...}

    Retorna:
        Lista de objetos:
            [
                {"question": "...", "answer": "..."},
                ...
            ]
    """
    if not isinstance(analysis_data, dict):
        analysis_data = {}

    patterns = analysis_data.get("patterns", {}) or {}
    risk_summary = analysis_data.get("risk_summary", {}) or {}
    incident_counts = risk_summary.get("incident_counts", {}) or {}

    flashcards: List[Flashcard] = []

    # Pergunta sobre severidade geral
    if incident_counts:
        q = "Quantos incidentes de alta, média e baixa severidade foram detectados?"
        a = (
            f"Alta: {incident_counts.get('high', 0)}, "
            f"Média: {incident_counts.get('medium', 0)}, "
            f"Baixa: {incident_counts.get('low', 0)}."
        )
        flashcards.append({"question": q, "answer": a})

    # Perguntas sobre top keywords / flags
    for kw, count in patterns.get("top_keywords", []) or []:
        q = (
            f"Em que contexto a palavra-chave ou flag '{kw}' aparece com maior frequência?"
        )
        a = (
            f"A palavra-chave/flag '{kw}' aparece em aproximadamente "
            f"{count} mensagens sinalizadas como potencialmente relevantes."
        )
        flashcards.append({"question": q, "answer": a})

    # Perguntas sobre principais remetentes / participantes
    for sender, count in patterns.get("top_senders", []) or []:
        q = f"Qual parece ser o papel de {sender} neste caso?"
        a = (
            f"{sender} aparece em cerca de {count} mensagens e pode ser um "
            f"participante-chave que merece investigação adicional."
        )
        flashcards.append({"question": q, "answer": a})

    # Fallback se nada foi gerado
    if not flashcards:
        flashcards.append(
            {
                "question": "Quais são os principais sinais de risco identificados neste caso?",
                "answer": (
                    "A análise automatizada não destacou padrões específicos; "
                    "uma revisão manual mais detalhada pode ser necessária."
                ),
            }
        )

    return flashcards
