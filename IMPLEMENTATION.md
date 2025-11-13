# 🚀 Implementation Guide - Investigation Intelligence System

## Quick Start (5 minutes)

### 1. Environment Setup

```bash
# Navigate to project
cd investigation-system

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install system dependencies (macOS)
brew install tesseract ffmpeg graphviz

# Set API key
export OPENAI_API_KEY="your-key-here"
```

### 2. First Case

```bash
# Create a case
python -m src.main create-case --name "Test Case" --id TEST001

# Ingest local files
python -m src.main ingest \
    --source local \
    --path ./examples/sample_case/input_files \
    --case-id TEST001

# Run full pipeline
python -m src.main full-pipeline --case-id TEST001

# Find your report
ls -l data/TEST001/output/
```

## Component Implementation Status

### ✅ Completed
- [x] Main orchestrator (`src/main.py`)
- [x] Configuration system (`config/config.yaml`)
- [x] Logger utility (`src/utils/logger.py`)
- [x] Project structure and documentation

### 🔄 To Implement (Priority Order)

#### Phase 1: Core Processing (Week 1)
1. **File Router** (`src/processing/router.py`)
   - Detect file types
   - Route to appropriate processor
   
2. **Document Processors**
   - `src/processing/pdf_processor.py` - PDF + OCR
   - `src/processing/document_processor.py` - DOC/DOCX/TXT
   - `src/processing/spreadsheet_processor.py` - XLS/XLSX

3. **Data Normalizer** (`src/normalization/normalizer.py`)
   - Convert all to JSON format
   - Chunked processing for large files

#### Phase 2: Ingestion (Week 1-2)
4. **Ingestion Modules**
   - `src/ingestion/local_folder.py` - Local files (PRIORITY)
   - `src/ingestion/google_drive.py` - Google Drive API
   - `src/ingestion/dropbox.py` - Dropbox API

#### Phase 3: Analysis (Week 2-3)
5. **Analysis Layers**
   - `src/analysis/llm_interface.py` - OpenAI API wrapper
   - `src/analysis/extraction_layer.py` - Entity extraction
   - `src/analysis/context_layer.py` - Cross-doc reasoning
   - `src/analysis/investigation_layer.py` - Collusion detection

#### Phase 4: Intelligence (Week 3)
6. **Intelligence Features**
   - `src/intelligence/mind_map.py` - Graph building
   - `src/intelligence/self_prompting.py` - Question generation

#### Phase 5: Output (Week 4)
7. **Report Generation**
   - `src/output/pdf_generator.py` - PDF reports
   - `src/output/json_exporter.py` - JSON exports
   - `src/output/graph_exporter.py` - Graph visualization

## Detailed Implementation Notes

### 1. File Router (`src/processing/router.py`)

```python
import magic
from pathlib import Path

class FileRouter:
    def __init__(self, config):
        self.config = config
        self.processors = {
            'pdf': PDFProcessor(config),
            'doc': DocumentProcessor(config),
            # ... etc
        }
    
    def process_file(self, file_path: Path, case_id: str):
        # Detect file type
        file_type = self._detect_type(file_path)
        
        # Route to processor
        processor = self.processors.get(file_type)
        if not processor:
            raise ValueError(f"Unsupported file type: {file_type}")
        
        # Process with chunking for large files
        return processor.process(file_path, case_id)
    
    def _detect_type(self, file_path: Path) -> str:
        mime = magic.from_file(str(file_path), mime=True)
        # Map MIME type to internal type
        mapping = {
            'application/pdf': 'pdf',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'docx',
            # ... etc
        }
        return mapping.get(mime, 'unknown')
```

### 2. PDF Processor with OCR

