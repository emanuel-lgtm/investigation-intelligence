# 🔍 Investigation Intelligence System

A comprehensive AI-powered investigation platform that ingests documents from multiple sources, performs deep analysis, and generates detailed investigative reports with mind mapping, relationship discovery, and self-prompting intelligence.

## 📋 Overview

This system transforms raw documents, audio, video, and data files into structured intelligence reports with:
- ✅ Unlimited file size support
- ✅ Multi-source ingestion (Google Drive, Dropbox, Local, External HD)
- ✅ Advanced AI analysis (V7-style extraction + NotebookLM reasoning + Investigation layer)
- ✅ Automatic mind mapping and relationship graphs
- ✅ Self-prompting: discovers unasked questions and hidden relationships
- ✅ Professional PDF reports with embedded visualizations

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        INGESTION LAYER                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │  Google  │  │ Dropbox  │  │  Local   │  │ External │       │
│  │  Drive   │  │   API    │  │  Folder  │  │    HD    │       │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘       │
│       └─────────────┴─────────────┴─────────────┘              │
│                          ▼                                       │
│              ┌─────────────────────────┐                        │
│              │  File Type Router       │                        │
│              │  (PDF/DOC/XLS/Audio/    │                        │
│              │   Video/Images)         │                        │
│              └────────┬────────────────┘                        │
└───────────────────────┼─────────────────────────────────────────┘
                        ▼
┌─────────────────────────────────────────────────────────────────┐
│                    NORMALIZATION LAYER                          │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐               │
│  │   OCR      │  │ Transcribe │  │  Parser    │               │
│  │ (Tesseract)│  │ (Whisper)  │  │ (openpyxl) │               │
│  └─────┬──────┘  └─────┬──────┘  └─────┬──────┘               │
│        └────────────────┴────────────────┘                      │
│                        ▼                                         │
│              ┌──────────────────────┐                          │
│              │  Unified JSON Store  │                          │
│              │  (Chunked Streaming) │                          │
│              └──────────┬───────────┘                          │
└───────────────────────────┼─────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                      ANALYSIS ENGINE                            │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              LAYER 1: EXTRACTION (V7-Style)              │  │
│  │  • Custom field detection                                │  │
│  │  • Entity extraction (people, companies, accounts)       │  │
│  │  • Structured data mining                                │  │
│  └───────────────────────┬──────────────────────────────────┘  │
│                          ▼                                       │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │           LAYER 2: CONTEXT (NotebookLM-Style)            │  │
│  │  • Cross-document reasoning                              │  │
│  │  • Timeline construction                                 │  │
│  │  • Summaries & meaning extraction                        │  │
│  └───────────────────────┬──────────────────────────────────┘  │
│                          ▼                                       │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │         LAYER 3: INVESTIGATION (Custom Logic)            │  │
│  │  • Collusion detection                                   │  │
│  │  • Inconsistency analysis                                │  │
│  │  • Anomaly detection                                     │  │
│  │  • Deception indicators                                  │  │
│  └───────────────────────┬──────────────────────────────────┘  │
└────────────────────────────┼─────────────────────────────────────┘
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                  INTELLIGENCE LAYER                             │
│  ┌──────────────────────────┐  ┌──────────────────────────┐    │
│  │   Mind Map Builder       │  │  Self-Prompting Engine   │    │
│  │   • Graph construction   │  │  • Unasked questions     │    │
│  │   • Relationship linking │  │  • Hidden relationships  │    │
│  │   • Network visualization│  │  • Hypotheses generation │    │
│  └────────────┬─────────────┘  └─────────────┬────────────┘    │
└────────────────┼────────────────────────────────┼────────────────┘
                 └────────────────┬───────────────┘
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                      OUTPUT LAYER                               │
│  ┌──────────────────────────┐  ┌──────────────────────────┐    │
│  │    PDF Report Generator  │  │  JSON/Graph Exports      │    │
│  │    (ReportLab)           │  │  • case_summary.json     │    │
│  │    • Executive summary   │  │  • graph.json            │    │
│  │    • Timeline            │  │  • embeddings (optional) │    │
│  │    • Mind map (embedded) │  │  • GraphML export        │    │
│  │    • Evidence tables     │  └──────────────────────────┘    │
│  │    • Hypotheses          │                                   │
│  └──────────────────────────┘                                   │
└─────────────────────────────────────────────────────────────────┘
```

## 📁 Project Structure

```
investigation-system/
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── config/
│   ├── config.yaml                   # Main configuration
│   └── credentials/                  # API keys and credentials
│       ├── google_drive_credentials.json
│       └── dropbox_token.txt
├── src/
│   ├── __init__.py
│   ├── main.py                       # Main orchestrator
│   ├── ingestion/                    # Data ingestion modules
│   │   ├── __init__.py
│   │   ├── base.py                  # Base ingestion class
│   │   ├── google_drive.py          # Google Drive connector
│   │   ├── dropbox.py               # Dropbox connector
│   │   ├── local_folder.py          # Local filesystem
│   │   └── external_hd.py           # External drive handler
│   ├── processing/                   # File processing
│   │   ├── __init__.py
│   │   ├── router.py                # File type router
│   │   ├── pdf_processor.py         # PDF handling + OCR
│   │   ├── document_processor.py    # DOC/DOCX/TXT
│   │   ├── spreadsheet_processor.py # XLS/XLSX/Numbers
│   │   ├── audio_processor.py       # Audio transcription
│   │   ├── video_processor.py       # Video transcription
│   │   └── image_processor.py       # Image OCR
│   ├── normalization/               # Data normalization
│   │   ├── __init__.py
│   │   ├── normalizer.py           # Main normalizer
│   │   └── json_store.py           # Unified JSON storage
│   ├── analysis/                    # AI analysis layers
│   │   ├── __init__.py
│   │   ├── extraction_layer.py     # Layer 1: V7-style extraction
│   │   ├── context_layer.py        # Layer 2: NotebookLM reasoning
│   │   ├── investigation_layer.py  # Layer 3: Investigation logic
│   │   └── llm_interface.py        # GPT-4/5 interface
│   ├── intelligence/                # Advanced intelligence
│   │   ├── __init__.py
│   │   ├── mind_map.py             # Mind map builder
│   │   ├── graph_builder.py        # Relationship graph
│   │   ├── self_prompting.py       # Question generation
│   │   └── hypothesis_generator.py  # Hidden relationship detection
│   ├── output/                      # Report generation
│   │   ├── __init__.py
│   │   ├── pdf_generator.py        # PDF report creation
│   │   ├── json_exporter.py        # JSON exports
│   │   └── graph_exporter.py       # Graph exports (JSON/GraphML)
│   └── utils/                       # Utilities
│       ├── __init__.py
│       ├── logger.py               # Logging setup
│       ├── chunking.py             # Chunked file processing
│       └── helpers.py              # Helper functions
├── tests/                           # Unit tests
│   ├── __init__.py
│   ├── test_ingestion.py
│   ├── test_processing.py
│   ├── test_analysis.py
│   └── test_output.py
├── data/                            # Data directory
│   ├── raw/                        # Raw ingested files
│   ├── normalized/                 # Normalized JSON
│   ├── analysis/                   # Analysis results
│   └── output/                     # Final reports
└── examples/                        # Example cases
    └── sample_case/
        ├── input_files/
        └── expected_output/
