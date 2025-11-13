# 🌐 Web Interface - Investigation Intelligence System

## Overview

Two web interface options are provided:

1. **Streamlit** (Quick & Easy) - Perfect for internal use, rapid prototyping
2. **FastAPI + React** (Production) - Professional, scalable, full-featured

Both interfaces provide:
- ✅ Case management
- ✅ File upload (drag & drop)
- ✅ Real-time processing status
- ✅ Analysis results visualization
- ✅ Interactive mind maps
- ✅ Report download
- ✅ Multi-user support

---

## Option 1: Streamlit Interface (Recommended for Quick Start)

### Features
- 🚀 **5-minute setup**
- 📱 **Responsive design**
- 🎨 **Modern UI out of the box**
- 📊 **Built-in charts and visualizations**
- 🔄 **Real-time updates**
- 👥 **Multi-page application**

### Installation

```bash
# Add to requirements.txt
pip install streamlit
pip install streamlit-aggrid
pip install streamlit-extras
pip install plotly
```

### File Structure

```
src/
└── web/
    ├── __init__.py
    ├── app.py                    # Main Streamlit app
    ├── pages/
    │   ├── 1_📁_Cases.py        # Case management
    │   ├── 2_📤_Upload.py       # File upload
    │   ├── 3_⚙️_Process.py      # Processing
    │   ├── 4_🔍_Analysis.py     # Analysis results
    │   ├── 5_🗺️_MindMap.py     # Interactive mind map
    │   └── 6_📄_Reports.py      # Report generation
    ├── components/
    │   ├── __init__.py
    │   ├── case_card.py         # Case display component
    │   ├── file_uploader.py     # Custom file uploader
    │   ├── progress_tracker.py  # Processing progress
    │   └── mindmap_viewer.py    # Interactive graph viewer
    └── utils/
        ├── __init__.py
        ├── session_state.py     # Session management
        └── styling.py           # Custom CSS
```

### Quick Implementation

#### Main App (`src/web/app.py`)

```python
import streamlit as st
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.main import InvestigationSystem

# Page configuration
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
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'system' not in st.session_state:
    st.session_state.system = InvestigationSystem()

if 'current_case' not in st.session_state:
    st.session_state.current_case = None

# Header
st.markdown('<h1 class="main-header">🔍 Investigation Intelligence System</h1>', 
            unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://via.placeholder.com/300x100.png?text=Logo", use_column_width=True)
    
    st.markdown("---")
    
    # Current case info
    if st.session_state.current_case:
        st.success(f"**Active Case:** {st.session_state.current_case}")
    else:
        st.info("No active case selected")
    
    st.markdown("---")
    
    # Quick actions
    st.subheader("Quick Actions")
    
    if st.button("➕ New Case"):
        st.switch_page("pages/1_📁_Cases.py")
    
    if st.button("📤 Upload Files"):
        st.switch_page("pages/2_📤_Upload.py")
    
    if st.button("⚙️ Process Case"):
        st.switch_page("pages/3_⚙️_Process.py")
    
    if st.button("📊 View Analysis"):
        st.switch_page("pages/4_🔍_Analysis.py")

# Main content
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="metric-card">
        <h2>12</h2>
        <p>Total Cases</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <h2>1,234</h2>
        <p>Documents Processed</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <h2>89</h2>
        <p>Entities Found</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="metric-card">
        <h2>24</h2>
        <p>Reports Generated</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Recent cases
st.subheader("📁 Recent Cases")

# Mock data - replace with actual cases
cases_data = [
    {"id": "CASE_001", "name": "Investigation Alpha", "status": "Completed", "files": 45},
    {"id": "CASE_002", "name": "Project Beta", "status": "Processing", "files": 23},
    {"id": "CASE_003", "name": "Analysis Gamma", "status": "Active", "files": 67},
]

for case in cases_data:
    with st.container():
        col1, col2, col3, col4 = st.columns([2, 2, 1, 1])
        
        with col1:
            st.write(f"**{case['id']}**")
        with col2:
            st.write(case['name'])
        with col3:
            st.write(f"📄 {case['files']} files")
        with col4:
            if case['status'] == "Completed":
                st.success(case['status'])
            elif case['status'] == "Processing":
                st.warning(case['status'])
            else:
                st.info(case['status'])

st.markdown("---")

# Quick stats
st.subheader("📊 System Status")

col1, col2 = st.columns(2)

with col1:
    st.metric("Processing Queue", "3 files", "+2 today")
    st.metric("API Calls Today", "127", "+45 from yesterday")

with col2:
    st.metric("Average Processing Time", "2.3 min", "-0.5 min")
    st.metric("Success Rate", "98.5%", "+1.2%")

# Footer
st.markdown("---")
st.caption("Investigation Intelligence System v1.0.0 | Powered by AI")
```

