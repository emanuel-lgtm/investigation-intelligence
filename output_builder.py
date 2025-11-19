# output_builder.py
# Gera todas as saídas (reports, mindmap, vídeos, áudio, flashcards, quiz)
# usando o resultado da análise TESE V8 e o engine_bridge.
#
# Integra também:
#   - JSON exporter (case_summary.json, messages.json)
#   - Bundle exporter (.tese light bundle)
#   - PDF exporter (relatório TESE em PDF)
#   - Helper build_all_outputs_for_case(...) que conecta um "case" (case_manager)
#     com um case_id estável para todos os exports.

from typing import Any, Dict, Optional
from pathlib import Path
import re

from engine_bridge import (
    create_report,
    create_mindmap,
    create_video_overview,
    create_flashcards,
    create_quiz,
    create_audio_overview,
)

from tese_engine.json_exporter import (
    export_case_summary_json,
    export_messages_json,
)
from tese_engine.bundle_exporter import create_light_bundle
from tese_engine.pdf_exporter import export_to_pdf


# -----------------------------------------------------------
# HELPERS INTERNOS
# -----------------------------------------------------------

def _get_project_root() -> Path:
    """
    Retorna o diretório raiz do projeto:
        /Applications/TESE/TESE v9/investigation-system
    (assumindo que este arquivo está na raiz do projeto).
    """
    return Path(__file__).resolve().parent


def _get_case_dir(case_id: str) -> Path:
    """
    Diretório padrão para armazenar artefatos de um caso específico.
    Exemplo:
        data/cases/<case_id>/
    """
    root = _get_project_root()
    return root / "data" / "cases" / case_id


def _get_bundle_path(case_id: str) -> Path:
    """
    Caminho padrão para o bundle .tese de um caso específico.
    Exemplo:
        data/bundles/<case_id>.tese
    """
    root = _get_project_root()
    bundles_dir = root / "data" / "bundles"
    bundles_dir.mkdir(parents=True, exist_ok=True)
    return bundles_dir / f"{case_id}.tese"


def _get_pdf_path(case_id: str) -> Path:
    """
    Caminho padrão para o PDF de relatório de um caso específico.
    Exemplo:
        data/reports/<case_id>.pdf
    """
    root = _get_project_root()
    reports_dir = root / "data" / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    return reports_dir / f"{case_id}.pdf"


def _make_safe_case_id(raw: Optional[str]) -> str:
    """
    Normaliza um identificador de caso para algo seguro em paths:
        - lowercase
        - espaços e caracteres estranhos -> "_"
        - remove "_" extras nas pontas

    Se raw for vazio/None, cai em "case".
    """
    if not raw:
        base = "case"
    else:
        base = str(raw).strip().lower()

    # troca qualquer coisa que não seja [a-z0-9_-] por "_"
    safe = re.sub(r"[^a-z0-9_-]+", "_", base)
    safe = safe.strip("_")
    return safe or "case"


# -----------------------------------------------------------
# FUNÇÕES DE SAÍDA (CHAMADAS PELA UI E PELO STUDIO PANEL)
# -----------------------------------------------------------

def build_report(analysis_data: Dict[str, Any]) -> str:
    """
    Retorna conteúdo bruto do relatório TESE (string grande).
    O app.py decide como exibir ou exportar.
    """
    try:
        return create_report(analysis_data)
    except Exception as e:
        return f"ERROR generating report: {str(e)}"


