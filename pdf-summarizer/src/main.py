from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import tempfile
import os
from pathlib import Path
import logging
from dotenv import load_dotenv

from .services.pdf_processor import PDFProcessor
from .services.gemini_service import GeminiService
from .models.schemas import SummaryResponse

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="PDF Summarizer API",
    description="AI-powered PDF summarization using Google Gemini",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
pdf_processor = PDFProcessor()
gemini_service = GeminiService()

@app.get("/")
async def root():
    return {
        "message": "PDF Summarizer API",
        "version": "1.0.0",
        "endpoints": {
            "summarize": "/summarize",
            "health": "/health",
            "docs": "/docs"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "PDF Summarizer API"}

@app.post("/summarize", response_model=SummaryResponse)
async def summarize_pdf(file: UploadFile = File(...)):
    """
    Upload a PDF file and get an AI-generated summary as a downloadable PDF
    """
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    if file.size > 10 * 1024 * 1024:  # 10MB limit
        raise HTTPException(status_code=400, detail="File size must be less than 10MB")
    
    try:
        # Create temporary file for uploaded PDF
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_pdf_path = temp_file.name
        
        logger.info(f"Processing PDF: {file.filename}")
        
        # Extract text from PDF
        extracted_text = pdf_processor.extract_text(temp_pdf_path)
        
        if not extracted_text.strip():
            raise HTTPException(status_code=400, detail="No text could be extracted from the PDF")
        
        logger.info(f"Extracted {len(extracted_text)} characters from PDF")
        
        # Generate summary using Gemini
        summary = await gemini_service.generate_summary(extracted_text)
        
        logger.info("Summary generated successfully")
        
        # Create summary PDF
        summary_pdf_path = pdf_processor.create_summary_pdf(
            summary, 
            f"Summary of {file.filename}"
        )
        
        # Clean up temporary uploaded file
        os.unlink(temp_pdf_path)
        
        # Prepare response
        summary_filename = f"summary_{file.filename}"
        
        return SummaryResponse(
            original_filename=file.filename,
            summary_text=summary,
            summary_pdf_path=summary_pdf_path,
            summary_filename=summary_filename,
            message="Summary generated successfully"
        )
    
    except Exception as e:
        logger.error(f"Error processing PDF: {str(e)}")
        # Clean up temporary files
        if 'temp_pdf_path' in locals():
            try:
                os.unlink(temp_pdf_path)
            except:
                pass
        
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")

@app.get("/download/{filename}")
async def download_summary(filename: str):
    """
    Download the generated summary PDF
    """
    file_path = Path(f"/tmp/{filename}")
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type='application/pdf'
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)