#### Upload Page (`src/web/pages/2_📤_Upload.py`)

```python
import streamlit as st
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from src.main import InvestigationSystem

st.set_page_config(page_title="Upload Files", page_icon="📤", layout="wide")

st.title("📤 Upload Files")

# Check if case is selected
if not st.session_state.get('current_case'):
    st.error("⚠️ Please select or create a case first!")
    if st.button("Go to Cases"):
        st.switch_page("pages/1_📁_Cases.py")
    st.stop()

case_id = st.session_state.current_case

st.info(f"Uploading to case: **{case_id}**")

# Upload method selection
upload_method = st.radio(
    "Select upload method:",
    ["📁 Local Files", "☁️ Google Drive", "📦 Dropbox"],
    horizontal=True
)

st.markdown("---")

if upload_method == "📁 Local Files":
    st.subheader("Upload Files from Computer")
    
    # File uploader
    uploaded_files = st.file_uploader(
        "Drag and drop files here or click to browse",
        accept_multiple_files=True,
        type=['pdf', 'doc', 'docx', 'txt', 'csv', 'xlsx', 'xls', 
              'jpg', 'jpeg', 'png', 'mp3', 'mp4', 'mov'],
        help="Supported: PDF, DOC/DOCX, TXT, CSV, Excel, Images, Audio, Video"
    )
    
    if uploaded_files:
        st.success(f"✅ {len(uploaded_files)} file(s) selected")
        
        # Show file list
        with st.expander("📋 View selected files"):
            for file in uploaded_files:
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.write(file.name)
                with col2:
                    st.write(f"{file.size / 1024:.1f} KB")
                with col3:
                    st.write(file.type)
        
        # Upload button
        if st.button("🚀 Upload Files", type="primary"):
            with st.spinner("Uploading files..."):
                # Save uploaded files
                case_dir = Path(f"data/{case_id}/raw")
                case_dir.mkdir(parents=True, exist_ok=True)
                
                progress_bar = st.progress(0)
                
                for i, file in enumerate(uploaded_files):
                    file_path = case_dir / file.name
                    with open(file_path, 'wb') as f:
                        f.write(file.read())
                    
                    progress_bar.progress((i + 1) / len(uploaded_files))
                
                st.success(f"✅ Successfully uploaded {len(uploaded_files)} files!")
                st.balloons()
                
                if st.button("➡️ Process Files Now"):
                    st.switch_page("pages/3_⚙️_Process.py")

elif upload_method == "☁️ Google Drive":
    st.subheader("Upload from Google Drive")
    
    folder_id = st.text_input(
        "Google Drive Folder ID",
        placeholder="abc123def456...",
        help="Right-click folder → Get link → Copy ID from URL"
    )
    
    recursive = st.checkbox("Include subfolders", value=True)
    
    if st.button("🚀 Import from Google Drive", type="primary"):
        if not folder_id:
            st.error("Please enter a folder ID")
        else:
            with st.spinner("Importing from Google Drive..."):
                try:
                    system = st.session_state.system
                    files = system.ingest_from_google_drive(
                        folder_id=folder_id,
                        case_id=case_id,
                        recursive=recursive
                    )
                    st.success(f"✅ Imported {len(files)} files from Google Drive!")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

elif upload_method == "📦 Dropbox":
    st.subheader("Upload from Dropbox")
    
    folder_path = st.text_input(
        "Dropbox Folder Path",
        placeholder="/Evidence/Case001",
        help="Full path to Dropbox folder"
    )
    
    recursive = st.checkbox("Include subfolders", value=True)
    
    if st.button("🚀 Import from Dropbox", type="primary"):
        if not folder_path:
            st.error("Please enter a folder path")
        else:
            with st.spinner("Importing from Dropbox..."):
                try:
                    system = st.session_state.system
                    files = system.ingest_from_dropbox(
                        folder_path=folder_path,
                        case_id=case_id,
                        recursive=recursive
                    )
                    st.success(f"✅ Imported {len(files)} files from Dropbox!")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

# Sidebar info
with st.sidebar:
    st.info("""
    ### 📝 Supported File Types
    
    **Documents:**
    - PDF, DOC/DOCX, TXT
    
    **Data:**
    - CSV, XLS/XLSX, JSON
    
    **Media:**
    - Images: JPG, PNG, TIFF
    - Audio: MP3, WAV, M4A
    - Video: MP4, MOV
    
    **File Size:**
    - ♾️ Unlimited (chunked processing)
    """)
```

