# TESE V8 Engine - Quick Reference Card

## 📦 Complete Module List (17 files)

| # | Module | Purpose | Entry |
|---|--------|---------|-------|
| 1 | `whatsapp_parser.py` | Parse WhatsApp TXT exports | 1 |
| 2 | `slack_parser.py` | Parse Slack JSON exports | 2 |
| 3 | `skype_parser.py` | Parse Skype logs (JSON/TXT) | 3 |
| 4 | `email_eml_parser.py` | Parse individual .eml files | 4 |
| 5 | `email_mbox_parser.py` | Parse .mbox archives | 6 |
| 6 | `message_scorer.py` | Score messages (0-100) | 7 |
| 7 | `incident_flagger.py` | Flag high-risk incidents | 8 |
| 8 | `pattern_aggregator.py` | Aggregate patterns | 9 |
| 9 | `platform_correlator.py` | Correlate across platforms | 10 |
| 10 | `timeline_builder.py` | Build chronological timeline | 11 |
| 11 | `risk_orchestrator.py` | Orchestrate risk analysis | 12 |
| 12 | `report_generator.py` | Generate forensic reports | 13 |
| 13 | `ingestion_manager.py` | Manage multi-source ingestion | 15 |
| 14 | `ui_integration.py` | Connect to Streamlit UI | 17 |
| 15 | `suggested_questions.py` | Generate investigation questions | 18 |
| 16 | `video_overview.py` | Generate video scripts | 19 |
| 17 | `__init__.py` | Package initialization | - |

---

## ⚡ Quick Start (3 commands)

```bash
# 1. Navigate to project
cd "/Applications/TESE/TESE v9/investigation-system"

# 2. Extract engine
unzip tese_v8_complete_engine.zip -d tese_engine

# 3. Test installation
python3 -c "from tese_engine import MessageScorer; print('✅ SUCCESS')"
```

---

## 🔧 Essential Imports for app.py

```python
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "tese_engine"))

# Core Analysis
from message_scorer import MessageScorer
from incident_flagger import IncidentFlagger
from pattern_aggregator import PatternAggregator
from risk_orchestrator import RiskOrchestrator
from report_generator import ReportGenerator

# Parsers
from whatsapp_parser import WhatsAppParser
from slack_parser import SlackParser
from skype_parser import SkypeParser

# Timeline & Correlation
from platform_correlator import PlatformCorrelator
from timeline_builder import TimelineBuilder
```

---

## 🎯 Common Usage Patterns

### Pattern 1: Parse → Score → Report
```python
# Parse
parser = WhatsAppParser()
messages = parser.parse(text)

# Score
scorer = MessageScorer()
for msg in messages:
    score_info = scorer.score_message(msg['content'])
    msg.update(score_info)

# Report
generator = ReportGenerator()
analysis = {"messages": messages, "patterns": {}}
report = generator.generate_summary(analysis)
```

### Pattern 2: Full Pipeline
```python
# Initialize
scorer = MessageScorer()
flagger = IncidentFlagger()
aggregator = PatternAggregator()
orchestrator = RiskOrchestrator(scorer, flagger, aggregator)

# Process
analysis = orchestrator.process_messages(messages)
```

### Pattern 3: Cross-Platform
```python
correlator = PlatformCorrelator()
timeline_builder = TimelineBuilder()

# Merge platforms
platform_messages = {
    "whatsapp": whatsapp_msgs,
    "slack": slack_msgs
}
merged = correlator.correlate(platform_messages)
timeline = timeline_builder.build(merged)
```

---

## 🐛 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| Import error | Add `sys.path.insert()` to app.py |
| Module not found | Check `__init__.py` exists |
| Syntax error | Run `python3 -m py_compile tese_engine/*.py` |
| Streamlit crash | Check for circular imports |

---

## 📊 Typical Analysis Flow

```
1. INGEST
   └─→ Load sources (WhatsApp, Slack, etc.)

2. PARSE
   └─→ WhatsAppParser, SlackParser, etc.

3. CORRELATE
   └─→ PlatformCorrelator merges all platforms

4. TIMELINE
   └─→ TimelineBuilder sorts chronologically

5. ANALYZE
   └─→ RiskOrchestrator (scorer + flagger + aggregator)

6. REPORT
   └─→ ReportGenerator creates forensic report

7. PRESENT
   └─→ Display in Studio or export
```

---

## 💡 Integration Options

### A. Simple Button (5 minutes)
```python
if st.button("Analyze with TESE V8"):
    scorer = MessageScorer()
    # ... process messages
    st.write("Done!")
```

### B. Replace Placeholders (15 minutes)
```python
def build_basic_report():
    # OLD: return "Placeholder report"
    # NEW: Run TESE V8 pipeline
    analysis = orchestrator.process_messages(messages)
    return generator.generate_summary(analysis)
```

### C. Full Integration (30 minutes)
- Connect all parsers to Sources ingestion
- Wire RiskOrchestrator to scoring
- Link ReportGenerator to Studio
- Add SuggestedQuestions to Chat

---

## ✅ Validation Commands

```bash
# Check files
ls tese_engine/ | wc -l  # Should be 17

# Test import
python3 -c "from tese_engine import MessageScorer"

# Syntax check
python3 -m py_compile tese_engine/*.py

# Run app
streamlit run app.py
```

---

## 🎓 Learn More

- `INSTALLATION_GUIDE.md` - Complete installation
- Module docstrings - See individual `.py` files
- `demo_checkpoint15.py` - Working examples

---

**Status**: ✅ Production Ready
**Version**: TESE V8.0.0
**Date**: November 17, 2025
