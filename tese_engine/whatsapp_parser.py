"""
tese_engine.whatsapp_parser

Simple WhatsApp chat export parser for TESE V9 integration.

Expected to be called via:
    from tese_engine.whatsapp_parser import parse_whatsapp

parse_whatsapp(file_obj) receives a Streamlit file_uploader object
and returns a dict:
{
    "platform": "whatsapp",
    "messages": [...],
    "meta": {...},
}
"""

import re
from datetime import datetime
from typing import List, Dict, Any


# Regex para formatos comuns de export do WhatsApp
# Exemplos:
#   [12/11/2025, 21:45] João: mensagem
#   12/11/2025, 21:45 - João: mensagem
WHATSAPP_LINE_RE = re.compile(
    r"""
    ^                               # início da linha
    (?:\[)?                         # abre colchete opcional
    (?P<date>\d{1,2}/\d{1,2}/\d{2,4})  # data 12/11/2025
    ,\s+
    (?P<time>\d{1,2}:\d{2}(?::\d{2})?)  # hora 21:45 ou 21:45:02
    (?:\])?                         # fecha colchete opcional
    \s*[-–]?\s*                     # hífen/traço opcional
    (?P<sender>[^:]+?):\s+          # nome do remetente até dois pontos
    (?P<content>.+)                 # conteúdo da mensagem
    $
    """,
    re.VERBOSE,
)


def _parse_datetime(date_str: str, time_str: str) -> str:
    """
    Tenta converter strings de data/hora em ISO 8601.
    Se falhar, retorna string vazia.
    """
    for fmt in ("%d/%m/%Y %H:%M", "%d/%m/%y %H:%M", "%m/%d/%Y %H:%M", "%m/%d/%y %H:%M",
                "%d/%m/%Y %H:%M:%S", "%d/%m/%y %H:%M:%S", "%m/%d/%Y %H:%M:%S", "%m/%d/%y %H:%M:%S"):
        try:
            dt = datetime.strptime(f"{date_str} {time_str}", fmt)
            return dt.isoformat()
        except ValueError:
            continue
    return ""


def _parse_whatsapp_text(content: str) -> List[Dict[str, Any]]:
    """
    Faz o parsing linha a linha do texto bruto do WhatsApp
    e retorna uma lista de mensagens normalizadas.
    """
    messages: List[Dict[str, Any]] = []
    current_msg = None
    msg_id = 0

    for raw_line in content.splitlines():
        line = raw_line.strip()
        if not line:
            continue

        m = WHATSAPP_LINE_RE.match(line)
        if m:
            # Nova mensagem
            msg_id += 1
            if current_msg is not None:
                messages.append(current_msg)

            d = m.groupdict()
            ts_iso = _parse_datetime(d["date"], d["time"])

            current_msg = {
                "id": msg_id,
                "platform": "whatsapp",
                "timestamp": ts_iso,
                "sender": d["sender"].strip(),
                "content": d["content"].strip(),
                "raw_line": raw_line,
            }
        else:
            # Continuação de mensagem anterior (mensagens quebradas em várias linhas)
            if current_msg is not None:
                current_msg["content"] += "\n" + raw_line
            else:
                # Linha fora de formato conhecido – salva como mensagem avulsa
                msg_id += 1
                current_msg = {
                    "id": msg_id,
                    "platform": "whatsapp",
                    "timestamp": "",
                    "sender": "",
                    "content": raw_line,
                    "raw_line": raw_line,
                }

    if current_msg is not None:
        messages.append(current_msg)

    return messages


def parse_whatsapp(file_obj) -> Dict[str, Any]:
    """
    Função principal esperada pelo engine_bridge.
    file_obj é o objeto retornado pelo st.file_uploader (possui .read()).

    Retorna:
    {
        "platform": "whatsapp",
        "messages": [...],
        "meta": {
            "filename": ...,
            "total_messages": ...,
        }
    }
    """
    try:
        # Streamlit UploadedFile -> bytes
        raw_bytes = file_obj.read()
        try:
            text = raw_bytes.decode("utf-8", errors="replace")
        except Exception:
            # fallback simples
            text = raw_bytes.decode("latin-1", errors="replace")

        messages = _parse_whatsapp_text(text)

        return {
            "platform": "whatsapp",
            "messages": messages,
            "meta": {
                "filename": getattr(file_obj, "name", "unknown"),
                "total_messages": len(messages),
            },
        }

    except Exception as e:
        return {
            "platform": "whatsapp",
            "messages": [],
            "error": f"Error parsing WhatsApp file: {str(e)}",
        }