#### Processing Page (`src/web/pages/3_⚙️_Process.py`)

```python
import streamlit as st
from pathlib import Path
import sys
import time

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from src.main import InvestigationSystem

st.set_page_config(page_title="Process Case", page_icon="⚙️", layout="wide")

st.title("⚙️ Process Case")

if not st.session_state.get('current_case'):
    st.error("⚠️ Please select a case first!")
    st.stop()

case_id = st.session_state.current_case

st.info(f"Processing case: **{case_id}**")

# Processing options
st.subheader("Processing Options")

col1, col2 = st.columns(2)

with col1:
    enable_ocr = st.checkbox("Enable OCR for scanned documents", value=True)
    enable_transcription = st.checkbox("Transcribe audio/video files", value=True)

with col2:
    parallel_processing = st.checkbox("Enable parallel processing", value=True)
    max_workers = st.slider("Number of parallel workers", 1, 8, 4)

st.markdown("---")

# Start processing
if st.button("🚀 Start Processing", type="primary", use_container_width=True):
    
    # Processing status container
    status_container = st.container()
    
    with status_container:
        st.subheader("📊 Processing Status")
        
        # Progress bars
        overall_progress = st.progress(0)
        st.write("Overall Progress")
        
        current_file = st.empty()
        file_progress = st.progress(0)
        
        # Status messages
        status_text = st.empty()
        
        # Mock processing (replace with actual processing)
        files = ["document1.pdf", "data.xlsx", "audio.mp3", "contract.docx", "evidence.jpg"]
        
        for i, file in enumerate(files):
            current_file.write(f"Processing: **{file}**")
            status_text.info(f"🔄 Extracting content from {file}...")
            
            # Simulate processing steps
            for j in range(100):
                file_progress.progress(j / 100)
                time.sleep(0.01)
            
            overall_progress.progress((i + 1) / len(files))
            status_text.success(f"✅ Completed: {file}")
            time.sleep(0.5)
        
        st.success("🎉 Processing Complete!")
        st.balloons()
        
        # Show results
        st.markdown("---")
        st.subheader("📊 Processing Results")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Files Processed", "5")
        with col2:
            st.metric("Success Rate", "100%")
        with col3:
            st.metric("Total Records", "1,234")
        with col4:
            st.metric("Processing Time", "2m 34s")
        
        # Next steps
        st.markdown("---")
        st.subheader("➡️ Next Steps")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔍 Run Analysis", use_container_width=True):
                st.switch_page("pages/4_🔍_Analysis.py")
        
        with col2:
            if st.button("📄 Generate Report", use_container_width=True):
                st.switch_page("pages/6_📄_Reports.py")

# Show processing log
with st.expander("📝 View Processing Log"):
    st.code("""
[2025-11-13 19:30:01] INFO: Starting case processing: TEST001
[2025-11-13 19:30:02] INFO: Found 5 files to process
[2025-11-13 19:30:03] INFO: Processing document1.pdf
[2025-11-13 19:30:05] INFO: Extracted 1,234 text blocks
[2025-11-13 19:30:06] INFO: OCR completed successfully
[2025-11-13 19:30:07] SUCCESS: document1.pdf processed
...
[2025-11-13 19:32:35] SUCCESS: All files processed successfully
    """, language="log")
```

### Running the Streamlit App

```bash
# From project root
streamlit run src/web/app.py

# Or with custom port
streamlit run src/web/app.py --server.port 8080

# Access at http://localhost:8501
```

### Streamlit Configuration

Create `src/web/.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#667eea"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"

[server]
port = 8501
enableCORS = false
enableXsrfProtection = true

[browser]
gatherUsageStats = false
```

---

## Option 2: FastAPI + React (Production-Ready)

### Features
- 🚀 **RESTful API**
- 🔐 **Authentication & Authorization**
- 📱 **Modern React frontend**
- 🎨 **Tailwind CSS styling**
- 📊 **Real-time WebSocket updates**
- 🔄 **Background task processing**
- 📦 **Docker deployment ready**

### Installation