```

## 🔧 Installation

### Prerequisites

```bash
# System requirements
- Python 3.10+
- macOS (primary target)
- OpenAI API key (for GPT-4/5)
- Optional: Google Drive API credentials
- Optional: Dropbox API token
```

### Setup

```bash
# 1. Clone or create project directory
mkdir investigation-system
cd investigation-system

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Install system dependencies (macOS)
brew install tesseract         # OCR
brew install ffmpeg            # Audio/video processing
brew install graphviz          # Graph visualization

# 5. Configure credentials
cp config/config.yaml.example config/config.yaml
# Edit config.yaml with your API keys

# 6. Set up API credentials
# - Place google_drive_credentials.json in config/credentials/
# - Place dropbox_token.txt in config/credentials/
# - Add OPENAI_API_KEY to environment or config.yaml
```

## 🚀 Usage

### Basic Usage

```python
from src.main import InvestigationSystem

# Initialize system
system = InvestigationSystem(config_path="config/config.yaml")

# Create a new case
case = system.create_case(
    case_id="CASE_001",
    name="Investigation Alpha",
    description="Fraud investigation for Company X"
)

# Ingest from multiple sources
system.ingest_from_google_drive(
    folder_id="...",
    case_id="CASE_001"
)

system.ingest_from_dropbox(
    folder_path="/Evidence/Case001",
    case_id="CASE_001"
)

system.ingest_from_local(
    folder_path="/Users/you/Documents/Evidence",
    case_id="CASE_001"
)

# Process and analyze
system.process_case("CASE_001")

# Generate report
report_path = system.generate_report(
    case_id="CASE_001",
    output_format=["pdf", "json", "graph"]
)

print(f"Report generated: {report_path}")
```

### CLI Usage

```bash
# Create new case
python -m src.main create-case --name "Investigation Alpha" --id CASE_001

# Ingest from Google Drive
python -m src.main ingest \
    --source google_drive \
    --folder-id "abc123" \
    --case-id CASE_001

# Ingest from local folder
python -m src.main ingest \
    --source local \
    --path "/path/to/evidence" \
    --case-id CASE_001

# Process case
python -m src.main process --case-id CASE_001

# Generate report
python -m src.main report \
    --case-id CASE_001 \
    --format pdf,json,graph \
    --output ./reports/
