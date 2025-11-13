import streamlit as st
import pandas as pd

st.set_page_config(page_title="Analysis", page_icon="🔍", layout="wide")

if 'current_case' not in st.session_state or not st.session_state.current_case:
    st.error("⚠️ Please select a case first!")
    if st.button("Go to Cases"):
        st.switch_page("pages/1_📂_Cases.py")
    st.stop()

st.title("🔍 Analysis Results")
st.info(f"Analyzing: **{st.session_state.current_case}**")

# Mock data
entities_data = {
    'Name': ['John Doe', 'Acme Corp', '$50,000', '2024-01-15', 'New York'],
    'Type': ['PERSON', 'ORG', 'MONEY', 'DATE', 'LOCATION'],
    'Mentions': [45, 32, 12, 8, 23],
    'Confidence': ['98%', '95%', '99%', '97%', '94%']
}

# Entities
st.subheader("📊 Key Entities")
df = pd.DataFrame(entities_data)
st.dataframe(df, use_container_width=True, hide_index=True)

st.markdown("---")

# Timeline
st.subheader("📅 Timeline")
st.markdown("""
- **2024-01-15** → Contract signed
- **2024-02-01** → Payment received
- **2024-03-10** → Meeting scheduled
- **2024-04-05** → Follow-up action
""")

st.markdown("---")

# Relationships
st.subheader("🔗 Relationships")
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **Direct Connections:**
    - John Doe → works_for → Acme Corp
    - Acme Corp → paid → $50,000
    - John Doe → met_with → Jane Smith
    """)

with col2:
    st.markdown("""
    **Indirect Links:**
    - John Doe → New York → Office
    - Acme Corp → 2024-01-15 → Contract
    """)

st.markdown("---")

# Self-prompting questions
st.subheader("💡 Unasked Questions")
st.warning("""
**Priority: High**
1. Who authorized the $50,000 transfer?
2. Why is there a gap between Jan 15 and Feb 1?
3. What's the connection between John and Jane?
4. Are there any undisclosed relationships?
""")

st.markdown("---")

# Mind Map placeholder
st.subheader("🗺️ Relationship Graph")
st.info("Interactive mind map will be displayed here. Coming soon!")

# Export
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    if st.button("📄 Generate Report", use_container_width=True):
        st.switch_page("pages/5_📄_Reports.py")
with col2:
    if st.button("📥 Export Data (JSON)", use_container_width=True):
        st.download_button(
            "Download JSON",
            data='{"entities": [], "relationships": []}',
            file_name="analysis.json",
            mime="application/json"
        )
