# ui_studio_panel.py
# UI do painel Estúdio (Studio) – TESE V9 BACKEND CONNECTED

import streamlit as st

from analysis_runner import analyze_uploaded_files
from output_builder import (
    build_report,
    build_mindmap,
    build_video_script,
    build_flashcards,
    build_quiz,
    build_audio_overview,
    export_case_json_outputs,
    export_tese_bundle,
    build_all_outputs_for_case,
)

from case_manager import (
    load_cases,
    save_cases,
    attach_exports_to_case,
)


def render_studio_panel(case=None):
    """
    Desenha o painel Estúdio na direita.
    Agora totalmente conectado ao backend TESE V9.
    """
    st.markdown(
        """
        <div class="ws-panel">
          <div class="ws-panel-header">Studio</div>
          <div class="ws-panel-title">Estúdio</div>
          <div class="ws-panel-subtitle">
            Ferramentas avançadas conectadas ao TESE Engine:
            relatórios, vídeos, mapas mentais e materiais de estudo.
          </div>
          <div class="ws-panel-body">
        """,
        unsafe_allow_html=True,
    )

    # Obter arquivos vinculados ao caso
    uploaded_files = case.get("files", [])
    selected_files = [f for f in uploaded_files if f.get("selected", True)]

    st.markdown('<div class="studio-grid">', unsafe_allow_html=True)
    st.caption("***Outputs gerados abaixo aparecerão automaticamente.***")

    # ------------------------------------------------------------------
    # 1) REPORT
    # ------------------------------------------------------------------
    if st.button("Reports", key="studio_reports", use_container_width=True):
        st.info("Gerando relatório TESE…")
        analysis_result = analyze_uploaded_files(selected_files)
        report_text = build_report(analysis_result["analysis"])
        st.session_state["studio_output"] = ("Report", report_text)

    st.caption("Relatório detalhado TESE")

    # ------------------------------------------------------------------
    # 2) MINDMAP
    # ------------------------------------------------------------------
    if st.button("Mind map", key="studio_mindmap", use_container_width=True):
        st.info("Gerando mindmap…")
        analysis_result = analyze_uploaded_files(selected_files)
        mindmap = build_mindmap(analysis_result["analysis"])
        st.session_state["studio_output"] = ("Mindmap", mindmap)

    st.caption("Mapa de entidades e relações")

    # ------------------------------------------------------------------
    # 3) VIDEO OVERVIEW
    # ------------------------------------------------------------------
    if st.button("Video overview", key="studio_video", use_container_width=True):
        st.info("Gerando roteiro para vídeo…")
        analysis_result = analyze_uploaded_files(selected_files)
        video_script = build_video_script(analysis_result["analysis"])
        st.session_state["studio_output"] = ("Video", video_script)

    st.caption("Roteiro para vídeo explicativo")

    # ------------------------------------------------------------------
    # 4) AUDIO OVERVIEW
    # ------------------------------------------------------------------
    if st.button("Audio overview", key="studio_audio", use_container_width=True):
        st.info("Gerando áudio…")
        analysis_result = analyze_uploaded_files(selected_files)
        audio_outline = build_audio_overview(analysis_result["analysis"])
        st.session_state["studio_output"] = ("Audio", audio_outline)

    st.caption("Resumo narrado do caso")

    # ------------------------------------------------------------------
    # 5) FLASHCARDS
    # ------------------------------------------------------------------
    if st.button("Flashcards", key="studio_flashcards", use_container_width=True):
        st.info("Gerando flashcards…")
        analysis_result = analyze_uploaded_files(selected_files)
        cards = build_flashcards(analysis_result["analysis"])
        st.session_state["studio_output"] = ("Flashcards", cards)

    st.caption("Pontos-chave para estudo")

    # ------------------------------------------------------------------
    # 6) QUIZ
    # ------------------------------------------------------------------
    if st.button("Quiz", key="studio_quiz", use_container_width=True):
        st.info("Gerando quiz…")
        analysis_result = analyze_uploaded_files(selected_files)
        quiz = build_quiz(analysis_result["analysis"])
        st.session_state["studio_output"] = ("Quiz", quiz)

    st.caption("Testar entendimento do caso")

    st.markdown('</div>', unsafe_allow_html=True)

    # ----------------------------------------------------------------------
    # OUTPUT BOX (qualquer botão do studio)
    # ----------------------------------------------------------------------
    if "studio_output" in st.session_state:
        output_type, output_content = st.session_state["studio_output"]

        st.markdown("---")
        st.subheader(f"Output gerado: {output_type}")

        if output_type in ["Report", "Video", "Audio"]:
            st.text_area("Resultado:", output_content, height=300)

        elif output_type in ["Mindmap", "Flashcards", "Quiz"]:
            st.json(output_content)

    # ----------------------------------------------------------------------
    # 🟦 NOVA SEÇÃO: EXPORTS DO CASE (JSON + .TESE)
    # ----------------------------------------------------------------------
    st.markdown("---")
    st.subheader("📦 Exportar caso")

    if st.button("Export JSON + Bundle (.TESE)", key="studio_export_case", use_container_width=True):
        st.info("Exportando JSON + Bundle…")

        # Reprocessar análise (com cache)
        analysis_result = analyze_uploaded_files(selected_files)
        analysis_data = analysis_result["analysis"]

        # 1) Gerar todos outputs em memória + export JSON + bundle
        export_result = build_all_outputs_for_case(
            case=case,
            analysis_data=analysis_data,
            include_messages=True,
        )

        # Atualizar no case_manager
        cases = load_cases()
        # localizar o case atual
        idx = next((i for i,c in enumerate(cases) if c["id"] == case["id"]), None)
        if idx is not None:
            cases = attach_exports_to_case(
                cases,
                idx,
                json_summary_path=export_result["json_exports"]["summary_path"],
                json_messages_path=export_result["json_exports"]["messages_path"],
                bundle_path=export_result["bundle_export"]["bundle_path"],
            )
            save_cases(cases)

        # Exibir resultados para o usuário
        st.success("Arquivos exportados!")
        st.json(export_result)

    # ----------------------------------------------------------------------
    # Lista de execuções recentes (dummy)
    # ----------------------------------------------------------------------
    st.markdown("### Recent studio runs")
    dummy_runs = [
        "Implosão da FIGO/ACSoftware: análise de conflitos",
        "Estrutura e crise do grupo econômico",
        "Digital sabotage & crédito bloqueado",
        "Resumo em áudio das comunicações críticas",
    ]
    for r in dummy_runs:
        st.markdown(
            f"""
            <div class="studio-run-item">
              <div class="studio-run-title">{r}</div>
              <div class="studio-run-meta">300 sources · 5d ago</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("</div></div>", unsafe_allow_html=True)

