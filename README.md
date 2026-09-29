# 🎓 EduPulse AI — Intelligent Student Study & Revision Utility

> **ShadowFox AI Engineer Internship — Beginner Level Task Submission**  
> *An AI-powered academic utility suite built with Google Gemini API, Streamlit, and modern AI engineering best practices.*

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit App](https://img.shields.io/badge/UI-Streamlit-FF4B4B.svg)](https://streamlit.io/)
[![Google Gemini API](https://img.shields.io/badge/AI%20Model-Google%20Gemini%20Flash-4285F4.svg)](https://aistudio.google.com/)
[![Tests](https://img.shields.io/badge/Tests-13%20Passed-brightgreen.svg)]()
[![Explanation video](https://drive.google.com/file/d/1kERshskMR65Y2Brx8b50njPix7O_bEti/view?usp=drivesdk)]()
---

## 📌 Executive Summary

Most beginner LLM applications function as simple "pass-through" wrappers around generic chat endpoints. **EduPulse AI** is engineered as a **structured, pedagogical student workflow engine**. It bridges the gap between raw study materials and active learning by implementing four specialized academic modes, strict pre-flight input validation, robust API error handling, and structured prompt orchestration.

### 🌟 Key Highlights
- **4 Dedicated AI Student Utilities:** Notes Summarizer, Interactive Quiz & Assessment, Answer Improver & Evaluator, and Feynman Concept Explainer.
- **Strict Guardrails:** Pre-flight validation against empty inputs, character repetition/gibberish, and token overflow.
- **Production-Style Error Recovery:** Gracefully catches missing keys, `401 Unauthorized`, `429 Rate Limits`, and network timeouts with actionable user guidance.
- **Built-in Offline / Demo Mode:** Fully functional out-of-the-box without requiring live API keys or billing setup.
- **Interactive In-App Prompt Inspector:** Transparently reveals system instructions, interpolated prompts, and prompt engineering rationale directly inside the UI.

---

## 🏛️ System Architecture

```
                      ┌───────────────────────────────────────┐
                      │    Student Input (Notes / Answers)    │
                      └───────────────────┬───────────────────┘
                                          │
                                          ▼
                      ┌───────────────────────────────────────┐
                      │   Layer 1: Pre-Flight Guardrails      │
                      │   - Empty / whitespace check          │
                      │   - Min / max length enforcement      │
                      │   - Repetitive text & gibberish filter│
                      │   - Multi-field pairing verification  │
                      └───────────────────┬───────────────────┘
                                          │ (Cleaned & Validated)
                                          ▼
                      ┌───────────────────────────────────────┐
                      │   Layer 2: Prompt Orchestration       │
                      │   - Persona & Pedagogical System Inst.│
                      │   - Dynamic template interpolation    │
                      │   - Strict Markdown output schema     │
                      │   - Temperature calibration (0.3-0.5) │
                      └───────────────────┬───────────────────┘
                                          │
                                          ▼
                      ┌───────────────────────────────────────┐
                      │   Layer 3: Resilient LLM Gateway      │
                      │   - Google Gemini API (gemini-2.5-f)  │
                      │   - Rate-limit & 401 interceptor      │
                      │   - Offline Demo Mode fallback        │
                      └───────────────────┬───────────────────┘
                                          │
                                          ▼
                      ┌───────────────────────────────────────┐
                      │   Layer 4: Interactive Rendering      │
                      │   - Formatted Markdown digest         │
                      │   - Regex MCQ parser & auto-grader    │
                      │   - Word reduction metrics & export   │
                      └───────────────────────────────────────┘
```

---

## 🚀 Core Features

### 1. 📝 Smart Notes Summarizer & Key Extraction
- Ingests raw lecture notes, textbooks excerpts, or transcripts.
- Extracts an **Executive Overview**, **Key Concept Glossary**, **Thematic Breakdown**, **Common Exam Pitfalls**, and a **5-Minute Rapid Recall Checklist**.
- Computes real-time information density and word reduction metrics.
- Allows exporting study guides as `.md` markdown files.

### 2. ❓ Interactive Quiz Generator & Auto-Grader
- Formulates multi-choice questions with 4 distinct options, subtle hints, and detailed pedagogical explanations.
- **Interactive Mode:** Students can select answers directly in the browser and receive instant grading, score percentages, and explanations.

### 3. ✍️ Weak Answer Diagnostic & Upgrade
- Benchmarks student draft answers against exam questions using academic grading rubrics.
- Displays a **Diagnostic Evaluation Card** rating Conceptual Accuracy, Completeness, and Academic Tone.
- Outlines **Identified Gaps / Misconceptions** and crafts a **Model Exemplar Answer** for top marks.

### 4. 💡 Multi-Level Concept Explainer (Feynman Technique)
- Deconstructs difficult academic concepts across 3 comprehension tiers (ELI5, High School/College, Technical Deep Dive).
- Generates real-world relatable analogies, step-by-step mechanisms, and memorable mnemonics.

---

## 🧠 Prompt Engineering Philosophy

The prompts follow rigorous prompt design principles:
1. **Explicit Role Assignment:** Every prompt initiates with an academic tutor persona instructed to avoid generic conversational filler and produce structured learning content.
2. **Schema Enforcement:** Strict markdown templates guarantee reliable layout structure across all model completions.
3. **Temperature Calibration:**
   - `0.30` for Summarization: Ensures high factual fidelity without creative hallucination.
   - `0.35` for Answer Improvement: Provides objective, criteria-based evaluation.
   - `0.40` for Quiz Generation: Balances realistic distractors with accurate answer keys.
   - `0.50` for Concept Explanations: Fosters vivid, relatable analogies and metaphors.
4. **Scaffolding:** Features like progressive hints before revealing explanations encourage active learning over passive reading.

---

## 🛡️ Input Validation & Error Handling

| Scenario | Handled By | System Behavior |
| :--- | :--- | :--- |
| **Empty Input** | `src/validators.py` | Halts execution before API call; displays prompt suggestion. |
| **Input Too Short (< 30 chars)** | `src/validators.py` | Warns that notes lack sufficient content for meaningful synthesis. |
| **Gibberish / Repetition** | `src/validators.py` | Regex identifies repeated sequences (e.g. `aaaa...`) or low unique-word ratios. |
| **Missing API Key** | `src/llm_service.py` | Informs user with link to Google AI Studio and offers 1-click Demo Mode. |
| **Rate Limit (`429`)** | `src/llm_service.py` | Recommends cooldown period and alternative model selection. |
| **Invalid Key (`401`)** | `src/llm_service.py` | Differentiates key rejection from network errors. |

---

## 📂 Project Structure

```
EduPulse-AI/
├── .env.example              # Environment variables template
├── .gitignore                # Git exclusions (API keys, pycache, venv)
├── README.md                 # Complete project documentation
├── VIDEO_SCRIPT.md           # 3-5 minute video presentation script
├── requirements.txt          # Python dependencies
├── app.py                    # Streamlit web application
├── src/
│   ├── __init__.py
│   ├── config.py             # Config & environment settings
│   ├── llm_service.py        # Gemini client gateway & error handler
│   ├── prompt_templates.py   # Structured prompts & system instructions
│   ├── validators.py         # Input validation & sanitization
│   ├── quiz_parser.py        # Regex parser for interactive MCQs
│   └── mock_service.py       # Offline demo responses & sample datasets
└── tests/
    ├── __init__.py
    ├── test_validators.py    # Unit tests for input validation
    ├── test_prompts.py       # Unit tests for prompt generation
    ├── test_quiz_parser.py   # Unit tests for quiz parsing
    └── test_llm_service.py   # Unit tests for LLM error handling & mock mode
```

---

## 🛠️ Installation & Quickstart

### 1. Clone the Repository
```bash
git clone https://github.com/<your-username>/edupulse-ai.git
cd edupulse-ai
```

### 2. Create and Activate a Virtual Environment
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Your API Key (Optional)
Create a `.env` file from the template:
```bash
cp .env.example .env
```
Add your free Google Gemini API key obtained from [Google AI Studio](https://aistudio.google.com/app/apikey):
```env
GEMINI_API_KEY=your_gemini_api_key_here
```
*(Note: You can also enter the API key directly in the web app sidebar, or use the **Demo / Offline Mode** without any key!)*

### 5. Run the Application
```bash
streamlit run app.py
```
The web dashboard will automatically open in your default browser at `http://localhost:8501`.

### 6. Run Unit Tests
```bash
pytest -v
```
All 13 unit tests will execute and verify validators, prompt templates, quiz parsing, and error handling.

---

## 🎥 Video Presentation Guide

As required by the ShadowFox submission criteria, a complete **3 to 5 minute video script** is provided in [`VIDEO_SCRIPT.md`](./VIDEO_SCRIPT.md). It outlines exact timestamps, screen actions, and talking points covering:
1. Candidate & Project Introduction
2. Live Demonstration of all 4 Student Utilities
3. Prompt Engineering Architecture & In-App Prompt Inspector
4. Defensive Engineering (Validation & Error Handling)
5. Test Suite Verification

---

## ⚖️ License
Developed for educational evaluation under the ShadowFox AI Engineer Internship track.
