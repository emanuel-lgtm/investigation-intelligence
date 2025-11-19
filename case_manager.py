# case_manager.py
# Gerenciamento de "cases" para o TESE V9
#
# Responsabilidades:
#   - Criar casos novos (estrutura padrão)
#   - Carregar casos do disco (JSON)
#   - Salvar casos no disco
#   - Helpers para status, exports e histórico (history)

from __future__ import annotations

import json
import re
from pathlib import Path
from datetime import date, datetime
from typing import List, Dict, Any, Optional


# --------------------------------------------------------------------
# Caminho padrão do arquivo de cases
# --------------------------------------------------------------------

def _get_project_root() -> Path:
    """
    Retorna o diretório raiz do projeto:
        /Applications/TESE/TESE v9/investigation-system
    (assumindo que este arquivo está na raiz do projeto).
    """
    return Path(__file__).resolve().parent


def get_cases_path() -> Path:
    """
    Caminho padrão do arquivo JSON de cases:
        data/cases.json
    """
    root = _get_project_root()
    data_dir = root / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir / "cases.json"


# --------------------------------------------------------------------
# Serialização / desserialização de datas
# --------------------------------------------------------------------

def _serialize_date(d: date) -> str:
    return d.isoformat()


def _deserialize_date(value: Any) -> date:
    """
    Converte uma string ISO (YYYY-MM-DD) em date.
    Se não for possível, retorna date.today() como fallback.
    """
    if isinstance(value, date):
        return value
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, str):
        try:
            return date.fromisoformat(value)
        except Exception:
            return date.today()
    return date.today()


# --------------------------------------------------------------------
# Normalização de case_id
# --------------------------------------------------------------------

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


# --------------------------------------------------------------------
# Leitura / escrita de lista de cases
# --------------------------------------------------------------------

def _deserialize_cases(raw_list: Any) -> List[Dict[str, Any]]:
    """
    Converte lista crua lida do JSON em lista de cases com tipos adequados.
    Garante campos obrigatórios e defaults.
    """
    if not isinstance(raw_list, list):
        return []

    cases: List[Dict[str, Any]] = []
    for raw in raw_list:
        if not isinstance(raw, dict):
            continue

        name = raw.get("name") or "Case"
        owner = raw.get("owner")
        sources = raw.get("sources") or []
        created_raw = raw.get("created")

        created = _deserialize_date(created_raw)

        # Novo: case_id (id estável)
        raw_id = raw.get("id") or name
        case_id = _make_safe_case_id(raw_id)

        # Novo: status, tags, summary, exports, last_updated_at, history
        status = raw.get("status") or "new"
        tags = raw.get("tags") or []
        summary = raw.get("summary") or ""

        exports = raw.get("exports") or {
            "pdf": None,
            "json_summary": None,
            "json_messages": None,
            "bundle": None,
        }

        last_updated_raw = raw.get("last_updated_at")
        last_updated_at = _deserialize_date(last_updated_raw)

        history_raw = raw.get("history") or []
        history: List[Dict[str, Any]] = []
        if isinstance(history_raw, list):
            for ev in history_raw:
                if isinstance(ev, dict):
                    history.append(ev)

        files = raw.get("files") or []

        case = {
            "id": case_id,
            "name": name,
            "sources": sources,
            "created": created,
            "owner": owner,
            "files": files,
            "status": status,
            "tags": tags,
            "summary": summary,
            "exports": exports,
            "last_updated_at": last_updated_at,
            "history": history,
        }
        cases.append(case)

    return cases