```bash
# Backend
pip install fastapi
pip install uvicorn[standard]
pip install python-multipart
pip install python-jose[cryptography]
pip install passlib[bcrypt]
pip install websockets
pip install celery
pip install redis

# Frontend (separate directory)
npx create-react-app investigation-frontend
cd investigation-frontend
npm install axios react-router-dom react-query
npm install @headlessui/react @heroicons/react
npm install recharts react-force-graph-2d
npm install tailwindcss
```

### Backend Structure

```
src/
└── api/
    ├── __init__.py
    ├── main.py                  # FastAPI app
    ├── auth.py                  # Authentication
    ├── dependencies.py          # Dependency injection
    ├── routers/
    │   ├── __init__.py
    │   ├── cases.py            # Case endpoints
    │   ├── upload.py           # File upload
    │   ├── processing.py       # Processing endpoints
    │   ├── analysis.py         # Analysis endpoints
    │   └── reports.py          # Report endpoints
    ├── models/
    │   ├── __init__.py
    │   ├── case.py
    │   ├── user.py
    │   └── task.py
    └── websockets/
        ├── __init__.py
        └── manager.py          # WebSocket manager
```

### Quick FastAPI Implementation

```python
# src/api/main.py
from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.main import InvestigationSystem

app = FastAPI(
    title="Investigation Intelligence API",
    description="AI-powered investigation and intelligence analysis",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global system instance
system = InvestigationSystem()

@app.get("/")
async def root():
    return {
        "message": "Investigation Intelligence API",
        "version": "1.0.0",
        "status": "operational"
    }

@app.post("/api/cases")
async def create_case(case_data: dict):
    """Create a new investigation case"""
    case_info = system.create_case(
        case_id=case_data['case_id'],
        name=case_data['name'],
        description=case_data.get('description', '')
    )
    return case_info

@app.get("/api/cases")
async def list_cases():
    """List all cases"""
    # Implement case listing
    return {"cases": []}

@app.post("/api/cases/{case_id}/upload")
async def upload_files(case_id: str, files: List[UploadFile] = File(...)):
    """Upload files to a case"""
    uploaded = []
    
    for file in files:
        # Save file
        file_path = Path(f"data/{case_id}/raw/{file.filename}")
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        uploaded.append(file.filename)
    
    return {"uploaded": uploaded, "count": len(uploaded)}

@app.post("/api/cases/{case_id}/process")
async def process_case(case_id: str):
    """Process all files in a case"""
    results = system.process_case(case_id)
    return results

@app.post("/api/cases/{case_id}/analyze")
async def analyze_case(case_id: str):
    """Run AI analysis on case"""
    results = system.analyze_case(case_id)
    return results

@app.post("/api/cases/{case_id}/report")
async def generate_report(case_id: str, formats: List[str] = ["pdf"]):
    """Generate investigation report"""
    paths = system.generate_report(case_id, formats)
    return {"report_paths": paths}

@app.get("/api/cases/{case_id}/status")
async def get_case_status(case_id: str):
    """Get case processing status"""
    # Implement status checking
    return {"status": "ready"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Running FastAPI

```bash
# Development
uvicorn src.api.main:app --reload

# Production
uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --workers 4

# Access API docs at http://localhost:8000/docs
```

---

## Comparison: Streamlit vs FastAPI+React

| Feature | Streamlit | FastAPI + React |
|---------|-----------|-----------------|
| **Setup Time** | 5 minutes | 2-3 hours |
| **Learning Curve** | Easy | Moderate |
| **Customization** | Limited | Full control |
| **Performance** | Good | Excellent |
| **Scalability** | Medium | High |
| **Multi-user** | Basic | Advanced |
| **Authentication** | Basic | Full OAuth/JWT |
| **Mobile Support** | Basic | Excellent |
| **Best For** | Internal tools, prototypes | Production apps |

---

## Recommendation

### Start with Streamlit if:
- ✅ You need something running TODAY
- ✅ Internal use only (small team)
- ✅ Rapid prototyping
- ✅ Python-only team

### Use FastAPI + React if:
- ✅ Production deployment
- ✅ Many concurrent users
- ✅ Need custom UI/UX
- ✅ Mobile app planned
- ✅ API-first architecture

---

## Next Steps

1. **Add to requirements.txt:**
   ```bash
   streamlit==1.29.0
   streamlit-aggrid==0.3.4
   plotly==5.18.0
   ```

2. **Create web interface:**
   ```bash
   mkdir -p src/web/pages
   # Copy code from above
   ```

3. **Run the app:**
   ```bash
   streamlit run src/web/app.py
   ```

4. **Access at:** http://localhost:8501

---

**Web interface can be fully implemented in 1-2 days with Streamlit!** 🚀
