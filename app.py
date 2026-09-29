"""
EduPulse AI - Smart Student Learning & Utility Suite
ShadowFox AI Engineering Internship - Beginner Level Project

Author: AI Engineer Intern
Tech Stack: Python, Streamlit, Google Gemini API, Pydantic
"""

import streamlit as st
import time
import os

from src.config import (
    APP_TITLE,
    APP_SUBTITLE,
    APP_VERSION,
    DEFAULT_MODEL,
    AVAILABLE_MODELS,
    MIN_INPUT_LENGTH,
    MAX_INPUT_LENGTH,
)
from src.validators import (
    validate_notes_input,
    validate_concept_input,
    validate_answer_improvement,
)
from src.prompt_templates import (
    build_summarizer_prompt,
    build_quiz_prompt,
    build_answer_improver_prompt,
    build_concept_explainer_prompt,
)
from src.llm_service import LLMService
from src.quiz_parser import parse_quiz_markdown
from src.mock_service import (
    SAMPLE_NOTES,
    SAMPLE_QA,
    SAMPLE_CONCEPT,
)

# ---------------------------------------------------------
# Page Configuration & Styling
# ---------------------------------------------------------
st.set_page_config(
    page_title="EduPulse AI | Student Learning Suite",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for Modern, Clean Academic UI
st.markdown("""
<style>
    /* Metric styling */
    div[data-testid="stMetricValue"] {
        font-size: 1.5rem !important;
        font-weight: 700;
        color: #1E3A8A;
    }
    
    /* Header card */
    .hero-banner {
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
        padding: 1.5rem 2rem;
        border-radius: 12px;
        color: white;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .hero-banner h1 {
        color: white !important;
        margin: 0;
        font-size: 2.1rem;
        font-weight: 800;
    }
    .hero-banner p {
        color: #DBEAFE !important;
        margin-top: 0.5rem;
        font-size: 1.05rem;
    }
    
    /* Tag Pills */
    .badge-pill {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-right: 0.5rem;
        background-color: #EEF2FF;
        color: #4338CA;
        border: 1px solid #C7D2FE;
    }
    
    /* Sidebar info box */
    .sidebar-info {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 0.75rem 1rem;
        font-size: 0.85rem;
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# Session State Initialization
# ---------------------------------------------------------
if "notes_input" not in st.session_state:
    st.session_state.notes_input = ""
if "quiz_notes_input" not in st.session_state:
    st.session_state.quiz_notes_input = ""
if "exam_question_input" not in st.session_state:
    st.session_state.exam_question_input = ""
if "draft_answer_input" not in st.session_state:
    st.session_state.draft_answer_input = ""
if "concept_input" not in st.session_state:
    st.session_state.concept_input = ""
if "quiz_data" not in st.session_state:
    st.session_state.quiz_data = None
if "user_quiz_answers" not in st.session_state:
    st.session_state.user_quiz_answers = {}


# ---------------------------------------------------------
# Sidebar Configuration
# ---------------------------------------------------------
with st.sidebar:
    st.title("⚙️ AI Control Center")
    st.caption(f"EduPulse v{APP_VERSION} — ShadowFox Internship")

    # API Key Configuration
    env_key = os.getenv("GEMINI_API_KEY", "").strip()
    api_key_input = st.text_input(
        "🔑 Google Gemini API Key",
        value=env_key,
        type="password",
        help="Enter your Gemini API key. Get a free key at https://aistudio.google.com/app/apikey",
    )

    # Demo Mode Switch
    default_mock = not bool(api_key_input or env_key)
    demo_mode = st.checkbox(
        "🧪 Demo / Offline Mode (No API key needed)",
        value=default_mock,
        help="Use realistic offline responses for demonstration and evaluation without calling live API.",
    )

    # Status Banner
    if demo_mode:
        st.info("🟡 **Status:** Running in Offline Demo Mode")
    elif api_key_input:
        st.success("🟢 **Status:** Gemini API Key Active")
    else:
        st.warning("⚠️ **Status:** No API Key Provided")

    st.markdown("---")
    st.subheader("Model Parameters")
    selected_model = st.selectbox(
        "Select Gemini Model",
        options=AVAILABLE_MODELS,
        index=0,
        help="Gemini 2.5 Flash and 1.5 Flash offer ultra-low latency and generous free tier quotas.",
    )

    temperature = st.slider(
        "Creativity (Temperature)",
        min_value=0.0,
        max_value=1.0,
        value=0.4,
        step=0.05,
        help="Lower values produce more deterministic, factual responses. Recommended: 0.3 - 0.5 for academic notes.",
    )

    st.markdown("---")
    # Project & Internship Info
    st.markdown(
        """
        <div class="sidebar-info">
            <strong>ShadowFox AI Engineer Internship</strong><br>
            • Track: <b>Beginner Level</b><br>
            • Task: AI-Powered Student Utility<br>
            • Core Focus: Input Validation, Interactive Quizzes & Student Workflows.
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------
# LLM Service Client Factory
# ---------------------------------------------------------
active_key = api_key_input.strip() if api_key_input else env_key
llm_service = LLMService(
    api_key=active_key,
    model_name=selected_model,
    mock_mode=demo_mode,
)


# ---------------------------------------------------------
# Hero Banner
# ---------------------------------------------------------
st.markdown(
    f"""
    <div class="hero-banner">
        <h1>🎓 {APP_TITLE}</h1>
        <p>{APP_SUBTITLE}</p>
        <div style="margin-top: 0.75rem;">
            <span class="badge-pill">📝 Smart Summaries</span>
            <span class="badge-pill">❓ Interactive Quizzes</span>
            <span class="badge-pill">✍️ Answer Evaluator</span>
            <span class="badge-pill">💡 Feynman Explainer</span>
            <span class="badge-pill">🛡️ Strict Input Guardrails</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# Main Application Tabs
# ---------------------------------------------------------
tab_summary, tab_quiz, tab_answer, tab_concept = st.tabs([
    "📝 1. Notes Summarizer",
    "❓ 2. Quiz & Flashcards",
    "✍️ 3. Answer Improver",
    "💡 4. Concept Explainer",
])


# =========================================================
# TAB 1: NOTES SUMMARIZER
# =========================================================
with tab_summary:
    st.subheader("📝 Intelligent Note Summarization & Key Extraction")
    st.write(
        "Transform raw lecture notes, textbook chapters, or transcripts into structured, "
        "high-retention revision guides with core definitions, takeaways, and recall flash-checks."
    )

    col_presets, col_upload = st.columns([2, 1])
    with col_presets:
        st.write("**Quick-Load Sample Notes:**")
        p_col1, p_col2 = st.columns(2)
        if p_col1.button("📂 Load OS Deadlocks Notes", key="btn_load_os"):
            st.session_state.notes_input = SAMPLE_NOTES["Operating Systems (Deadlocks)"]
            st.rerun()
        if p_col2.button("📂 Load Biology Photosynthesis", key="btn_load_bio"):
            st.session_state.notes_input = SAMPLE_NOTES["Biology (Photosynthesis)"]
            st.rerun()

    with col_upload:
        uploaded_file = st.file_uploader("Or Upload Note File (.txt, .md)", type=["txt", "md"], key="file_sum")
        if uploaded_file is not None:
            st.session_state.notes_input = uploaded_file.read().decode("utf-8")

    # Content Input
    notes_text = st.text_area(
        "Enter or Paste Study Notes:",
        value=st.session_state.notes_input,
        height=220,
        placeholder="Paste your lecture notes, textbook excerpts, or reading assignments here...",
        key="txt_notes_area",
    )
    # Update session state
    st.session_state.notes_input = notes_text

    # Controls
    ctrl_col1, ctrl_col2, ctrl_col3 = st.columns([1, 1, 1])
    with ctrl_col1:
        summary_style = st.selectbox(
            "Summary Depth",
            ["Standard Study Guide", "Quick Executive TL;DR", "Deep Exam Cram Guide"],
            index=0,
        )
    with ctrl_col2:
        academic_tier = st.selectbox(
            "Academic Target Level",
            ["Undergraduate / College", "High School / AP", "Graduate / Advanced"],
            index=0,
        )
    with ctrl_col3:
        char_count = len(notes_text)
        word_count = len(notes_text.split())
        st.metric("Input Length", f"{word_count:,} words", f"{char_count:,} characters")

    # Generate Action
    if st.button("🚀 Generate Revision Guide", type="primary", key="btn_gen_summary"):
        # 1. Validation
        is_valid, err_msg = validate_notes_input(notes_text)
        if not is_valid:
            st.error(err_msg)
        else:
            prompt_pkg = build_summarizer_prompt(notes_text, summary_style, academic_tier)
            with st.spinner("🧠 Synthesizing key concepts and structuring study guide..."):
                response = llm_service.execute_prompt(
                    system_instruction=prompt_pkg["system_instruction"],
                    user_prompt=prompt_pkg["user_prompt"],
                    temperature=temperature,
                    task_type="summarizer",
                )

            if not response["success"]:
                st.error(response["error"])
            else:
                st.success(f"✅ Generated in {response['metadata']['duration_sec']}s using `{response['metadata']['model']}`")
                
                # Metrics comparison
                out_words = len(response["content"].split())
                reduction_pct = round((1 - (out_words / max(word_count, 1))) * 100, 1)
                m1, m2, m3 = st.columns(3)
                m1.metric("Original Words", f"{word_count:,}")
                m2.metric("Structured Digest", f"{out_words:,} words")
                m3.metric("Information Density", f"{max(0, reduction_pct)}% condensed")

                # Formatted Output
                st.markdown("---")
                st.markdown(response["content"])

                # Download button
                st.download_button(
                    label="📥 Download Study Digest (.md)",
                    data=response["content"],
                    file_name="EduPulse_Study_Digest.md",
                    mime="text/markdown",
                )


# =========================================================
# TAB 2: INTERACTIVE QUIZ GENERATOR
# =========================================================
with tab_quiz:
    st.subheader("❓ Knowledge Assessment & Interactive Quiz Generation")
    st.write(
        "Generate multi-choice questions with answer keys, hints, and pedagogical explanations. "
        "Take the test directly in the browser to measure mastery."
    )

    q_col1, q_col2 = st.columns([2, 1])
    with q_col1:
        if st.button("📋 Copy Notes from Summarizer Tab", key="btn_copy_from_sum"):
            st.session_state.quiz_notes_input = st.session_state.notes_input
            st.rerun()

    quiz_notes = st.text_area(
        "Study Notes for Quiz Generation:",
        value=st.session_state.quiz_notes_input,
        height=180,
        placeholder="Enter notes to generate quiz questions from...",
        key="txt_quiz_notes",
    )
    st.session_state.quiz_notes_input = quiz_notes

    q_ctrl1, q_ctrl2, q_ctrl3 = st.columns(3)
    with q_ctrl1:
        num_q = st.select_slider("Number of Questions", options=[3, 5, 8], value=3)
    with q_ctrl2:
        diff_level = st.selectbox("Difficulty Level", ["Medium", "Easy", "Challenging"], index=0)
    with q_ctrl3:
        st.write("")
        st.write("")
        gen_quiz_btn = st.button("🎯 Build Interactive Quiz", type="primary", key="btn_gen_quiz")

    if gen_quiz_btn:
        is_valid, err_msg = validate_notes_input(quiz_notes, min_chars=30)
        if not is_valid:
            st.error(err_msg)
        else:
            prompt_pkg = build_quiz_prompt(quiz_notes, num_q, diff_level)
            with st.spinner("🤖 Formulating questions, distractors, and explanations..."):
                response = llm_service.execute_prompt(
                    system_instruction=prompt_pkg["system_instruction"],
                    user_prompt=prompt_pkg["user_prompt"],
                    temperature=temperature,
                    task_type="quiz",
                )

            if not response["success"]:
                st.error(response["error"])
            else:
                st.success(f"✅ Created {num_q} questions in {response['metadata']['duration_sec']}s")
                st.session_state.quiz_raw = response["content"]
                st.session_state.quiz_parsed = parse_quiz_markdown(response["content"])
                st.session_state.quiz_prompt_pkg = prompt_pkg
                st.session_state.user_quiz_answers = {}

    # Display Quiz if Available
    if "quiz_parsed" in st.session_state and st.session_state.quiz_parsed:
        st.markdown("---")
        st.markdown("### 📝 Live Interactive Quiz")
        st.caption("Select your answers below and click **Evaluate My Score**.")

        questions = st.session_state.quiz_parsed

        with st.form("quiz_interactive_form"):
            for idx, q in enumerate(questions):
                st.markdown(f"#### Q{idx + 1}: {q['question']}")
                opt_keys = sorted(q["options"].keys())
                formatted_options = [f"[{k}] {q['options'][k]}" for k in opt_keys]
                
                selected = st.radio(
                    f"Select answer for Question {idx + 1}:",
                    options=formatted_options,
                    index=None,
                    key=f"q_radio_{idx}",
                    label_visibility="collapsed",
                )
                if selected:
                    # Extract the letter inside brackets e.g. '[A]' -> 'A'
                    user_choice = selected[1]
                    st.session_state.user_quiz_answers[idx] = user_choice

                # Hint Expander
                if q.get("hint"):
                    with st.expander(f"💡 Need a hint for Q{idx + 1}?"):
                        st.write(q["hint"])

                st.markdown("<br>", unsafe_allow_html=True)

            submitted = st.form_submit_button("📊 Submit & Grade My Answers", type="primary")

        if submitted:
            correct_count = 0
            st.markdown("### 🏆 Quiz Results & Diagnostic Breakdown")
            for idx, q in enumerate(questions):
                user_ans = st.session_state.user_quiz_answers.get(idx, "Unanswered")
                correct_ans = q["correct_answer"]

                is_correct = (user_ans == correct_ans)
                if is_correct:
                    correct_count += 1
                    st.success(f"**Q{idx + 1}: Correct!** You selected [{user_ans}]")
                else:
                    st.error(f"**Q{idx + 1}: Incorrect.** You selected: [{user_ans}] | Correct Answer: **[{correct_ans}]**")

                st.info(f"**Pedagogical Explanation:** {q.get('explanation', 'None provided.')}")
                st.markdown("---")

            score_pct = round((correct_count / len(questions)) * 100)
            score_col1, score_col2 = st.columns(2)
            score_col1.metric("Final Score", f"{correct_count} / {len(questions)}")
            score_col2.metric("Accuracy", f"{score_pct}%")

        # Raw Quiz Markdown View
        with st.expander("📄 View Full Raw Quiz with Answers"):
            st.markdown(st.session_state.get("quiz_raw", ""))


# =========================================================
# TAB 3: ANSWER IMPROVER & EVALUATOR
# =========================================================
with tab_answer:
    st.subheader("✍️ Weak Answer Diagnostic & Upgrade")
    st.write(
        "Submit an exam question along with a student's initial draft answer. "
        "The AI evaluates the response against academic rubrics, identifies missing concepts, and provides a polished model answer."
    )

    if st.button("📂 Load Sample Question & Weak Draft", key="btn_load_qa"):
        st.session_state.exam_question_input = SAMPLE_QA["question"]
        st.session_state.draft_answer_input = SAMPLE_QA["draft_answer"]
        st.rerun()

    col_q, col_a = st.columns(2)
    with col_q:
        exam_q = st.text_area(
            "Exam / Assignment Question:",
            value=st.session_state.exam_question_input,
            height=140,
            placeholder="e.g. Explain how TCP achieves reliable delivery compared to UDP...",
            key="txt_exam_q",
        )
        st.session_state.exam_question_input = exam_q

    with col_a:
        draft_a = st.text_area(
            "Student's Draft Answer (Weak/Unpolished):",
            value=st.session_state.draft_answer_input,
            height=140,
            placeholder="e.g. TCP is reliable and uses handshakes while UDP is faster...",
            key="txt_draft_a",
        )
        st.session_state.draft_answer_input = draft_a

    ans_ctrl1, ans_ctrl2 = st.columns([2, 1])
    with ans_ctrl1:
        target_benchmark = st.selectbox(
            "Target Academic Grade",
            ["A+ / High Distinction (Exemplar)", "First Class Honors", "Standard Passing Grade (B/C)"],
            index=0,
        )
    with ans_ctrl2:
        st.write("")
        st.write("")
        eval_btn = st.button("🔍 Evaluate & Upgrade Answer", type="primary", key="btn_eval_answer")

    if eval_btn:
        is_valid, err_msg = validate_answer_improvement(exam_q, draft_a)
        if not is_valid:
            st.error(err_msg)
        else:
            prompt_pkg = build_answer_improver_prompt(exam_q, draft_a, target_benchmark)
            with st.spinner("⚖️ Benchmarking against academic rubric and crafting exemplar..."):
                response = llm_service.execute_prompt(
                    system_instruction=prompt_pkg["system_instruction"],
                    user_prompt=prompt_pkg["user_prompt"],
                    temperature=temperature,
                    task_type="answer_improver",
                )

            if not response["success"]:
                st.error(response["error"])
            else:
                st.success(f"✅ Evaluated in {response['metadata']['duration_sec']}s using `{response['metadata']['model']}`")
                st.markdown("---")
                st.markdown(response["content"])


# =========================================================
# TAB 4: CONCEPT EXPLAINER (FEYNMAN TECHNIQUE)
# =========================================================
with tab_concept:
    st.subheader("💡 Multi-Level Concept Masterclass (Feynman Technique)")
    st.write(
        "Master abstract academic topics through cognitive scaffolding: intuitive 1-sentence definitions, "
        "real-world analogies, step-by-step mechanisms, and memorable mnemonics."
    )

    exp_col1, exp_col2 = st.columns([3, 1])
    with exp_col1:
        concept_term = st.text_input(
            "Enter Concept or Topic:",
            value=st.session_state.concept_input,
            placeholder="e.g., Gradient Descent, Transformer Self-Attention, Epigenetics, Capital Asset Pricing Model",
            key="txt_concept",
        )
        st.session_state.concept_input = concept_term
    with exp_col2:
        st.write("")
        st.write("")
        if st.button("🎲 Sample: Gradient Descent", key="btn_sample_concept"):
            st.session_state.concept_input = SAMPLE_CONCEPT
            st.rerun()

    exp_ctrl1, exp_ctrl2, exp_ctrl3 = st.columns([1, 1, 1])
    with exp_ctrl1:
        comp_level = st.selectbox(
            "Comprehension Level",
            ["Undergraduate / College", "ELI5 (Beginner / Analogy-Heavy)", "Deep Dive (Technical / Mathematical)"],
            index=0,
        )
    with exp_ctrl2:
        pedagogy_style = st.selectbox(
            "Teaching Approach",
            ["Analogy-Driven (Feynman Technique)", "First Principles & Socratic", "Exam Cram & Mnemonics"],
            index=0,
        )
    with exp_ctrl3:
        st.write("")
        st.write("")
        explain_btn = st.button("✨ Explain Concept", type="primary", key="btn_gen_explain")

    if explain_btn:
        is_valid, err_msg = validate_concept_input(concept_term)
        if not is_valid:
            st.error(err_msg)
        else:
            prompt_pkg = build_concept_explainer_prompt(concept_term, comp_level, pedagogy_style)
            with st.spinner(f"🧠 Synthesizing mental models for '{concept_term}'..."):
                response = llm_service.execute_prompt(
                    system_instruction=prompt_pkg["system_instruction"],
                    user_prompt=prompt_pkg["user_prompt"],
                    temperature=temperature,
                    task_type="concept_explainer",
                )

            if not response["success"]:
                st.error(response["error"])
            else:
                st.success(f"✅ Generated in {response['metadata']['duration_sec']}s using `{response['metadata']['model']}`")
                st.markdown("---")
                st.markdown(response["content"])


# Footer
st.markdown("---")
st.caption("EduPulse AI • ShadowFox AI Engineering Internship Submission • Powered by Google Gemini & Streamlit")
