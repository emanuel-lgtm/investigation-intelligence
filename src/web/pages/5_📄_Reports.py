import streamlit as st

st.set_page_config(page_title="Reports", page_icon="📄", layout="wide")

if 'current_case' not in st.session_state or not st.session_state.current_case:
    st.error("⚠️ Please select a case first!")
    if st.button("Go to Cases"):
        st.switch_page("pages/1_📂_Cases.py")
    st.stop()

st.title("📄 Generate Reports")
st.info(f"Reporting on: **{st.session_state.current_case}**")

# Report options
st.subheader("📋 Report Configuration")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Select Formats:**")
    pdf = st.checkbox("📄 PDF Report (12 sections)", value=True)
    json_format = st.checkbox("📊 JSON Data (structured)", value=True)
    graph = st.checkbox("🗺️ Graph (mind map HTML)", value=True)

with col2:
    st.markdown("**Report Sections:**")
    exec_summary = st.checkbox("Executive Summary", value=True)
    entities = st.checkbox("Entities Found", value=True)
    timeline = st.checkbox("Timeline", value=True)
    relationships = st.checkbox("Relationships", value=True)
    questions = st.checkbox("Unasked Questions", value=True)
    recommendations = st.checkbox("Recommendations", value=True)

st.markdown("---")

# Generate button
if st.button("🚀 Generate Reports", type="primary", use_container_width=True):
    with st.spinner("Generating reports..."):
        import time
        progress = st.progress(0)
        
        # Simulate generation
        steps = ["Collecting data", "Analyzing entities", "Building relationships", 
                "Creating visualizations", "Generating PDF", "Finalizing"]
        
        for i, step in enumerate(steps):
            st.info(f"⏳ {step}...")
            time.sleep(0.5)
            progress.progress((i+1)/len(steps))
        
        st.success("✅ Reports generated successfully!")
        st.balloons()
    
    # Download section
    st.markdown("---")
    st.subheader("📥 Download Reports")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if pdf:
            st.download_button(
                "📄 Download PDF",
                data="Mock PDF content",
                file_name=f"{st.session_state.current_case}_report.pdf",
                mime="application/pdf",
                use_container_width=True
            )
    
    with col2:
        if json_format:
            st.download_button(
                "📊 Download JSON",
                data='{"case": "data"}',
                file_name=f"{st.session_state.current_case}_data.json",
                mime="application/json",
                use_container_width=True
            )
    
    with col3:
        if graph:
            st.download_button(
                "🗺️ Download Graph",
                data="<html>Mind map</html>",
                file_name=f"{st.session_state.current_case}_graph.html",
                mime="text/html",
                use_container_width=True
            )

# Report preview
st.markdown("---")
st.subheader("👁️ Report Preview")

with st.expander("📄 PDF Report Structure (12 sections)"):
    st.markdown("""
    1. **Executive Summary** - Overview and key findings
    2. **Case Information** - Basic case details
    3. **Document Inventory** - List of processed files
    4. **Entities Identified** - People, organizations, locations
    5. **Timeline of Events** - Chronological sequence
    6. **Relationship Map** - Connections between entities
    7. **Financial Transactions** - Money flows
    8. **Key Findings** - Important discoveries
    9. **Unasked Questions** - AI-generated inquiries
    10. **Risk Assessment** - Potential issues
    11. **Recommendations** - Suggested actions
    12. **Appendices** - Supporting data
    """)

# Statistics
st.markdown("---")
st.subheader("📊 Report Statistics")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Pages", "42")
col2.metric("Entities", "89")
col3.metric("Relationships", "127")
col4.metric("Questions", "15")
