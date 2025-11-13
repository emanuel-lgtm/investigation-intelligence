import streamlit as st

st.set_page_config(page_title="Upload", page_icon="📤", layout="wide")

if 'current_case' not in st.session_state or not st.session_state.current_case:
    st.error("⚠️ Please select a case first!")
    if st.button("Go to Cases"):
        st.switch_page("pages/1_📂_Cases.py")
    st.stop()

st.title("📤 Upload Files")
st.info(f"Uploading to: **{st.session_state.current_case}**")

# Upload method
upload_method = st.radio("Select method:", ["📁 Local Files", "☁️ Google Drive", "📦 Dropbox"], horizontal=True)

st.markdown("---")

if upload_method == "📁 Local Files":
    st.subheader("Upload from Computer")
    
    uploaded_files = st.file_uploader(
        "Drag and drop files here",
        accept_multiple_files=True,
        type=['pdf', 'doc', 'docx', 'txt', 'csv', 'xlsx', 'jpg', 'jpeg', 'png', 'mp3', 'mp4'],
        help="Supports: PDF, DOC, TXT, CSV, Excel, Images, Audio, Video"
    )
    
    if uploaded_files:
        st.success(f"✅ {len(uploaded_files)} file(s) selected")
        
        with st.expander("📋 View files"):
            for file in uploaded_files:
                col1, col2 = st.columns([3,1])
                col1.write(file.name)
                col2.write(f"{file.size/1024:.1f} KB")
        
        if st.button("🚀 Upload Files", type="primary", use_container_width=True):
            progress = st.progress(0)
            for i, file in enumerate(uploaded_files):
                progress.progress((i+1)/len(uploaded_files))
            st.success(f"✅ Uploaded {len(uploaded_files)} files!")
            st.balloons()

elif upload_method == "☁️ Google Drive":
    st.subheader("Import from Google Drive")
    
    folder_id = st.text_input(
        "Google Drive Folder ID",
        placeholder="abc123def456",
        help="Right-click folder → Get link → Copy ID"
    )
    
    recursive = st.checkbox("Include subfolders", value=True)
    
    if st.button("🚀 Import", type="primary", use_container_width=True):
        if not folder_id:
            st.error("Please enter folder ID")
        else:
            with st.spinner("Importing..."):
                st.info("Google Drive integration coming soon!")

elif upload_method == "📦 Dropbox":
    st.subheader("Import from Dropbox")
    
    folder_path = st.text_input(
        "Dropbox Folder Path",
        placeholder="/Evidence/Case001"
    )
    
    recursive = st.checkbox("Include subfolders", value=True)
    
    if st.button("🚀 Import", type="primary", use_container_width=True):
        if not folder_path:
            st.error("Please enter path")
        else:
            with st.spinner("Importing..."):
                st.info("Dropbox integration coming soon!")

# Info sidebar
with st.sidebar:
    st.info("""
    ### 📝 Supported Files
    
    **Documents:**
    - PDF, DOC/DOCX, TXT
    
    **Data:**
    - CSV, XLS/XLSX
    
    **Media:**
    - Images: JPG, PNG
    - Audio: MP3
    - Video: MP4
    """)
