"""
TESE V8 Engine package root.

Os módulos internos (parsers, análise, outputs) são importados diretamente
pelo engine_bridge.py, por isso este __init__ é mantido mínimo e seguro,
sem importar classes/funções específicas (como WhatsAppParser).

Isso evita erros de import quando mudamos a implementação interna dos parsers.
"""

__all__ = [
    "whatsapp_parser",
    "slack_parser",
    "skype_parser",
    "email_eml_parser",
    "email_mbox_parser",
    "message_scorer",
    "incident_flagger",
    "pattern_aggregator",
    "platform_correlator",
    "timeline_builder",
    "risk_orchestrator",
    "report_generator",
    "mindmap_generator",
    "video_overview",
    "suggested_questions",
    "ui_integration",
]
