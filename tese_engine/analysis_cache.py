"""
TESE V9 - Analysis Cache

Cache de resultados de análise para conjuntos de arquivos grandes.

Ideia:
    - Cada conjunto de arquivos enviados gera uma chave de cache (hash).
    - Se o mesmo conjunto for analisado de novo, reaproveitamos:
        * parsed_by_platform
        * analysis

Formato de armazenamento (JSON em data/analysis_cache.json):

{
  "cache_key_1": {
    "files": [
      {"name": "export_whatsapp.txt", "sha256": "..."},
      {"name": "slack_export.json", "sha256": "..."}
    ],
    "parsed_by_platform": {...},
    "analysis": {...},
    "created_at": "2025-11-19T10:12:00",
    "version": "v9.0.0"
  },
  ...
}
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Tuple, Optional


# Versão do pipeline – se mudar algo estrutural grande, podemos usar
# para invalidar cache antigo manualmente.
CACHE_VERSION = "v9.0.0"


def _get_project_root() -> Path:
    """
    Retorna o diretório raiz do projeto:
        /Applications/TESE/TESE v9/investigation-system
    (assumindo que este arquivo está em tese_engine/)
    """
    return Path(__file__).resolve().parents[1]


def _get_cache_path() -> Path:
    root = _get_project_root()
    data_dir = root / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir / "analysis_cache.json"


def _sha256_bytes(data: bytes) -> str:
    h = hashlib.sha256()
    h.update(data)
    return h.hexdigest()


def compute_fileset_hash(uploaded_files: List[Any]) -> Tuple[str, List[Dict[str, Any]]]:
    """
    Gera uma chave de cache para um CONJUNTO de arquivos.

    - Para cada arquivo:
        * lê bytes via file.getvalue() (Streamlit/UploadedFile)
        * calcula sha256 individual
    - Combina todos os hashes em uma única string:
        cache_key = sha256("name1:hash1|name2:hash2|...")

    Retorna:
        (cache_key, files_meta)
    """
    if not uploaded_files:
        return "EMPTY_FILES", []

    parts: List[str] = []
    files_meta: List[Dict[str, Any]] = []

    for f in uploaded_files:
        # Tenta obter bytes sem consumir stream
        try:
            raw = f.getvalue()
        except Exception:
            # Fallback defensivo
            raw = getattr(f, "read", lambda: b"")()
        if raw is None:
            raw = b""

        file_hash = _sha256_bytes(raw)
        name = getattr(f, "name", "unknown")

        files_meta.append(
            {
                "name": str(name),
                "sha256": file_hash,
            }
        )
        parts.append(f"{name}:{file_hash}")

    combined = "|".join(parts).encode("utf-8")
    cache_key = _sha256_bytes(combined)
    return cache_key, files_meta


def _load_cache_raw() -> Dict[str, Any]:
    path = _get_cache_path()
    if not path.exists():
        return {}
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _save_cache_raw(cache: Dict[str, Any]) -> None:
    path = _get_cache_path()
    try:
        with path.open("w", encoding="utf-8") as f:
            json.dump(cache, f, ensure_ascii=False)
    except Exception:
        # Não podemos falhar a análise só por não conseguir salvar cache
        pass


def get_cached_result(cache_key: str) -> Optional[Dict[str, Any]]:
    """
    Retorna o registro de cache para a chave dada, ou None se não existir.
    """
    cache = _load_cache_raw()
    entry = cache.get(cache_key)
    if not entry:
        return None

    # Opcional: checar versão para invalidar cache antigo
    if entry.get("version") != CACHE_VERSION:
        return None

    return entry


def set_cached_result(
    cache_key: str,
    files_meta: List[Dict[str, Any]],
    parsed_by_platform: Dict[str, Any],
    analysis: Dict[str, Any],
) -> None:
    """
    Armazena resultado no cache.
    """
    cache = _load_cache_raw()
    cache[cache_key] = {
        "files": files_meta,
        "parsed_by_platform": parsed_by_platform,
        "analysis": analysis,
        "created_at": datetime.utcnow().isoformat(),
        "version": CACHE_VERSION,
    }
    _save_cache_raw(cache)
