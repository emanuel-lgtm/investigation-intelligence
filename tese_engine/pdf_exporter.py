"""
TESE V9 - PDF Exporter

Responsável por gerar um arquivo PDF simples com o conteúdo
do relatório TESE e alguns metadados básicos.

Para PDFs mais sofisticados, podemos evoluir depois. Aqui o foco é:
    - Funcionar bem com grandes volumes
    - Não quebrar o app se a biblioteca de PDF não estiver instalada

Estratégia:
    - Tenta usar reportlab, se disponível.
    - Se não estiver instalado, gera um "pseudo-PDF" simples com
      conteúdo em texto (ainda com extensão .pdf) como fallback.

Recomendado:
    pip install reportlab
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict


def _ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def _export_with_reportlab(
    analysis_data: Dict[str, Any],
    report_text: str,
    output_path: Path,
) -> Path:
    """
    Gera PDF usando reportlab.
    """
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas

    _ensure_parent(output_path)

    c = canvas.Canvas(str(output_path), pagesize=A4)
    width, height = A4

    # Cabeçalho básico
    c.setFont("Helvetica-Bold", 14)
    c.drawString(72, height - 72, "TESE Forensic Report")

    # Metadados simples (total de mensagens, etc.)
    messages = analysis_data.get("messages", []) or []
    total_messages = len(messages)

    c.setFont("Helvetica", 10)
    c.drawString(72, height - 92, f"Total messages analysed: {total_messages}")

    # Corpo: texto do relatório (quebrando em linhas)
    text_obj = c.beginText()
    text_obj.setFont("Helvetica", 9)
    text_obj.setTextOrigin(72, height - 120)

    # Quebra o report_text em linhas
    for line in report_text.splitlines():
        text_obj.textLine(line)
        # Se chegar muito perto do fim da página, cria nova
        if text_obj.getY() < 72:
            c.drawText(text_obj)
            c.showPage()
            text_obj = c.beginText()
            text_obj.setFont("Helvetica", 9)
            text_obj.setTextOrigin(72, height - 72)

    c.drawText(text_obj)
    c.showPage()
    c.save()

    return output_path


def _export_plaintext_fallback(
    analysis_data: Dict[str, Any],
    report_text: str,
    output_path: Path,
) -> Path:
    """
    Fallback extremamente simples caso reportlab não esteja disponível.

    Cria um arquivo .pdf que na prática contém texto puro.
    Leitores de PDF podem reclamar, mas pelo menos o app não quebra.

    Idealmente o ambiente terá reportlab instalado.
    """
    _ensure_parent(output_path)
    header = "TESE Forensic Report (Plaintext Fallback)\n\n"
    messages = analysis_data.get("messages", []) or []
    total_messages = len(messages)
    meta = f"Total messages analysed: {total_messages}\n\n"

    content = header + meta + report_text

    # Escreve como texto bruto
    output_path.write_text(content, encoding="utf-8")
    return output_path


def export_to_pdf(
    analysis_data: Dict[str, Any],
    report_text: str,
    output_path: Path,
) -> Path:
    """
    Exporta o relatório TESE para PDF.

    Parâmetros:
        analysis_data: dict retornado por run_full_analysis
        report_text: texto gerado por report_generator.generate_report
        output_path: Path onde o PDF será salvo

    Retorna:
        Path final do PDF.

    OBS: se reportlab não estiver instalado, usa fallback em texto.
    """
    try:
        # Tenta usar reportlab
        import reportlab  # noqa: F401

        return _export_with_reportlab(analysis_data, report_text, output_path)
    except Exception:
        # Qualquer problema → fallback em texto (não quebra o app)
        return _export_plaintext_fallback(analysis_data, report_text, output_path)