```

## 📊 Data Flow

### 1. Ingestion Phase
```
Source → Download/Stream → Type Detection → Queue for Processing
```

### 2. Processing Phase
```
Raw File → Parser/OCR/Transcribe → Chunked Processing → JSON Record
```

### 3. Normalization Phase
```json
{
  "case_id": "CASE_001",
  "source_id": "gdrive_abc123",
  "type": "pdf",
  "origin": "google_drive",
  "location": "page_5",
  "speaker": null,
  "text": "Extracted content here...",
  "metadata": {
    "filename": "contract.pdf",
    "created": "2024-01-15",
    "modified": "2024-03-20",
    "author": "John Doe"
  }
}
```

### 4. Analysis Phase (3 Layers)

**Layer 1: Extraction**
- Custom fields: parties, dates, amounts, accounts
- Entity recognition: people, companies, locations
- Structured data extraction

**Layer 2: Context**
- Cross-reference documents
- Build timeline of events
- Generate summaries and meaning

**Layer 3: Investigation**
- Detect inconsistencies
- Flag suspicious patterns
- Identify potential collusion

### 5. Intelligence Phase
- Build relationship graph
- Generate mind map
- Self-prompt for unasked questions
- Propose hypotheses

### 6. Output Phase
- PDF report (12+ sections)
- JSON exports
- Graph data (JSON/GraphML)

## 🎯 Key Features

### 1. Multi-Source Ingestion
```python
# Supports unlimited file sizes via chunked streaming
system.ingest_from_google_drive(folder_id="...")
system.ingest_from_dropbox(folder_path="...")
system.ingest_from_local(folder_path="...")
system.ingest_from_external_hd(mount_path="/Volumes/Evidence")
```

### 2. Comprehensive File Support
- **Documents**: PDF, DOC/DOCX, TXT, HTML, Markdown
- **Data**: JSON, CSV, XLS/XLSX, Apple Numbers
- **Media**: JPG/PNG/TIFF, MP3/WAV/M4A, MP4/MOV
- **Special**: Screen recordings, voice memos, scanned documents

### 3. Three-Layer Analysis
- **V7-Style Extraction**: Unlimited custom fields
- **NotebookLM Context**: Cross-document reasoning
- **Investigation Logic**: Collusion, deception, anomalies

### 4. Self-Prompting Intelligence
**Unasked Questions:**
- "Who authorized this transfer?"
- "Why is Company X mentioned only in internal logs?"
- "Is there missing documentation for payment #442?"

**Hidden Relationships:**
- "Person C may act as intermediary between A and B"
- "Invoices 17-19 coincide with unusually high chat activity"

### 5. Mind Mapping & Visualization
- Automatic relationship graph
- Visual mind map embedded in PDF
- Export formats: JSON, GraphML, PNG

### 6. Professional Reporting
12-section PDF report:
1. Cover page
2. Executive summary
3. Key entities & roles
4. Timeline of events
5. Context & meaning
6. Collusion/impropriety analysis
7. Structured data tables
8. Mind-map diagram
9. Unasked questions
10. Hidden relationships
11. Evidence appendix
12. Next steps

## 🔐 Security & Privacy

- All processing happens locally (except LLM API calls)
- API keys stored securely in config/credentials/
- Optional: Use local LLM (Ollama/LLaMA) instead of OpenAI
- Data encryption at rest (optional)
- Audit logging for all operations

## 🛠️ Configuration

### config.yaml
```yaml
system:
  case_dir: "./data"
  temp_dir: "./data/temp"
  max_workers: 4
  
llm:
  provider: "openai"  # or "anthropic" or "local"
  model: "gpt-4-turbo-preview"
  api_key: "${OPENAI_API_KEY}"
  
ingestion:
  google_drive:
    enabled: true
    credentials_path: "config/credentials/google_drive_credentials.json"
  dropbox:
    enabled: true
    token_path: "config/credentials/dropbox_token.txt"
  
processing:
  chunk_size: 10485760  # 10MB chunks
  ocr_language: "eng"
  whisper_model: "large-v3"
  
analysis:
  extraction:
    custom_fields: ["parties", "dates", "amounts", "accounts", "entities"]
  context:
    max_context_docs: 50
  investigation:
    anomaly_threshold: 0.75
    
output:
  pdf:
    include_mind_map: true
    include_evidence: true
  json:
    pretty_print: true
  graph:
    formats: ["json", "graphml", "png"]
```

## 📚 API Reference

See `docs/API.md` for complete API documentation.

## 🧪 Testing

```bash
# Run all tests
pytest

# Run specific test suite
pytest tests/test_analysis.py

# Run with coverage
pytest --cov=src tests/
```

## 🤝 Contributing

This is a private investigation tool. For internal use only.

## 📄 License

Proprietary - All Rights Reserved

## 📞 Support

For questions or issues, contact the development team.

---

**Version**: 1.0.0  
**Last Updated**: November 2025  
**Python Version**: 3.10+  
**Platform**: macOS (primary), Linux (compatible)