def build_mindmap(analysis_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Retorna estrutura de mindmap (geralmente dict com nodes e links).
    """
    try:
        return create_mindmap(analysis_data)
    except Exception as e:
        return {
            "error": True,
            "message": f"ERROR generating mindmap: {str(e)}"
        }


def build_video_script(analysis_data: Dict[str, Any]) -> str:
    """
    Retorna roteiro bruto para vídeo overview.
    """
    try:
        return create_video_overview(analysis_data)
    except Exception as e:
        return f"ERROR generating video overview: {str(e)}"


def build_flashcards(analysis_data: Dict[str, Any]) -> Any:
    """
    Retorna flashcards (lista de cards ou dict com erro).
    """
    try:
        return create_flashcards(analysis_data)
    except Exception as e:
        return {
            "error": True,
            "message": f"ERROR generating flashcards: {str(e)}"
        }


def build_quiz(analysis_data: Dict[str, Any]) -> Any:
    """
    Retorna perguntas e respostas para quiz.
    """
    try:
        return create_quiz(analysis_data)
    except Exception as e:
        return {
            "error": True,
            "message": f"ERROR generating quiz: {str(e)}"
        }


def build_audio_overview(analysis_data: Dict[str, Any]) -> str:
    """
    Retorna texto para ser passado para um TTS real.
    A versão atual usa placeholder do engine_bridge.
    """
    try:
        return create_audio_overview(analysis_data)
    except Exception as e:
        return f"ERROR generating audio overview: {str(e)}"


# -----------------------------------------------------------
# EXPORT JSON (SUMMARY + MESSAGES)
# -----------------------------------------------------------

def export_case_json_outputs(
    analysis_data: Dict[str, Any],
    mindmap_data: Optional[Dict[str, Any]],
    case_id: str,
    include_messages: bool = True,
) -> Dict[str, Any]:
    """
    Gera JSONs padrão do caso em disco:

        data/cases/<case_id>/case_summary.json
        data/cases/<case_id>/messages.json (opcional)

    Parâmetros:
        analysis_data : dict retornado por run_full_analysis
        mindmap_data  : dict retornado por build_mindmap (pode ser None)
        case_id       : identificador do caso (ex: "case_001")
        include_messages : se True, também exporta messages.json

    Retorna:
        {
            "summary_path": "str ou None",
            "messages_path": "str ou None",
            "error": None | "mensagem de erro"
        }
    """
    case_dir = _get_case_dir(case_id)
    summary_path = case_dir / "case_summary.json"
    messages_path = case_dir / "messages.json"

    result: Dict[str, Any] = {
        "summary_path": None,
        "messages_path": None,
        "error": None,
    }

    try:
        # Exporta summary compacto (incident_counts, patterns, platforms, timeline_summary, mindmap)
        export_case_summary_json(
            analysis_data=analysis_data,
            mindmap=mindmap_data,
            output_path=summary_path,
        )
        result["summary_path"] = str(summary_path)
    except Exception as e:
        result["error"] = f"ERROR exporting case_summary.json: {e}"
        # Se der erro aqui, não tentamos messages.json
        return result

    if include_messages:
        try:
            export_messages_json(
                analysis_data=analysis_data,
                output_path=messages_path,
            )
            result["messages_path"] = str(messages_path)
        except Exception as e:
            # Summary continua válido; só marcamos erro parcial.
            result["error"] = f"ERROR exporting messages.json: {e}"

    return result


# -----------------------------------------------------------
# EXPORT BUNDLE .TESE (LIGHT)
# -----------------------------------------------------------

def export_tese_bundle(
    analysis_data: Dict[str, Any],
    outputs: Dict[str, Any],
    case_id: str,
    include_messages: bool = True,
    extra_meta: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Cria um bundle .tese "light" para o caso, contendo:

        case/meta.json
        case/analysis.json
        case/summary/case_summary.json
        case/summary/messages.json (opcional)
        case/exports/report.txt
        case/exports/video_script.txt
        case/exports/flashcards.json
        case/exports/quiz.json

    Parâmetros:
        analysis_data: dict retornado por run_full_analysis
        outputs: dict com:
            {
                "report": str,
                "mindmap": dict,
                "video_script": str,
                "flashcards": list ou dict,
                "quiz": dict
            }
        case_id: identificador do caso ("case_001", "proj_alpha_2025" etc.)
        include_messages: se True, inclui messages.json com todas as mensagens
        extra_meta: metadados adicionais para meta.json (tags, status, etc.)

    Retorna:
        {
            "bundle_path": "str ou None",
            "error": None | "mensagem de erro"
        }
    """
    bundle_path = _get_bundle_path(case_id)

    result: Dict[str, Any] = {
        "bundle_path": None,
        "error": None,
    }

    try:
        create_light_bundle(
            case_id=case_id,
            analysis_data=analysis_data,
            outputs=outputs,
            bundle_path=bundle_path,
            include_messages=include_messages,
            extra_meta=extra_meta,
        )
        result["bundle_path"] = str(bundle_path)
    except Exception as e:
        result["error"] = f"ERROR creating .tese bundle: {e}"

    return result


# -----------------------------------------------------------
# EXPORT PDF
# -----------------------------------------------------------

def export_case_pdf(
    analysis_data: Dict[str, Any],
    report_text: str,
    case_id: str,
) -> Dict[str, Any]:
    """
    Gera um PDF de relatório para o caso:

        data/reports/<case_id>.pdf

    Retorna:
        {
            "pdf_path": "str ou None",
            "error": None | "mensagem de erro"
        }
    """
    pdf_path = _get_pdf_path(case_id)

    result: Dict[str, Any] = {
        "pdf_path": None,
        "error": None,
    }

    try:
        final_path = export_to_pdf(analysis_data, report_text, pdf_path)
        result["pdf_path"] = str(final_path)
    except Exception as e:
        result["error"] = f"ERROR exporting PDF: {e}"

    return result


# -----------------------------------------------------------
# HELPER: CONECTAR UM "CASE" (case_manager) AO case_id E EXPORTS
# -----------------------------------------------------------

def build_all_outputs_for_case(
    case: Dict[str, Any],
    analysis_data: Dict[str, Any],
    include_messages: bool = True,
) -> Dict[str, Any]:
    """
    Helper backend-only.

    Recebe:
        - um dict de case (como retornado por case_manager.load_cases()[i])
        - o analysis_data retornado por run_full_analysis

    Faz:
        - Deriva um case_id estável (usando case["id"] se existir, senão o name)
        - Gera todas as saídas: report, mindmap, video_script, flashcards, quiz, audio
        - Exporta JSONs (summary + messages) usando esse case_id
        - Exporta bundle .tese usando esse case_id
        - Exporta PDF de relatório para esse case_id

    Retorna:
        {
            "case_id": str,
            "report": str,
            "mindmap": dict,
            "video_script": str,
            "flashcards": Any,
            "quiz": Any,
            "audio": str,
            "json_exports": {...},
            "bundle_export": {...},
            "pdf_export": {...},
        }
    """
    # 1) Deriva case_id
    raw_id = case.get("id") or case.get("name") or "case"
    case_id = _make_safe_case_id(raw_id)

    # 2) Gera outputs em memória usando as funções já usadas pela UI
    report = build_report(analysis_data)
    mindmap = build_mindmap(analysis_data)
    video_script = build_video_script(analysis_data)
    flashcards = build_flashcards(analysis_data)
    quiz = build_quiz(analysis_data)
    audio = build_audio_overview(analysis_data)

    outputs = {
        "report": report,
        "mindmap": mindmap,
        "video_script": video_script,
        "flashcards": flashcards,
        "quiz": quiz,
    }

    # 3) Exporta JSONs (summary + messages)
    json_exports = export_case_json_outputs(
        analysis_data=analysis_data,
        mindmap_data=mindmap,
        case_id=case_id,
        include_messages=include_messages,
    )

    # 4) Exporta bundle .tese
    extra_meta = {
        "name": case.get("name"),
        "owner": case.get("owner"),
        "sources": case.get("sources"),
    }

    bundle_export = export_tese_bundle(
        analysis_data=analysis_data,
        outputs=outputs,
        case_id=case_id,
        include_messages=include_messages,
        extra_meta=extra_meta,
    )

    # 5) Exporta PDF de relatório
    pdf_export = export_case_pdf(
        analysis_data=analysis_data,
        report_text=report,
        case_id=case_id,
    )

    return {
        "case_id": case_id,
        "report": report,
        "mindmap": mindmap,
        "video_script": video_script,
        "flashcards": flashcards,
        "quiz": quiz,
        "audio": audio,
        "json_exports": json_exports,
        "bundle_export": bundle_export,
        "pdf_export": pdf_export,
    }
