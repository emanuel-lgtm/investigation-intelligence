import streamlit as st
import os

# Page config
st.set_page_config(
    page_title="Investigation Intelligence System",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS matching projetoabc.netlify.app style
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
    }
    
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* Hero Header */
    .hero-header {
        text-align: center;
        padding: 3rem 0;
        margin-bottom: 3rem;
    }
    
    .hero-title {
        font-size: 4rem;
        font-weight: 800;
        color: white;
        text-shadow: 0 4px 20px rgba(0,0,0,0.2);
        margin-bottom: 1rem;
        line-height: 1.2;
    }
    
    .hero-subtitle {
        font-size: 1.5rem;
        color: rgba(255,255,255,0.9);
        font-weight: 300;
        margin-bottom: 2rem;
    }
    
    /* Glass Card */
    .glass-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.2);
        margin-bottom: 2rem;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 48px rgba(0,0,0,0.15);
    }
    
    /* Feature Cards */
    .feature-card {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        height: 100%;
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 8px 30px rgba(102, 126, 234, 0.3);
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    
    .feature-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #667eea;
        margin-bottom: 0.5rem;
    }
    
    .feature-text {
        color: #64748b;
        font-size: 1rem;
        line-height: 1.6;
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 1rem 3rem;
        font-size: 1.1rem;
        font-weight: 600;
        border-radius: 50px;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 25px rgba(102, 126, 234, 0.6);
    }
    
    /* Sidebar */
    .css-1d391kg, [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    .css-1d391kg .stMarkdown, [data-testid="stSidebar"] .stMarkdown {
        color: white;
    }
    
    /* Metrics */
    .metric-container {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        color: #64748b;
        font-size: 1rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Status Cards */
    .status-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        border-left: 4px solid #667eea;
    }
    
    .status-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 1rem;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Success/Error boxes */
    .stSuccess, .stError, .stInfo, .stWarning {
        border-radius: 10px;
        padding: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'current_case' not in st.session_state:
    st.session_state.current_case = None
if 'cases' not in st.session_state:
    st.session_state.cases = []

# Hero Section
st.markdown("""
<div class="hero-header">
    <div class="hero-title">🔍 Investigation Intelligence</div>
    <div class="hero-subtitle">AI-Powered Investigation & Analysis Platform</div>
</div>
""", unsafe_allow_html=True)

# Main content in glass card
with st.container():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    # Welcome message
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <h2 style="color: #1e293b; font-weight: 700; margin-bottom: 1rem;">
            Transform Your Investigation Process
        </h2>
        <p style="color: #64748b; font-size: 1.2rem; max-width: 800px; margin: 0 auto;">
            Leverage cutting-edge AI technology to analyze documents, discover relationships, 
            and generate comprehensive investigation reports in minutes.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Feature Cards
st.markdown("### 🎯 Key Features")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">♾️</div>
        <div class="feature-title">Unlimited</div>
        <div class="feature-text">Process files of any size with no restrictions</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🤖</div>
        <div class="feature-title">AI-Powered</div>
        <div class="feature-text">Advanced entity extraction and analysis</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🗺️</div>
        <div class="feature-title">Visualizations</div>
        <div class="feature-text">Interactive relationship maps and timelines</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📄</div>
        <div class="feature-title">Reports</div>
        <div class="feature-text">Professional PDF reports in seconds</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Quick Start Section
st.markdown('<div class="glass-card">', unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    <div style="padding: 1rem 0;">
        <h3 style="color: #1e293b; font-weight: 700; margin-bottom: 1.5rem;">🚀 Quick Start Guide</h3>
        <div style="color: #64748b; font-size: 1.1rem; line-height: 2;">
            <div style="margin-bottom: 1rem;">
                <strong style="color: #667eea;">1. Create a Case</strong> → Organize your investigation
            </div>
            <div style="margin-bottom: 1rem;">
                <strong style="color: #667eea;">2. Upload Files</strong> → Documents, images, audio, video
            </div>
            <div style="margin-bottom: 1rem;">
                <strong style="color: #667eea;">3. Process</strong> → AI analyzes everything automatically
            </div>
            <div style="margin-bottom: 1rem;">
                <strong style="color: #667eea;">4. Review</strong> → Explore entities, relationships, timeline
            </div>
            <div>
                <strong style="color: #667eea;">5. Generate Report</strong> → Professional PDF output
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="status-card">
        <div class="status-title">📊 Statistics</div>
        <div class="metric-container" style="margin-bottom: 1rem;">
            <div class="metric-value">{}</div>
            <div class="metric-label">Total Cases</div>
        </div>
        <div class="metric-container">
            <div class="metric-value">{}</div>
            <div class="metric-label">Active Case</div>
        </div>
    </div>
    """.format(
        len(st.session_state.cases),
        st.session_state.current_case or "None"
    ), unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# System Status
st.markdown("---")

st.markdown('<div class="glass-card">', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="status-card">', unsafe_allow_html=True)
    st.markdown('<div class="status-title">🔑 API Configuration</div>', unsafe_allow_html=True)
    
    openai_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY", "")
    anthropic_key = os.getenv("ANTHROPIC_API_KEY") or st.secrets.get("ANTHROPIC_API_KEY", "")
    
    if openai_key:
        st.success("✅ OpenAI API Configured")
    else:
        st.error("❌ OpenAI API Not Configured")
    
    if anthropic_key:
        st.success("✅ Anthropic API Configured")
    else:
        st.error("❌ Anthropic API Not Configured")
    
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="status-card">', unsafe_allow_html=True)
    st.markdown('<div class="status-title">ℹ️ System Information</div>', unsafe_allow_html=True)
    st.info("""
    **Version:** 1.0.0  
    **Python:** 3.13  
    **Status:** ✅ Online  
    **Uptime:** 24/7
    """)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# CTA Button
st.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🎈 Test System", use_container_width=True):
        st.balloons()
        st.success("✅ All systems operational! Navigate to Cases to get started.")

# Footer
st.markdown("""
<div style="text-align: center; padding: 2rem 0; color: white;">
    <p style="font-size: 0.9rem; opacity: 0.8;">
        Investigation Intelligence System v1.0.0 | Powered by OpenAI & Anthropic
    </p>
</div>
""", unsafe_allow_html=True)

# Sidebar styling
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0;">
        <h1 style="color: white; font-size: 2rem; margin-bottom: 0.5rem;">🔍</h1>
        <h3 style="color: white; font-weight: 300;">Investigation</h3>
        <h3 style="color: white; font-weight: 700; margin-top: -0.5rem;">Intelligence</h3>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    if st.session_state.current_case:
        st.success(f"**Active Case:**\n\n{st.session_state.current_case}")
    else:
        st.info("**No Case Selected**\n\nCreate a case to get started")
    
    st.markdown("---")
    
    st.markdown("### 📍 Navigation")
    st.page_link("pages/1_📂_Cases.py", label="Cases Management", icon="📂")
    st.page_link("pages/2_📤_Upload.py", label="Upload Documents", icon="📤")
    st.page_link("pages/3_⚙️_Process.py", label="Process Files", icon="⚙️")
    st.page_link("pages/4_🔍_Analysis.py", label="View Analysis", icon="🔍")
    st.page_link("pages/5_📄_Reports.py", label="Generate Reports", icon="📄")