```python
import PyPDF2
import pytesseract
from pdf2image import convert_from_path

class PDFProcessor:
    def process(self, file_path, case_id):
        try:
            # Try text extraction first
            text = self._extract_text(file_path)
            
            # If no text, use OCR
            if not text.strip():
                text = self._ocr_pdf(file_path)
            
            return {
                'type': 'pdf',
                'text': text,
                'pages': self._get_page_count(file_path),
                'metadata': self._extract_metadata(file_path)
            }
        except Exception as e:
            logger.error(f"PDF processing failed: {e}")
            raise
    
    def _extract_text(self, file_path):
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
        return text
    
    def _ocr_pdf(self, file_path):
        images = convert_from_path(file_path, dpi=300)
        text = ""
        for img in images:
            text += pytesseract.image_to_string(img, lang='eng+por')
        return text
```

### 3. LLM Interface

```python
from openai import OpenAI

class LLMInterface:
    def __init__(self, config):
        self.client = OpenAI(api_key=config['llm']['openai_api_key'])
        self.model = config['llm']['model']
    
    def extract_entities(self, text: str) -> dict:
        prompt = f"""
        Extract structured information from this text:
        - People (names, roles)
        - Organizations
        - Dates
        - Monetary amounts
        - Locations
        - Key events
        
        Text: {text}
        
        Return as JSON.
        """
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        
        return self._parse_json(response.choices[0].message.content)
    
    def generate_unasked_questions(self, context: str) -> list:
        prompt = f"""
        Given this investigation context, generate questions that should be asked but haven't been yet.
        Focus on:
        - Missing information
        - Unexplained events
        - Potential conflicts
        - Hidden relationships
        
        Context: {context}
        
        Return 10-20 prioritized questions.
        """
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return self._parse_questions(response.choices[0].message.content)
```

### 4. Mind Map Builder

```python
import networkx as nx
import matplotlib.pyplot as plt

class MindMapBuilder:
    def build(self, extraction_results, context_results, investigation_results):
        G = nx.Graph()
        
        # Add entities as nodes
        for entity in extraction_results['entities']:
            G.add_node(
                entity['name'],
                type=entity['type'],
                metadata=entity.get('metadata', {})
            )
        
        # Add relationships as edges
        for rel in context_results['relationships']:
            G.add_edge(
                rel['source'],
                rel['target'],
                type=rel['relationship_type'],
                weight=rel.get('confidence', 1.0)
            )
        
        # Run graph algorithms
        centrality = nx.betweenness_centrality(G)
        communities = nx.community.greedy_modularity_communities(G)
        
        return {
            'graph': nx.node_link_data(G),
            'metrics': {
                'centrality': centrality,
                'communities': [list(c) for c in communities]
            }
        }
    
    def visualize(self, graph_data, output_path):
        G = nx.node_link_graph(graph_data['graph'])
        
        plt.figure(figsize=(20, 20))
        pos = nx.spring_layout(G, k=0.5, iterations=50)
        
        nx.draw_networkx_nodes(G, pos, node_size=1000, node_color='lightblue')
        nx.draw_networkx_labels(G, pos, font_size=8)
        nx.draw_networkx_edges(G, pos, alpha=0.5)
        
        plt.axis('off')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
```

### 5. PDF Report Generator

