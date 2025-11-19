import streamlit as st

from case_manager import (
    load_cases,
    save_cases,
    create_case,
)
from ui_studio_panel import render_studio_panel
from ui_theme import inject_global_css, render_header


def _get_selected_case_index(cases):
    """
    Helper para recuperar/armazenar o índice do case selecionado
    na session_state, para manter seleção estável entre reruns.
    """
    if "selected_case_index" not in st.session_state:
        st.session_state["selected_case_index"] = 0

    if not cases:
        st.session_state["selected_case_index"] = 0
        return 0

    idx = st.session_state["selected_case_index"]
    if idx < 0 or idx >= len(cases):
        idx = 0
    return idx


def _render_cases_overview(cases, selected_index: int):
    """
    Renderiza um mini 'grid' de cases, apenas visual.
    NÃO altera a lógica de seleção, só mostra informações.
    """
    if not cases:
        return

    st.markdown("### Visão geral dos cases")

    # Callout explicando o painel
    st.markdown(
        """
        <div class="tese-callout">
          Esta visão mostra todos os cases salvos pelo <code>case_manager</code>.
          Selecionar um case na barra lateral atualiza o estúdio abaixo.
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Cabeçalho
    cols_head = st.columns([3, 1.5, 1.5, 1.8])
    cols_head[0].markdown("**Case**")
    cols_head[1].markdown("**Status**")
    cols_head[2].markdown("**Criado em**")
    cols_head[3].markdown("**Exports**")

    for i, case in enumerate(cases):
        is_selected = (i == selected_index)
        exports = case.get("exports", {}) or {}
        pdf_ok = bool(exports.get("pdf"))
        bundle_ok = bool(exports.get("bundle"))
        json_ok = bool(exports.get("json_summary")) or bool(exports.get("json_messages"))

        label = case["name"]
        if is_selected:
            label = f"👉 {label}"

        cols = st.columns([3, 1.5, 1.5, 1.8])

        with cols[0]:
            st.markdown(
                f"- **{label}**  \n"
                f"`{case['id']}`",
                unsafe_allow_html=False,
            )

        with cols[1]:
            st.markdown(case.get("status", "new"))

        with cols[2]:
            st.markdown(str(case.get("created", "")))

        with cols[3]:
            exports_bits = []
            if pdf_ok:
                exports_bits.append("📄 PDF")
            if json_ok:
                exports_bits.append("🧾 JSON")
            if bundle_ok:
                exports_bits.append("📦 Bundle")
            if not exports_bits:
                exports_bits.append("—")

            st.markdown(" · ".join(exports_bits))


def main():
    st.set_page_config(
        page_title="TESE V9 – Investigation Studio",
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # 🎨 Tema global (NÃO mexe em backend)
    inject_global_css()
    render_header()

    # Container principal para manter consistência visual
    with st.container():
        st.markdown(
            '<div class="tese-page-container">',
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="tese-main-title">TESE V9 – Investigation Studio</div>
            <div class="tese-main-subtitle">
              Selecione ou crie um case na barra lateral e use o estúdio para ingestão,
              análise e geração de relatórios.
            </div>
            """,
            unsafe_allow_html=True,
        )

        # ------------------------------------------------------------
        # 1) Carregar cases existentes
        # ------------------------------------------------------------
        cases = load_cases()

        # ------------------------------------------------------------
        # 2) Sidebar: seleção e criação de casos
        # ------------------------------------------------------------
        st.sidebar.header("Cases")

        if not cases:
            st.sidebar.info("Nenhum case cadastrado ainda. Crie o primeiro case abaixo.")

        # Form para criar novo case
        with st.sidebar.form(key="create_case_form"):
            new_case_name = st.text_input("Nome do novo case")
            new_case_sources_raw = st.text_input(
                "Fontes (opcional, separado por vírgulas)",
                help="Ex.: WhatsApp, Slack, E-mail",
            )
            create_clicked = st.form_submit_button("Criar case")

        if create_clicked and new_case_name.strip():
            sources = []
            if new_case_sources_raw.strip():
                sources = [s.strip() for s in new_case_sources_raw.split(",") if s.strip()]

            new_case = create_case(
                name=new_case_name.strip(),
                sources=sources,
                owner=None,
            )
            cases.append(new_case)
            save_cases(cases)
            # garante que o novo case fique selecionado
            st.session_state["selected_case_index"] = len(cases) - 1
            st.success(f"Case '{new_case_name.strip()}' criado com sucesso.")
            st.experimental_rerun()

        # Se não houver cases depois da criação, exibe mensagem e encerra
        if not cases:
            st.markdown(
                '<div class="tese-callout">Crie um case na barra lateral para começar a usar o estúdio.</div>',
                unsafe_allow_html=True,
            )
            st.markdown("</div>", unsafe_allow_html=True)
            return

        # Seleção de case existente
        current_idx = _get_selected_case_index(cases)

        case_labels = [
            f"{c['name']} ({c['id']})"
            for c in cases
        ]

        selected_index = st.sidebar.selectbox(
            "Selecionar case",
            options=list(range(len(cases))),
            format_func=lambda i: case_labels[i],
            index=current_idx,
        )
        st.session_state["selected_case_index"] = selected_index
        selected_case = cases[selected_index]

        # ------------------------------------------------------------
        # 3) Visão geral dos cases (lista bonita, só visual)
        # ------------------------------------------------------------
        _render_cases_overview(cases, selected_index)

        st.markdown("---")

        # ------------------------------------------------------------
        # 4) Painel Studio (toda a lógica pesada está em ui_studio_panel)
        # ------------------------------------------------------------
        st.subheader("Studio do case selecionado")
        render_studio_panel(case=selected_case)

        st.markdown("</div>", unsafe_allow_html=True)  # fecha .tese-page-container


if __name__ == "__main__":
    main()
