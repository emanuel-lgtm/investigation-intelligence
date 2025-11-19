import streamlit as st


def inject_global_css() -> None:
    """
    Injeta CSS global inspirado no frontend Checkpoint B,
    sem alterar a lógica do backend.
    """
    st.markdown(
        """
        <style>
        /* RESET BÁSICO */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        html, body {
            height: 100%;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text',
                         'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            background: #050510;
            color: #f8fafc;
            line-height: 1.6;
        }

        /* Esconde o cabeçalho padrão do Streamlit e menu */
        header[data-testid="stHeader"] {
            background: transparent;
        }
        [data-testid="stToolbar"], #MainMenu, footer, .stDeployButton {
            visibility: hidden;
            height: 0;
        }

        /* Container principal */
        .block-container {
            padding-top: 0 !important;
            padding-left: 0 !important;
            padding-right: 0 !important;
            max-width: 1400px;
        }

        :root {
            --primary-purple: #8b5cf6;
            --primary-blue:   #3b82f6;
            --dark-bg:        #050510;
            --card-bg:        #111827;
            --card-hover:     #1f2937;
            --text-primary:   #f8fafc;
            --text-secondary: #9ca3af;
            --border-color:   #374151;
        }

        /* HEADER GLOBAL */
        .tese-header {
            background: linear-gradient(135deg, #020617 0%, #111827 60%, #020617 100%);
            border-bottom: 1px solid var(--border-color);
            position: sticky;
            top: 0;
            z-index: 1000;
            padding: 1.25rem 2rem;
        }

        .tese-header-inner {
            max-width: 1400px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .tese-logo {
            display: flex;
            align-items: center;
            gap: 1rem;
        }

        .tese-logo-icon {
            width: 40px;
            height: 40px;
            background: linear-gradient(135deg, var(--primary-purple), var(--primary-blue));
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            font-size: 1.2rem;
            color: white;
        }

        .tese-logo-title {
            display: flex;
            flex-direction: column;
            gap: 2px;
        }

        .tese-logo-title h1 {
            font-size: 1.5rem;
            margin: 0;
            background: linear-gradient(135deg, var(--primary-purple), var(--primary-blue));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .tese-logo-subtitle {
            font-size: 0.8rem;
            color: var(--text-secondary);
        }

        .tese-header-pill {
            padding: 0.35rem 0.9rem;
            border-radius: 999px;
            font-size: 0.8rem;
            font-weight: 500;
            background: rgba(16, 185, 129, 0.12);
            color: #a7f3d0;
            border: 1px solid rgba(16, 185, 129, 0.4);
        }

        .tese-page-container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 2.2rem 2rem 3rem 2rem;
        }

        .tese-main-title {
            font-size: 2.6rem;
            font-weight: 800;
            margin-bottom: 0.75rem;
        }

        .tese-main-subtitle {
            font-size: 0.95rem;
            color: var(--text-secondary);
            margin-bottom: 1.5rem;
        }

        .tese-callout {
            background: #3f3f07;
            color: #fef9c3;
            padding: 0.9rem 1.4rem;
            border-radius: 0.75rem;
            border: 1px solid rgba(250, 204, 21, 0.5);
            font-size: 0.9rem;
        }

        @media (max-width: 900px) {
            .tese-page-container {
                padding: 1.5rem 1.25rem 2rem 1.25rem;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_header() -> None:
    """
    Renderiza o cabeçalho global TESE V9.
    Não controla navegação, apenas visual.
    """
    st.markdown(
        """
        <div class="tese-header">
          <div class="tese-header-inner">
            <div class="tese-logo">
              <div class="tese-logo-icon">T9</div>
              <div class="tese-logo-title">
                <h1>TESE V9</h1>
                <span class="tese-logo-subtitle">Trauma Evidence Support Engine · Investigation Studio</span>
              </div>
            </div>
            <div class="tese-header-pill">
              Backend connected · Engine V9 active
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