```python
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table
from reportlab.lib.styles import getSampleStyleSheet

class PDFReportGenerator:
    def generate(self, analysis_results, case_id):
        output_path = f"data/{case_id}/output/{case_id}_report.pdf"
        
        doc = SimpleDocTemplate(output_path, pagesize=A4)
        story = []
        styles = getSampleStyleSheet()
        
        # 1. Cover Page
        story.append(Paragraph(f"Investigation Report: {case_id}", styles['Title']))
        story.append(Spacer(1, 12))
        
        # 2. Executive Summary
        story.append(Paragraph("Executive Summary", styles['Heading1']))
        story.append(Paragraph(analysis_results['context']['summary'], styles['Normal']))
        story.append(Spacer(1, 12))
        
        # 3. Key Entities
        story.append(Paragraph("Key Entities", styles['Heading1']))
        entities_data = [[e['name'], e['type'], e.get('role', 'Unknown')] 
                         for e in analysis_results['extraction']['entities'][:20]]
        t = Table([['Name', 'Type', 'Role']] + entities_data)
        story.append(t)
        story.append(Spacer(1, 12))
        
        # 4. Timeline
        story.append(Paragraph("Timeline of Events", styles['Heading1']))
        for event in analysis_results['context']['timeline']:
            story.append(Paragraph(
                f"{event['date']}: {event['description']}", 
                styles['Normal']
            ))
        story.append(Spacer(1, 12))
        
        # 5. Mind Map
        story.append(Paragraph("Relationship Map", styles['Heading1']))
        mind_map_path = f"data/{case_id}/analysis/mind_map.png"
        if os.path.exists(mind_map_path):
            story.append(Image(mind_map_path, width=500, height=500))
        story.append(Spacer(1, 12))
        
        # 6. Unasked Questions
        story.append(Paragraph("Critical Unasked Questions", styles['Heading1']))
        for i, question in enumerate(analysis_results['self_prompting']['questions'][:20], 1):
            story.append(Paragraph(
                f"{i}. {question['question']} (Priority: {question['priority']})",
                styles['Normal']
            ))
        story.append(Spacer(1, 12))
        
        # 7. Hidden Relationships
        story.append(Paragraph("Hidden Relationships & Hypotheses", styles['Heading1']))
        for hyp in analysis_results['self_prompting']['hypotheses']:
            story.append(Paragraph(f"<b>{hyp['hypothesis']}</b>", styles['Normal']))
            story.append(Paragraph(f"Evidence: {hyp['evidence']}", styles['Normal']))
            story.append(Paragraph(f"Confidence: {hyp['confidence']}", styles['Normal']))
            story.append(Spacer(1, 6))
        
        # Build PDF
        doc.build(story)
        return output_path
```

## Testing Strategy

### Unit Tests
```python
# tests/test_processing.py
def test_pdf_processor():
    processor = PDFProcessor(config)
    result = processor.process('test.pdf', 'TEST001')
    assert result['type'] == 'pdf'
    assert len(result['text']) > 0
```

### Integration Tests
```python
# tests/test_full_pipeline.py
def test_full_pipeline():
    system = InvestigationSystem()
    case_id = "TEST_INTEGRATION"
    
    # Create case
    system.create_case(case_id, "Integration Test")
    
    # Ingest
    system.ingest_from_local('./test_data', case_id)
    
    # Process
    system.process_case(case_id)
    
    # Analyze
    system.analyze_case(case_id)
    
    # Generate report
    paths = system.generate_report(case_id)
    
    assert os.path.exists(paths['pdf'])
```

## Performance Optimization

### Chunked Processing for Large Files
```python
def process_large_file(file_path, chunk_size=10*1024*1024):
    """Process file in chunks to handle unlimited size."""
    with open(file_path, 'rb') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            yield process_chunk(chunk)
```

### Parallel Processing
```python
from concurrent.futures import ThreadPoolExecutor

def process_multiple_files(file_list, max_workers=4):
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(process_file, file_list))
    return results
```

## Deployment Checklist

- [ ] All dependencies installed
- [ ] API keys configured
- [ ] System dependencies (tesseract, ffmpeg, graphviz)
- [ ] Permissions for data directories
- [ ] Logging configured
- [ ] Test case runs successfully
- [ ] Documentation reviewed

## Next Steps

1. **Implement local file ingestion first** (easiest to test)
2. **Build PDF processor** (most common file type)
3. **Create basic LLM interface** (core functionality)
4. **Generate simple text report** (validate pipeline)
5. **Iterate and enhance**

## Support

For implementation questions or issues, refer to:
- Main documentation: `README.md`
- Configuration guide: `config/config.yaml`
- API reference: `docs/API.md` (to be created)
