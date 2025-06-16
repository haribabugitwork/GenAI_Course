import streamlit as st
import requests
import io
import os
from pathlib import Path
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
API_BASE_URL = os.getenv('API_BASE_URL', 'http://localhost:8000')

def main():
    st.set_page_config(
        page_title="PDF Summarizer",
        page_icon="📄",
        layout="wide"
    )
    
    # Custom CSS
    st.markdown("""
    <style>
    .main-header {
        text-align: center;
        color: #2E86AB;
        margin-bottom: 2rem;
    }
    .upload-section {
        border: 2px dashed #cccccc;
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
        margin: 1rem 0;
    }
    .summary-section {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    .success-message {
        color: #28a745;
        font-weight: bold;
    }
    .error-message {
        color: #dc3545;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown('<h1 class="main-header">📄 PDF Summarizer AI</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #666;">Upload a PDF document and get an AI-generated summary powered by Google Gemini</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("ℹ️ About")
        st.write("""
        This app uses Google Gemini AI to create intelligent summaries of PDF documents.
        
        **Features:**
        - Extract text from PDF files
        - Generate AI-powered summaries
        - Download summary as PDF
        - Support for documents up to 10MB
        """)
        
        st.header("🔧 API Status")
        if st.button("Check API Health"):
            check_api_health()
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<div class="upload-section">', unsafe_allow_html=True)
        st.subheader("📁 Upload PDF Document")
        
        uploaded_file = st.file_uploader(
            "Choose a PDF file",
            type=['pdf'],
            help="Upload a PDF file (max 10MB)"
        )
        
        if uploaded_file:
            # Display file info
            st.success(f"✅ File uploaded: {uploaded_file.name}")
            st.info(f"📊 File size: {uploaded_file.size / 1024:.1f} KB")
            
            # Process button
            if st.button("🚀 Generate Summary", type="primary"):
                process_pdf(uploaded_file)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.subheader("📋 Instructions")
        st.write("""
        1. **Upload** a PDF file using the file uploader
        2. **Click** the "Generate Summary" button
        3. **Wait** for the AI to process your document
        4. **View** the summary and download the PDF
        
        **Supported formats:** PDF only
        **Max file size:** 10MB
        **Processing time:** 30-60 seconds
        """)

def check_api_health():
    """Check if the API is running"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            st.sidebar.success("✅ API is healthy")
        else:
            st.sidebar.error("❌ API is not responding correctly")
    except requests.exceptions.RequestException:
        st.sidebar.error("❌ Cannot connect to API. Make sure the server is running.")

def process_pdf(uploaded_file):
    """Process the uploaded PDF file"""
    try:
        # Show progress
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        status_text.text("📤 Uploading file...")
        progress_bar.progress(20)
        
        # Prepare the file for upload
        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
        
        status_text.text("🤖 Processing with AI...")
        progress_bar.progress(40)
        
        # Send request to API
        response = requests.post(
            f"{API_BASE_URL}/summarize",
            files=files,
            timeout=120  # 2 minutes timeout
        )
        
        progress_bar.progress(80)
        
        if response.status_code == 200:
            progress_bar.progress(100)
            status_text.text("✅ Summary generated successfully!")
            
            result = response.json()
            display_results(result)
            
        else:
            st.error(f"❌ Error: {response.text}")
            
    except requests.exceptions.Timeout:
        st.error("⏰ Request timed out. The document might be too large or complex.")
    except requests.exceptions.RequestException as e:
        st.error(f"🔌 Connection error: {str(e)}")
    except Exception as e:
        st.error(f"❌ Unexpected error: {str(e)}")
    finally:
        # Clean up progress indicators
        if 'progress_bar' in locals():
            progress_bar.empty()
        if 'status_text' in locals():
            status_text.empty()

def display_results(result):
    """Display the summarization results"""
    st.markdown('<div class="summary-section">', unsafe_allow_html=True)
    
    # Success message
    st.markdown(f'<p class="success-message">{result["message"]}</p>', unsafe_allow_html=True)
    
    # Original filename
    st.write(f"**Original file:** {result['original_filename']}")
    
    # Summary text
    st.subheader("📝 Generated Summary")
    
    # Create tabs for different views
    tab1, tab2 = st.tabs(["📖 Formatted View", "📄 Raw Text"])
    
    with tab1:
        # Display formatted summary
        st.markdown(result['summary_text'])
    
    with tab2:
        # Display raw text in code block
        st.code(result['summary_text'], language='text')
    
    # Download section
    st.subheader("⬇️ Download Summary")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Text download
        st.download_button(
            label="📄 Download as Text",
            data=result['summary_text'],
            file_name=f"summary_{result['original_filename']}.txt",
            mime="text/plain"
        )
    
    with col2:
        # PDF download (this would require additional API call)
        if st.button("📑 Download as PDF"):
            st.info("PDF download functionality requires additional implementation")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Statistics
    with st.expander("📊 Summary Statistics"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Characters", len(result['summary_text']))
        
        with col2:
            word_count = len(result['summary_text'].split())
            st.metric("Words", word_count)
        
        with col3:
            paragraph_count = len([p for p in result['summary_text'].split('\n\n') if p.strip()])
            st.metric("Paragraphs", paragraph_count)

# Footer
def show_footer():
    st.markdown("---")
    st.markdown(
        '<p style="text-align: center; color: #666;">Built with ❤️ using Streamlit and Google Gemini AI</p>',
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
    show_footer()