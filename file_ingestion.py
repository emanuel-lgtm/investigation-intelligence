# file_ingestion.py
# Responsável por ingestão de arquivos do usuário via UI
# Chama o engine_bridge.parse_file e monta o dicionário consolidado
# para run_full_analysis()

from engine_bridge import parse_file, detect_file_type


def ingest_uploaded_files(uploaded_files):
    """
    uploaded_files: lista de objetos do Streamlit uploader
    Retorna:
       {
          "whatsapp": [...],
          "slack": [...],
          "skype": [...],
          "email": [...],
          "unknown": [...],
       }
    """

    parsed_by_platform = {
        "whatsapp": [],
        "slack": [],
        "skype": [],
        "email": [],
        "unknown": [],
    }

    if not uploaded_files:
        return parsed_by_platform

    for f in uploaded_files:
        file_type = detect_file_type(f.name)

        parsed = parse_file(f)

        if file_type == "whatsapp":
            messages = parsed.get("messages", [])
            parsed_by_platform["whatsapp"].extend(messages)

        elif file_type == "slack":
            messages = parsed.get("messages", [])
            parsed_by_platform["slack"].extend(messages)

        elif file_type == "skype":
            messages = parsed.get("messages", [])
            parsed_by_platform["skype"].extend(messages)

        elif file_type in ["eml", "mbox"]:
            messages = parsed.get("messages", [])
            parsed_by_platform["email"].extend(messages)

        else:
            # não reconhecido
            parsed_by_platform["unknown"].append(
                {
                    "filename": f.name,
                    "error": parsed.get("error", "Unknown format"),
                    "trace": parsed.get("trace", ""),
                }
            )

    return parsed_by_platform
