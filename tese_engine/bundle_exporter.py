"""
TESE V9 - Bundle Exporter (.tese)

Cria um "bundle" leve de caso TESE em formato .tese (na prática, um .zip),
contendo:

  case/
    meta.json
    analysis.json
    summary/case_summary.json
    summary/messages.json   (opcional)
    exports/report.txt
    exports/video_script.txt
    exports/flashcards.json
    exports/quiz.json

Obs.: este exportador não precisa copiar os arquivos de entrada
(WhatsApp/Slack/Email) para o bundle – isso pode ser feito em um
"full bundle" no futuro. Aqui focamos em grandes volumes, evitando
duplicação gigante de dados.
"""

from __future__ import annotations

import json
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from .json_exporter import (
    build_case_summary_payload,
    build_messages_payload,
)


def _ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def create_light_bundle(
    case_id: str,
    analysis_data: Dict[str, Any],
    outputs: Dict[str, Any],
    bundle_path: Path,
    include_messages: bool = True,
    extra_meta: Optional[Dict[str, Any]] = None,
) -> Path:
    """
    Cria um bundle .tese "light" com JSONs e textos.

    Parâmetros:
        case_id: identificador do caso (string)
        analysis_data: dict retornado por run_full_analysis
        outputs: dict com:
            {
                "report": str,
                "mindmap": dict,
                "video_script": str,
                "flashcards": list,
                "quiz": dict
            }
        bundle_path: caminho final do arquivo .tese (zip)
        include_messages: se True, inclui messages.json com todas as mensagens
        extra_meta: metadados adicionais (tags, status etc.)

    Retorna:
        bundle_path
    """
    _ensure_parent(bundle_path)

    mindmap = outputs.get("mindmap") or {}
    report_text = outputs.get("report") or ""
    video_script = outputs.get("video_script") or ""
    flashcards = outputs.get("flashcards") or []
    quiz = outputs.get("quiz") or {}

    # Meta principal
    meta = {
        "case_id": case_id,
        "exported_at": datetime.utcnow().isoformat(),
    }
    if extra_meta:
        meta.update(extra_meta)

    # Payloads
    summary_payload = build_case_summary_payload(analysis_data, mindmap=mindmap)
    messages_payload: List[Dict[str, Any]] = []
    if include_messages:
        messages_payload = build_messages_payload(analysis_data)

    # Abre zip para escrita
    with zipfile.ZipFile(bundle_path, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
        # meta.json
        zf.writestr(
            "case/meta.json",
            json.dumps(meta, ensure_ascii=False, indent=2),
        )

        # analysis.json (raw analysis_data completo)
        zf.writestr(
            "case/analysis.json",
            json.dumps(analysis_data, ensure_ascii=False, indent=2),
        )

        # summary
        zf.writestr(
            "case/summary/case_summary.json",
            json.dumps(summary_payload, ensure_ascii=False, indent=2),
        )

        if include_messages:
            zf.writestr(
                "case/summary/messages.json",
                json.dumps(messages_payload, ensure_ascii=False, indent=2),
            )

        # exports
        zf.writestr("case/exports/report.txt", report_text)
        zf.writestr("case/exports/video_script.txt", video_script)
        zf.writestr(
            "case/exports/flashcards.json",
            json.dumps(flashcards, ensure_ascii=False, indent=2),
        )
        zf.writestr(
            "case/exports/quiz.json",
            json.dumps(quiz, ensure_ascii=False, indent=2),
        )

    return bundle_path
