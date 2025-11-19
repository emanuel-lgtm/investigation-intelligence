"""
TESE V9 - Analysis Runner

Responsabilidade:
    - Receber arquivos enviados pela UI (Streamlit UploadedFile).
    - Ingerir e detectar plataformas (file_ingestion.ingest_uploaded_files).
    - Rodar o pipeline completo de análise (engine_bridge.run_full_analysis).
    - Integrar com:
        * analysis_cache (para reaproveitar resultados)
        * logging_utils (para diagnósticos)

Retorno principal (contrato com a UI):

    {
        "parsed_by_platform": {
            "whatsapp": [...],
            "slack": [...],
            "email": [...],
            "skype": [...],
            "unknown": [...]
        },
        "analysis": {
            "messages": [...],
            "patterns": {...},
            "correlation": {...},
            "timeline": [...],
            "risk_summary": {...},
            "status": "ok" | "error",
            ...
        },
        "cache": {
            "used": bool,
            "key": str | None,
        }
    }
"""

from __future__ import annotations

from typing import Any, Dict, List

from file_ingestion import ingest_uploaded_files
from engine_bridge import run_full_analysis

from tese_engine.analysis_cache import (
    compute_fileset_hash,
    get_cached_result,
    set_cached_result,
)
from tese_engine.logging_utils import get_logger


logger = get_logger("analysis_runner")


def analyze_uploaded_files(
    uploaded_files: List[Any],
    use_cache: bool = True,
) -> Dict[str, Any]:
    """
    Função de alto nível chamada pela UI.

    Parâmetros:
        uploaded_files: lista de objetos UploadedFile (ou similares).
        use_cache: se True, tenta reaproveitar resultados de cache
                   para o mesmo conjunto de arquivos.

    Retorno:
        Dicionário com parsed_by_platform, analysis e info de cache.
    """
    if not uploaded_files:
        logger.info("analyze_uploaded_files called with no files.")
        return {
            "parsed_by_platform": {},
            "analysis": {
                "messages": [],
                "patterns": {},
                "correlation": {},
                "timeline": [],
                "risk_summary": {},
                "status": "error",
                "error": "No files uploaded.",
            },
            "cache": {"used": False, "key": None},
        }

    # ------------------------------------------------------------------
    # 1) Gera chave de cache para o conjunto de arquivos
    # ------------------------------------------------------------------
    cache_key, files_meta = compute_fileset_hash(uploaded_files)
    logger.info(
        "Starting analysis for fileset.",
        extra={
            "cache_key": cache_key,
            "num_files": len(uploaded_files),
            "files": [m["name"] for m in files_meta],
        },
    )

    # ------------------------------------------------------------------
    # 2) Tenta cache (se habilitado)
    # ------------------------------------------------------------------
    if use_cache:
        cache_entry = get_cached_result(cache_key)
        if cache_entry is not None:
            logger.info(
                "Cache hit for fileset.",
                extra={
                    "cache_key": cache_key,
                    "num_files": len(uploaded_files),
                },
            )
            return {
                "parsed_by_platform": cache_entry.get("parsed_by_platform", {}),
                "analysis": cache_entry.get("analysis", {}),
                "cache": {"used": True, "key": cache_key},
            }

    # ------------------------------------------------------------------
    # 3) Ingestão de arquivos (detecção de plataforma + parsing)
    # ------------------------------------------------------------------
    logger.info(
        "Cache miss (or disabled). Running ingestion and analysis.",
        extra={"cache_key": cache_key},
    )

    try:
        ingestion_result = ingest_uploaded_files(uploaded_files)
    except Exception as e:
        logger.exception("Error during ingestion.")
        return {
            "parsed_by_platform": {},
            "analysis": {
                "messages": [],
                "patterns": {},
                "correlation": {},
                "timeline": [],
                "risk_summary": {},
                "status": "error",
                "error": f"Ingestion failed: {e}",
            },
            "cache": {"used": False, "key": cache_key},
        }

    # ingest_uploaded_files pode devolver diretamente o dict de plataformas
    if isinstance(ingestion_result, dict) and "parsed_by_platform" in ingestion_result:
        parsed_by_platform = ingestion_result["parsed_by_platform"]
    else:
        parsed_by_platform = ingestion_result

    # ------------------------------------------------------------------
    # 4) Pipeline de análise TESE V8 (via engine_bridge)
    # ------------------------------------------------------------------
    try:
        analysis = run_full_analysis(parsed_data_per_platform=parsed_by_platform)
    except Exception as e:
        logger.exception("Error during full analysis.")
        return {
            "parsed_by_platform": parsed_by_platform,
            "analysis": {
                "messages": [],
                "patterns": {},
                "correlation": {},
                "timeline": [],
                "risk_summary": {},
                "status": "error",
                "error": f"Analysis failed: {e}",
            },
            "cache": {"used": False, "key": cache_key},
        }

    # ------------------------------------------------------------------
    # 5) Atualiza cache com resultado (se sucesso)
    # ------------------------------------------------------------------
    if isinstance(analysis, dict) and analysis.get("status") == "ok":
        try:
            set_cached_result(
                cache_key=cache_key,
                files_meta=files_meta,
                parsed_by_platform=parsed_by_platform,
                analysis=analysis,
            )
            logger.info(
                "Analysis result stored in cache.",
                extra={"cache_key": cache_key},
            )
        except Exception:
            logger.exception(
                "Failed to store analysis result in cache.",
                extra={"cache_key": cache_key},
            )

    return {
        "parsed_by_platform": parsed_by_platform,
        "analysis": analysis,
        "cache": {"used": False, "key": cache_key},
    }
