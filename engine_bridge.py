import traceback

from tese_engine.whatsapp_parser import parse_whatsapp
from tese_engine.slack_parser import parse_slack

from tese_engine.message_scorer import score_messages
from tese_engine.incident_flagger import flag_incidents
from tese_engine.pattern_aggregator import aggregate_patterns
from tese_engine.platform_correlator import correlate_platforms
from tese_engine.timeline_builder import build_timeline
from tese_engine.risk_orchestrator import orchestrate_risk

from tese_engine.report_generator import generate_report
from tese_engine.mindmap_generator import generate_mindmap
from tese_engine.video_overview import generate_video_script
from tese_engine.suggested_questions import generate_flashcards
from tese_engine.ui_integration import generate_quiz


def detect_file_type(filename: str) -> str:
    """Simple file type detection based on the file name."""
    name = filename.lower()

    # WhatsApp (.txt)
    if name.endswith(".txt") and "whatsapp" in name:
        return "whatsapp"
    if name.endswith(".txt") and "chat" in name:
        return "whatsapp"

    # Slack (.json / .csv)
    if name.endswith(".json"):
        return "slack"
    if name.endswith(".csv"):
        return "slack"

    # Skype (placeholder)
    if ("skype" in name or name.endswith(".db")):
        return "skype"

    # Email (placeholders)
    if name.endswith(".eml"):
        return "eml"
    if name.endswith(".mbox"):
        return "mbox"

    return "unknown"


def parse_file(file_obj):
    """
    Entry point for parsing any uploaded file.

    Returns a dict with at least:
        {
            "platform": str,
            "messages": list,
            "filename": str,
            "error": optional str
        }
    """
    try:
        file_type = detect_file_type(file_obj.name)

        # WhatsApp
        if file_type == "whatsapp":
            return parse_whatsapp(file_obj)

        # Slack
        if file_type == "slack":
            messages = parse_slack(file_obj)
            return {
                "platform": "slack",
                "messages": messages,
                "filename": file_obj.name,
            }

        # Skype (placeholder)
        if file_type == "skype":
            return {
                "platform": "skype",
                "messages": [],
                "error": "Skype parser not implemented yet.",
                "filename": file_obj.name,
            }

        # Email (placeholder)
        if file_type in ["eml", "mbox"]:
            return {
                "platform": "email",
                "messages": [],
                "error": "Email parser (EML/MBOX) not implemented yet.",
                "filename": file_obj.name,
            }

        # Unknown
        return {
            "platform": "unknown",
            "messages": [],
            "error": f"Unrecognized file type: {file_obj.name}",
            "filename": file_obj.name,
        }

    except Exception as e:
        return {
            "platform": "error",
            "messages": [],
            "error": str(e),
            "trace": traceback.format_exc(),
            "filename": getattr(file_obj, "name", None),
        }


# ----------------------------------------------------------------------
# ANÁLISE COMPLETA (TESE V8 PIPELINE)
# ----------------------------------------------------------------------
def run_full_analysis(parsed_data_per_platform: dict):
    """
    Flatten messages from all platforms and run the TESE V8 pipeline.
    """
    try:
        all_messages = []

        for _platform, data in parsed_data_per_platform.items():
            if isinstance(data, list):
                all_messages.extend(data)
            elif isinstance(data, dict) and "messages" in data:
                all_messages.extend(data["messages"])

        scored = score_messages(all_messages)
        flagged = flag_incidents(scored)
        patterns = aggregate_patterns(flagged)
        correlated = correlate_platforms(flagged)
        timeline = build_timeline(flagged)

        risk = orchestrate_risk(
            flagged_messages=flagged,
            pattern_data=patterns,
            correlation_data=correlated,
            timeline_data=timeline,
        )

        return {
            "messages": flagged,
            "patterns": patterns,
            "correlation": correlated,
            "timeline": timeline,
            "risk_summary": risk,
            "status": "ok",
        }

    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "trace": traceback.format_exc(),
        }


def create_report(analysis_data):
    return generate_report(analysis_data)


def create_mindmap(analysis_data):
    return generate_mindmap(analysis_data)


def create_video_overview(analysis_data):
    return generate_video_script(analysis_data)


def create_flashcards(analysis_data):
    return generate_flashcards(analysis_data)


def create_quiz(analysis_data):
    return generate_quiz(analysis_data)


def create_audio_overview(analysis_data):
    # Placeholder for future TTS integration
    return "AUDIO_OVERVIEW_PLACEHOLDER"
