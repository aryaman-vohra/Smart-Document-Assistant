import streamlit as st
import os
from pathlib import Path

# Import custom modules
from core.document_processor import DocumentProcessor
from core.ai_assistant import AIAssistant
from core.question_generator import QuestionGenerator
from utils.validators import validate_question
from config.settings import settings

# Page configuration
st.set_page_config(
    page_title="Smart Document Assistant",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
def load_css():
    css_file = Path("static/style.css")
    if css_file.exists():
        with open(css_file) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# Initialize session state
def initialize_session_state():
    if 'document_text' not in st.session_state:
        st.session_state.document_text = ""
    if 'document_name' not in st.session_state:
        st.session_state.document_name = ""
    if 'summary' not in st.session_state:
        st.session_state.summary = ""
    if 'current_mode' not in st.session_state:
        st.session_state.current_mode = "upload"
    if 'challenge_questions' not in st.session_state:
        st.session_state.challenge_questions = []
    if 'current_question_index' not in st.session_state:
        st.session_state.current_question_index = 0
    if 'user_answers' not in st.session_state:
        st.session_state.user_answers = {}
    if 'evaluations' not in st.session_state:
        st.session_state.evaluations = {}

initialize_session_state()

# Initialize processors
@st.cache_resource
def get_processors():
    return {
        'doc_processor': DocumentProcessor(),
        'ai_assistant': AIAssistant(),
        'question_generator': QuestionGenerator()
    }

processors = get_processors()

def main():
    st.markdown("<h1 class='main-header'>📚 Smart Document Assistant</h1>", unsafe_allow_html=True)
    
    # Check API key
    if not settings.GEMINI_API_KEY:
        st.error("⚠️ Gemini API key not found. Please set GEMINI_API_KEY in your .env file.")
        st.stop()
    
    # Sidebar navigation
    with st.sidebar:
        st.header("Navigation")
        
        if st.session_state.document_text:
            st.success(f"📄 Document loaded: {st.session_state.document_name}")
            
            mode = st.radio(
                "Choose interaction mode:",
                ["Ask Anything", "Challenge Me"],
                key="interaction_mode"
            )
            
            if st.button("🔄 Upload New Document"):
                reset_session()
                st.rerun()
        else:
            st.info("Please upload a document to get started")
    
    # Main content area
    if not st.session_state.document_text:
        show_upload_interface()
    else:
        show_document_interface()

def show_upload_interface():
    st.markdown("<div class='upload-section'>", unsafe_allow_html=True)
    st.header("📁 Upload Your Document")
    st.write("Upload a PDF or TXT file to get started with AI-powered document analysis.")
    
    uploaded_file = st.file_uploader(
        "Choose a file",
        type=['pdf', 'txt'],
        help="Supported formats: PDF, TXT (Max size: 10MB)"
    )
    
    if uploaded_file is not None:
        process_uploaded_file(uploaded_file)
    
    st.markdown("</div>", unsafe_allow_html=True)

def process_uploaded_file(uploaded_file):
    with st.spinner("Processing document..."):
        success, text, error = processors['doc_processor'].process_file(uploaded_file)
        
        if success:
            st.session_state.document_text = text
            st.session_state.document_name = uploaded_file.name
            
            # Generate summary
            summary = processors['ai_assistant'].generate_summary(text)
            st.session_state.summary = summary
            
            st.success("✅ Document processed successfully!")
            st.rerun()
        else:
            st.error(f"❌ Error: {error}")

def show_document_interface():
    # Display document summary
    st.markdown("<div class='summary-box'>", unsafe_allow_html=True)
    st.subheader("📋 Document Summary")
    st.write(st.session_state.summary)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Mode selection
    mode = st.session_state.get('interaction_mode', 'Ask Anything')
    
    if mode == "Ask Anything":
        show_qa_interface()
    else:
        show_challenge_interface()

def show_qa_interface():
    st.header("💬 Ask Anything")
    st.write("Ask any question about the document content.")
    
    question = st.text_area(
        "Your question:",
        placeholder="What are the main findings of this document?",
        height=100
    )
    
    col1, col2 = st.columns([1, 4])
    
    with col1:
        ask_button = st.button("🤔 Ask", type="primary")
    
    with col2:
        if st.button("🗑️ Clear History"):
            processors['ai_assistant'].clear_history()
            st.success("Conversation history cleared!")
    
    if ask_button and question:
        is_valid, error_msg = validate_question(question)
        
        if is_valid:
            with st.spinner("Thinking..."):
                answer_data = processors['ai_assistant'].answer_question(
                    question, st.session_state.document_text
                )
                
                st.markdown("<div class='question-box'>", unsafe_allow_html=True)
                st.write(f"**Question:** {question}")
                st.markdown("</div>", unsafe_allow_html=True)
                
                st.markdown("<div class='answer-box'>", unsafe_allow_html=True)
                st.write(f"**Answer:** {answer_data['answer']}")
                st.markdown(f"<div class='reference-text'>**Reference:** {answer_data['reference']}</div>", 
                           unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.error(f"❌ {error_msg}")

def show_challenge_interface():
    st.header("🎯 Challenge Me")
    st.write("Test your understanding with AI-generated questions.")
    
    # Generate questions if not already done
    if not st.session_state.challenge_questions:
        if st.button("🎲 Generate Challenge Questions", type="primary"):
            with st.spinner("Generating challenging questions..."):
                questions = processors['question_generator'].generate_challenge_questions(
                    st.session_state.document_text
                )
                st.session_state.challenge_questions = questions
                st.rerun()
    else:
        show_challenge_questions()

def show_challenge_questions():
    questions = st.session_state.challenge_questions
    current_idx = st.session_state.current_question_index
    
    # Progress indicator
    st.progress((current_idx + 1) / len(questions))
    st.write(f"Question {current_idx + 1} of {len(questions)}")
    
    if current_idx < len(questions):
        question_data = questions[current_idx]
        
        st.markdown("<div class='challenge-question'>", unsafe_allow_html=True)
        st.write(f"**Question {current_idx + 1}:** {question_data['question']}")
        st.write(f"*Type: {question_data['type'].title()}*")
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Answer input
        user_answer = st.text_area(
            "Your answer:",
            key=f"answer_{current_idx}",
            height=100,
            placeholder="Type your answer here..."
        )
        
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            if st.button("✅ Submit Answer", type="primary"):
                if user_answer.strip():
                    evaluate_answer(current_idx, user_answer, question_data)
                else:
                    st.error("Please provide an answer before submitting.")
        
        with col2:
            if current_idx < len(questions) - 1:
                if st.button("➡️ Next Question"):
                    st.session_state.current_question_index += 1
                    st.rerun()
        
        # Show evaluation if available
        if current_idx in st.session_state.evaluations:
            show_evaluation(current_idx)
    
    else:
        show_challenge_results()

def evaluate_answer(question_idx, user_answer, question_data):
    with st.spinner("Evaluating your answer..."):
        evaluation = processors['question_generator'].evaluate_answer(
            question_data['question'],
            user_answer,
            st.session_state.document_text,
            question_data['expected_answer']
        )
        
        st.session_state.evaluations[question_idx] = evaluation
        st.session_state.user_answers[question_idx] = user_answer
        st.rerun()

def show_evaluation(question_idx):
    evaluation = st.session_state.evaluations[question_idx]
    
    st.markdown("<div class='evaluation-box'>", unsafe_allow_html=True)
    st.write("### 📊 Evaluation Results")
    
    # Score display with color coding
    score = evaluation['score']
    if score >= 4:
        score_color = "#27AE60"  # Green
        score_emoji = "🌟"
    elif score >= 3:
        score_color = "#F39C12"  # Orange
        score_emoji = "👍"
    else:
        score_color = "#E74C3C"  # Red
        score_emoji = "📚"
    
    st.markdown(f"<div class='score-display' style='color: {score_color};'>{score_emoji} Score: {score}/5</div>", 
                unsafe_allow_html=True)
    
    st.write(f"**Feedback:** {evaluation['feedback']}")
    st.write(f"**Justification:** {evaluation['justification']}")
    st.markdown("</div>", unsafe_allow_html=True)

def show_challenge_results():
    st.header("🏆 Challenge Complete!")
    st.write("Here's your performance summary:")
    
    total_questions = len(st.session_state.challenge_questions)
    total_score = sum(st.session_state.evaluations.get(i, {}).get('score', 0) 
                     for i in range(total_questions))
    average_score = total_score / total_questions if total_questions > 0 else 0
    
    # Overall performance
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Questions Answered", total_questions)
    
    with col2:
        st.metric("Total Score", f"{total_score}/{total_questions * 5}")
    
    with col3:
        st.metric("Average Score", f"{average_score:.1f}/5")
    
    # Performance breakdown
    st.subheader("📈 Detailed Results")
    
    for i, question in enumerate(st.session_state.challenge_questions):
        with st.expander(f"Question {i+1}: {question['question'][:50]}..."):
            st.write(f"**Full Question:** {question['question']}")
            st.write(f"**Your Answer:** {st.session_state.user_answers.get(i, 'Not answered')}")
            
            if i in st.session_state.evaluations:
                eval_data = st.session_state.evaluations[i]
                st.write(f"**Score:** {eval_data['score']}/5")
                st.write(f"**Feedback:** {eval_data['feedback']}")
    
    # Action buttons
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 Try New Challenge"):
            st.session_state.challenge_questions = []
            st.session_state.current_question_index = 0
            st.session_state.user_answers = {}
            st.session_state.evaluations = {}
            st.rerun()
    
    with col2:
        if st.button("📚 Upload New Document"):
            reset_session()
            st.rerun()

def reset_session():
    """Reset all session state variables."""
    keys_to_reset = [
        'document_text', 'document_name', 'summary', 'current_mode',
        'challenge_questions', 'current_question_index', 'user_answers', 'evaluations'
    ]
    
    for key in keys_to_reset:
        if key in st.session_state:
            del st.session_state[key]
    
    # Clear AI assistant history
    processors['ai_assistant'].clear_history()

# Footer
def show_footer():
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #7F8C8D; font-size: 0.9em;'>
            Smart Document Assistant |  Aryaman_Vohra
        </div>
        """, 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
    show_footer()