import streamlit as st
import requests
import json
from typing import List
import time
from urllib.parse import urlparse
import os
from dotenv import load_dotenv
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="DocLens - Intelligent Document Analysis",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    .question-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
        color: #333;
    }
    
    .answer-card {
        background: #e8f4fd;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
        color: #333;
    }
    
    .error-card {
        background: #ffe6e6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #dc3545;
        margin: 1rem 0;
        color: #333;
    }
    
    .info-box {
        background: #d1ecf1;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #17a2b8;
        margin: 1rem 0;
        color: #333;
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        text-align: center;
        margin: 1rem 0;
        color: #333;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'questions' not in st.session_state:
    st.session_state.questions = [""]
if 'answers' not in st.session_state:
    st.session_state.answers = []
if 'processing' not in st.session_state:
    st.session_state.processing = False

def validate_url(url: str) -> bool:
    """Validate if the URL is properly formatted"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def is_pdf_url(url: str) -> bool:
    """Check if URL points to a PDF file"""
    return url.lower().endswith('.pdf') or 'pdf' in url.lower()

def add_question():
    """Add a new question input field"""
    st.session_state.questions.append("")

def remove_question(index: int):
    """Remove a question input field"""
    if len(st.session_state.questions) > 1:
        st.session_state.questions.pop(index)
        st.rerun()

def process_document():
    
    """Process the document and get answers"""
    if not st.session_state.pdf_url or not st.session_state.pdf_url.strip():
        st.error("Please enter a valid PDF URL")
        return
    
    # Filter out empty questions
    valid_questions = [q.strip() for q in st.session_state.questions if q.strip()]
    if not valid_questions:
        st.error("Please enter at least one question")
        return
    
    if not validate_url(st.session_state.pdf_url):
        st.error("Please enter a valid URL")
        return
    
    if not is_pdf_url(st.session_state.pdf_url):
        st.warning("The URL doesn't appear to point to a PDF file. Please ensure it's a valid PDF URL.")
    
    st.session_state.processing = True
    
    try:
        # Prepare the request
        payload = {
            "documents": st.session_state.pdf_url.strip(),
            "questions": valid_questions
        }
        
        # Make API call to your FastAPI backend
        # You'll need to update this URL to match your backend
        api_url = os.getenv("BACKEND_DOCLENS_API_URL")
        
        with st.spinner("Processing document and generating answers..."):
            response = requests.post(api_url, json=payload, timeout=120)
            
            if response.status_code == 200:
                result = response.json()
                st.session_state.answers = result.get('answers', [])
                st.success("Document processed successfully!")
            else:
                error_detail = response.json().get('detail', 'Unknown error occurred')
                st.error(f"Error processing document: {error_detail}")
                
    except requests.exceptions.RequestException as e:
        st.error(f"Connection error: {str(e)}")
        st.info("Please ensure your FastAPI backend is running on localhost:8000")
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")
    finally:
        st.session_state.processing = False

# Main header
st.markdown("""
<div class="main-header">
    <h1>📄 DocLens</h1>
    <p style="font-size: 1.2rem; margin: 0;">Intelligent Document Analysis with RAG</p>
    <p style="font-size: 1rem; margin: 0.5rem 0 0 0;">Upload PDF documents and get intelligent answers to your questions</p>
</div>
""", unsafe_allow_html=True)

# Sidebar for configuration
# with st.sidebar:
#     st.header("⚙️ Configuration")
    
#     # Backend URL configuration
#     st.subheader("Backend Settings")
#     backend_url = st.text_input(
#         "Backend URL",
#         value="https://doc-lens-three.vercel.app/",
#         help="URL of your FastAPI backend"
#     )
    
#     # API Key (if needed)
#     api_key = st.text_input(
#         "API Key (Optional)",
#         type="password",
#         help="API key for authentication (if required)"
#     )
    
#     st.divider()
    
#     # Information about the project
#     st.subheader("ℹ️ About DocLens")
#     st.markdown("""
#     DocLens uses advanced AI technology to:
#     - Extract text from PDF documents
#     - Create semantic embeddings
#     - Answer questions using RAG
#     - Provide accurate, context-aware responses
#     """)
    
#     # Status indicator
#     st.subheader("🔍 Backend Status")
#     try:
#         health_response = requests.get(f"{backend_url}/health", timeout=5)
#         if health_response.status_code == 200:
#             st.success("✅ Backend Connected")
#         else:
#             st.error("❌ Backend Error")
#     except:
#         st.error("❌ Backend Unreachable")
#         st.info("Make sure your FastAPI backend is running")

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.header("📚 Document Analysis")
    
    # PDF URL input
    st.subheader("1. Document Input")
    pdf_url = st.text_input(
        "PDF Document URL",
        placeholder="https://example.com/document.pdf",
        help="Enter the URL of the PDF document you want to analyze"
    )
    
    if pdf_url:
        st.session_state.pdf_url = pdf_url
        
        # URL validation feedback
        if validate_url(pdf_url):
            if is_pdf_url(pdf_url):
                st.success("✅ Valid PDF URL detected")
            else:
                st.warning("⚠️ URL format is valid, but doesn't appear to be a PDF")
        else:
            st.error("❌ Invalid URL format")

with col2:
    st.header("📊 Quick Stats")
    
    # Display metrics
    if st.session_state.answers:
        st.markdown("""
        <div class="metric-card">
            <h3>📈 Results</h3>
            <h2>{}</h2>
            <p>Questions Answered</p>
        </div>
        """.format(len(st.session_state.answers)), unsafe_allow_html=True)
        
        

# Questions section
st.header("❓ Questions")
st.markdown("Enter your questions below. You can add multiple questions to analyze different aspects of the document.")

# Dynamic question inputs
for i, question in enumerate(st.session_state.questions):
    col1, col2 = st.columns([6, 1])
    
    with col1:
        st.session_state.questions[i] = st.text_input(
            f"Question {i+1}",
            value=question,
            placeholder=f"Enter your question {i+1} here...",
            key=f"question_{i}"
        )
    
    with col2:
        if len(st.session_state.questions) > 1:
            if st.button("🗑️", key=f"remove_{i}", help="Remove this question"):
                remove_question(i)

# Add question button
if st.button("➕ Add Another Question", on_click=add_question):
    pass

st.divider()

# Process button
if st.button(
    "🚀 Process Document & Get Answers",
    on_click=process_document,
    disabled=st.session_state.processing,
    type="primary"
):
    pass

# Display results
if st.session_state.answers:
    st.header("💡 Answers")
    st.markdown("Here are the intelligent answers to your questions based on the document content:")
    
    for i, (question, answer) in enumerate(zip(st.session_state.questions, st.session_state.answers)):
        if question.strip():  # Only show for non-empty questions
            st.markdown(f"""
            <div class="question-card">
                <h4>❓ Question {i+1}:</h4>
                <p><strong>{question}</strong></p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="answer-card">
                <h4>💡 Answer:</h4>
                <p>{answer}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.divider()

# Information section
with st.expander("ℹ️ How DocLens Works"):
    st.markdown("""
    ### 🔍 **Document Processing Pipeline**
    
    1. **PDF Extraction**: Downloads and extracts text from your PDF document
    2. **Text Chunking**: Breaks down the document into manageable chunks
    3. **Vector Embeddings**: Creates semantic embeddings using advanced AI models
    4. **Question Processing**: Analyzes your questions and finds relevant document sections
    5. **RAG Generation**: Uses Retrieval-Augmented Generation to provide accurate answers
    
    ### 🚀 **Key Features**
    
    - **Semantic Search**: Finds relevant information even with paraphrased questions
    - **Context-Aware**: Considers document context for accurate responses
    - **Fast Processing**: Optimized for quick response times
    - **Multiple Questions**: Process multiple questions in a single request
    
    ### 📋 **Best Practices**
    
    - Use clear, specific questions for better results
    - Ensure PDF URLs are publicly accessible
    - Questions should relate to the document content
    - For complex topics, break down into multiple questions
    """)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666; padding: 1rem;'>"
    "Built with ❤️ using Streamlit and FastAPI | DocLens v1.0.0"
    "</div>",
    unsafe_allow_html=True
)


