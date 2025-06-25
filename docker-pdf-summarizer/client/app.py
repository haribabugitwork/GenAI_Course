import streamlit as st
import requests
import os
from io import BytesIO
import time

# Configuration
API_BASE_URL = os.getenv('API_BASE_URL', 'http://nginx:80')

def main():
    st.set_page_config(
        page_title="PDF Summarizer",
        page_icon="📄",
        layout="wide"
    )
    
    st.title("📄 PDF Summarizer with Gemini AI")
    st.markdown("Upload a PDF file to generate an AI-powered summary")
    
    # Sidebar
    with st.sidebar:
        st.header("About")
        st.info(
            "This application uses Google's Gemini AI to create "
            "intelligent summaries of your PDF documents."
        )
        
        # Health check
        if st.button("Check API Status"):
            check_api_health()
    
    # Main interface
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_file = st.file_uploader(
            "Choose a PDF file",
            type="pdf",
            help="Upload a PDF file to generate a summary"
        )
        
        if uploaded_file is not None:
            st.success(f"File uploaded: {uploaded_file.name}")
            
            # File details
            file_details = {
                "Filename": uploaded_file.name,
                "File size": f"{uploaded_file.size} bytes"
            }
            st.json(file_details)
            
            if st.button("Generate Summary", type="primary"):
                generate_summary(uploaded_file)
    
    with col2:
        st.header("Instructions")
        st.markdown("""
        1. **Upload** a PDF file using the file uploader
        2. **Click** the "Generate Summary" button
        3. **Wait** for the AI to process your document
        4. **Download** the generated summary PDF
        """)

def check_api_health():
    """Check if the API is running."""
    try:
        with st.spinner("Checking API status..."):
            response = requests.get(f"{API_BASE_URL}/health", timeout=10)
            
        if response.status_code == 200:
            st.success("✅ API is running!")
            st.json(response.json())
        else:
            st.error(f"❌ API returned status code: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Failed to connect to API: {str(e)}")

def generate_summary(uploaded_file):
    """Generate summary by calling the API."""
    try:
        with st.spinner("🤖 Generating summary with Gemini AI..."):
            # Prepare file for upload
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
            
            # Make API request
            response = requests.post(
                f"{API_BASE_URL}/summarize-pdf/",
                files=files,
                timeout=300  # 5 minutes timeout
            )
        
        if response.status_code == 200:
            st.success("✅ Summary generated successfully!")
            
            # Create download button
            summary_filename = f"summary_{uploaded_file.name}"
            st.download_button(
                label="📥 Download Summary PDF",
                data=response.content,
                file_name=summary_filename,
                mime="application/pdf",
                type="primary"
            )
            
            st.balloons()
            
        else:
            st.error(f"❌ Error generating summary: {response.status_code}")
            if response.text:
                st.error(f"Details: {response.text}")
                
    except requests.exceptions.Timeout:
        st.error("⏰ Request timed out. Please try again with a smaller file.")
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Network error: {str(e)}")
    except Exception as e:
        st.error(f"❌ Unexpected error: {str(e)}")

if __name__ == "__main__":
    main()