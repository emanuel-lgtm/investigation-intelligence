import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Cases", page_icon="📂", layout="wide")

if 'cases' not in st.session_state:
    st.session_state.cases = []
if 'current_case' not in st.session_state:
    st.session_state.current_case = None

st.title("📂 Case Management")
st.markdown("---")

# Create new case
st.subheader("➕ Create New Case")

with st.form("create_case"):
    col1, col2 = st.columns(2)
    with col1:
        case_id = st.text_input("Case ID*", placeholder="CASE_001")
        case_name = st.text_input("Case Name*", placeholder="Financial Investigation")
    with col2:
        case_type = st.selectbox("Type", ["Financial", "Corporate", "Legal", "Compliance", "Other"])
        priority = st.selectbox("Priority", ["Low", "Medium", "High", "Critical"])
    
    description = st.text_area("Description", height=100)
    submitted = st.form_submit_button("🚀 Create", use_container_width=True)
    
    if submitted:
        if not case_id or not case_name:
            st.error("❌ ID and Name required!")
        elif any(c['id'] == case_id for c in st.session_state.cases):
            st.error(f"❌ Case '{case_id}' exists!")
        else:
            st.session_state.cases.append({
                'id': case_id,
                'name': case_name,
                'type': case_type,
                'priority': priority,
                'description': description,
                'created': datetime.now().strftime("%Y-%m-%d %H:%M"),
                'status': 'Active',
                'files': 0
            })
            st.session_state.current_case = case_id
            st.success(f"✅ Created '{case_id}'!")
            st.balloons()
            st.rerun()

st.markdown("---")

# List cases
st.subheader("📋 Existing Cases")

if not st.session_state.cases:
    st.info("👋 No cases yet. Create one above!")
else:
    for case in st.session_state.cases:
        with st.expander(f"📁 {case['id']} - {case['name']}", expanded=(case['id']==st.session_state.current_case)):
            col1, col2, col3 = st.columns([2,1,1])
            with col1:
                st.write(f"**Type:** {case['type']}")
                st.write(f"**Description:** {case.get('description', 'None')}")
            with col2:
                st.write(f"**Priority:** {case['priority']}")
                st.write(f"**Status:** {case['status']}")
            with col3:
                if st.button("✅ Select", key=f"sel_{case['id']}", use_container_width=True):
                    st.session_state.current_case = case['id']
                    st.rerun()
                if st.button("🗑️ Delete", key=f"del_{case['id']}", use_container_width=True):
                    st.session_state.cases = [c for c in st.session_state.cases if c['id'] != case['id']]
                    if st.session_state.current_case == case['id']:
                        st.session_state.current_case = None
                    st.rerun()

# Summary
st.markdown("---")
col1, col2, col3 = st.columns(3)
col1.metric("Total Cases", len(st.session_state.cases))
col2.metric("Active", len([c for c in st.session_state.cases if c['status']=='Active']))
col3.metric("Current", st.session_state.current_case or "None")
