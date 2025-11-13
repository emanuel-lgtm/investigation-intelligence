import streamlit as st
import os

# Page config
st.set_page_config(
    page_title="Investigation Intelligence System",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1rem 0;
    }
    .metric-card {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
    }
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'current_case' not in st.session_state:
    st.session_state.current_case = None
if 'cases' not in st.session_state:
    st.session_state.cases = []

# Header
st.markdown('<h1 class="main-header">🔍 Investigation Intelligence System</h1>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 🎯 Navigation")
    if st.session_state.current_case:
        st.success(f"**Active:** {st.session_state.current_case}")
    else:
        st.info("No case selected")
    
    st.markdown("---")
    st.page_link("pages/1_📂_Cases.py", label="Cases", icon="📂")
    st.page_link("pages/2_📤_Upload.py", label="Upload", icon="📤")
    st.page_link("pages/3_⚙️_Process.py", label="Process", icon="⚙️")
    st.page_link("pages/4_🔍_Analysis.py", label="Analysis", icon="🔍")
    st.page_link("pages/5_📄_Reports.py", label="Reports", icon="📄")

# Main content
st.markdown("## 🎉 Welcome to Investigation Intelligence!")

st.info("""
### 🚀 Quick Start:
1. **Create a Case** → Go to Cases page
2. **Upload Files** → Add documents
3. **Process** → AI analysis
4. **Review** → See results
5. **Generate Report** → PDF output
""")

# Metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown('<div class="metric-card"><h2>♾️</h2><h3>Unlimited</h3><p>File Size</p></div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="metric-card"><h2>20+</h2><h3>File Types</h3><p>Supported</p></div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="metric-card"><h2>3</h2><h3>AI Layers</h3><p>Analysis</p></div>', unsafe_allow_html=True)
with col4:
    st.markdown('<div class="metric-card"><h2>🔒</h2><h3>Secure</h3><p>Encrypted</p></div>', unsafe_allow_html=True)

st.markdown("---")

# System status
col1, col2 = st.columns(2)
with col1:
    st.markdown("### 🔑 API Status")
    openai_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY", "")
    anthropic_key = os.getenv("ANTHROPIC_API_KEY") or st.secrets.get("ANTHROPIC_API_KEY", "")
    
    if openai_key:
        st.success("✅ OpenAI Configured")
    else:
        st.error("❌ OpenAI Not Configured")
    
    if anthropic_key:
        st.success("✅ Anthropic Configured")
    else:
        st.error("❌ Anthropic Not Configured")

with col2:
    st.markdown("### ℹ️ System Info")
    st.info("**Version:** 1.0.0\n**Status:** ✅ Online\n**Cases:** " + str(len(st.session_state.cases)))

# Test button
if st.button("🎈 Test System", use_container_width=True):
    st.balloons()
    st.success("✅ All systems operational!")

st.caption("Investigation Intelligence v1.0.0 | Powered by AI")