def _serialize_cases(cases: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Converte lista de cases em estrutura pronta para JSON, serializando datas.
    """
    serialized: List[Dict[str, Any]] = []
    for c in cases:
        c_copy = dict(c)

        created_val = c_copy.get("created")
        if isinstance(created_val, (date, datetime)):
            c_copy["created"] = _serialize_date(
                created_val.date() if isinstance(created_val, datetime) else created_val
            )

        last_val = c_copy.get("last_updated_at")
        if isinstance(last_val, (date, datetime)):
            c_copy["last_updated_at"] = _serialize_date(
                last_val.date() if isinstance(last_val, datetime) else last_val
            )

        # garante que exports exista com todas as chaves esperadas
        exports = c_copy.get("exports") or {}
        exports = {
            "pdf": exports.get("pdf"),
            "json_summary": exports.get("json_summary"),
            "json_messages": exports.get("json_messages"),
            "bundle": exports.get("bundle"),
        }
        c_copy["exports"] = exports

        # history pode ser mantido como lista de dicts
        history = c_copy.get("history")
        if not isinstance(history, list):
            c_copy["history"] = []
        serialized.append(c_copy)

    return serialized


def load_cases() -> List[Dict[str, Any]]:
    """
    Carrega todos os cases do disco.
    Se o arquivo não existir, retorna lista vazia.
    """
    path = get_cases_path()
    if not path.exists():
        return []

    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return []

    return _deserialize_cases(raw)


def save_cases(cases: List[Dict[str, Any]]) -> None:
    """
    Salva todos os cases no disco em formato JSON.
    """
    path = get_cases_path()
    serialized = _serialize_cases(cases)
    path.write_text(json.dumps(serialized, ensure_ascii=False, indent=2), encoding="utf-8")


# --------------------------------------------------------------------
# Criação de novo case
# --------------------------------------------------------------------

def create_case(
    name: str,
    sources: Optional[List[str]] = None,
    owner: Optional[str] = None,
    created: Optional[date] = None,
) -> Dict[str, Any]:
    """
    Cria um novo case com a estrutura padrão.
    """
    if created is None:
        created = date.today()

    sources = sources or []

    # Gera um id seguro a partir do nome + data (evita colisões simples)
    base_id = f"{name}_{created.isoformat()}"
    case_id = _make_safe_case_id(base_id)

    new_case: Dict[str, Any] = {
        "id": case_id,
        "name": name,
        "sources": sources,
        "created": created,
        "owner": owner,
        "files": [],
        "status": "new",
        "tags": [],
        "summary": "",
        "exports": {
            "pdf": None,
            "json_summary": None,
            "json_messages": None,
            "bundle": None,
        },
        "last_updated_at": created,
        "history": [],
    }

    return new_case


# --------------------------------------------------------------------
# Helpers opcionais para atualizar status / exports / histórico
# --------------------------------------------------------------------

def update_case_status(
    cases: List[Dict[str, Any]],
    index: int,
    new_status: str,
) -> List[Dict[str, Any]]:
    """
    Atualiza o status de um case na lista e last_updated_at.
    """
    if 0 <= index < len(cases):
        cases[index]["status"] = new_status
        cases[index]["last_updated_at"] = date.today()
    return cases


def attach_exports_to_case(
    cases: List[Dict[str, Any]],
    index: int,
    *,
    pdf_path: Optional[str] = None,
    json_summary_path: Optional[str] = None,
    json_messages_path: Optional[str] = None,
    bundle_path: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Atualiza os caminhos de exports de um case na lista.
    """
    if 0 <= index < len(cases):
        exports = cases[index].get("exports") or {}
        exports.setdefault("pdf", None)
        exports.setdefault("json_summary", None)
        exports.setdefault("json_messages", None)
        exports.setdefault("bundle", None)

        if pdf_path is not None:
            exports["pdf"] = pdf_path
        if json_summary_path is not None:
            exports["json_summary"] = json_summary_path
        if json_messages_path is not None:
            exports["json_messages"] = json_messages_path
        if bundle_path is not None:
            exports["bundle"] = bundle_path

        cases[index]["exports"] = exports
        cases[index]["last_updated_at"] = date.today()

    return cases


def log_case_event(
    cases: List[Dict[str, Any]],
    index: int,
    event_type: str,
    details: Optional[Dict[str, Any]] = None,
) -> List[Dict[str, Any]]:
    """
    Adiciona um evento ao histórico (history) de um case.

    Exemplo de uso:
        log_case_event(cases, idx, "analysis_run", {"num_messages": 1234})
        log_case_event(cases, idx, "export", {"bundle": ".../case_001.tese"})

    Cada entrada terá forma:
        {
            "type": "analysis_run" | "export" | ...,
            "timestamp": "2025-11-19T10:12:00",
            "details": {...}
        }
    """
    if 0 <= index < len(cases):
        history = cases[index].get("history")
        if not isinstance(history, list):
            history = []
        event = {
            "type": event_type,
            "timestamp": datetime.utcnow().isoformat(),
            "details": details or {},
        }
        history.append(event)
        cases[index]["history"] = history
        cases[index]["last_updated_at"] = date.today()

    return cases
