# 🧠 MindMate Harmony

**AI-Powered Mental Wellness Tracker** | Built with JAC & Streamlit

Track your emotional state, identify triggers, and receive personalized coping strategies with intelligent analysis.

---

## ⚡ Quick Start

```bash
# Install dependencies
pip install jaclang streamlit requests pandas plotly

# Run web interface
streamlit run mindmate_frontend.py

# Or run CLI version
jac run mindmate_frontend.jac
```

Browser opens at `http://localhost:8501`

---

## 🎯 Features

**Core Functions**
- 📝 Mood tracking with AI analysis
- 🧠 9 trigger categories (work, health, relationships, etc.)
- 📊 Visual analytics dashboard
- 💡 Personalized advice & music recommendations
- 🔒 Local data storage (privacy-first)

**Intelligence**
- Auto-detect severity (Low/Medium/High)
- Keyword pattern matching (50+ keywords)
- Context-aware insights for each trigger type
- Crisis situation detection

---

## 📁 Files

```
mindmate/
├── mindmate_backend.jac      # JAC analysis engine
├── mindmate_frontend.py       # Streamlit web UI
├── mindmate_frontend.jac      # JAC CLI interface
├── requirements.txt           # Dependencies
└── mindmate_data.json         # Auto-generated storage
```

---

## 💻 Usage

### 1. Create Entry
- Describe your mood (be detailed)
- Choose severity or use auto-detect
- Get instant analysis with advice & music

**Example:**
```
"Feeling stressed about work deadlines. Boss keeps adding 
tasks and I'm worried about finishing on time."
```

**Result:**
- Severity: Medium
- Trigger: Work  
- Personalized advice (6 steps)
- Music: "Clair de Lune - Debussy"

### 2. View Analytics
- Severity distribution pie chart
- Trigger frequency bar chart
- Mood timeline scatter plot
- Filter by date/severity

### 3. Manage Data
- Export as JSON
- Search entries
- Delete individual entries
- Clear all data

---

## 🔧 Customization

**Add Triggers** (in `mindmate_frontend.py`):
```python
TRIGGER_KEYWORDS = {
    "work": ["job", "boss", "deadline"],
    "custom": ["keyword1", "keyword2"]  # Add yours
}
```

**Adjust Severity Detection**:
```python
high_words = ["crisis", "emergency", "your-word"]
medium_words = ["stressed", "anxious", "your-word"]
```

**Change Colors** (in CSS section):
```python
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| `streamlit not found` | `pip install streamlit` |
| `jac not found` | `pip install jaclang` |
| Port 8501 in use | Add `--server.port 8502` |
| Data not saving | Check write permissions |

---

## 🆘 Crisis Resources


*This app is for wellness tracking only, not emergency care.*

---

## 🔮 Roadmap

- [ ] REST API for JAC backend integration
- [ ] Real-time LLM insights (OpenAI/Claude)
- [ ] Mobile app version
- [ ] Mood prediction ML models
- [ ] Voice input support
- [ ] Cloud sync with encryption


## 🙏 Credits

Built by **Chris Philip**  
Powered by [JAC](https://jaseci.org) | [Streamlit](https://streamlit.io) | [Plotly](https://plotly.com)

---

**Made with 💙 for mental wellness**

⭐ Star this repo if it helped you | 🐛 [Report issues](https://github.com/yourusername/mindmate/issues)
