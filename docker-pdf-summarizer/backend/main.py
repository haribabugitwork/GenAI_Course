from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import tempfile
import os
from pdf_processor import PDFProcessor
from gemini_client import GeminiClient
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="PDF Summarizer API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize processors
pdf_processor = PDFProcessor()
gemini_client = GeminiClient()

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "pdf-summarizer"}

@app.post("/summarize-pdf/")
async def summarize_pdf(file: UploadFile = File(...)):
    try:
        # Validate file type
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")
        
        # Create temporary file for uploaded PDF
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_pdf_path = temp_file.name
        
        try:
            # Extract text from PDF
            logger.info(f"Processing PDF: {file.filename}")
            text_content = pdf_processor.extract_text(temp_pdf_path)
            
            if not text_content.strip():
                raise HTTPException(status_code=400, detail="No text content found in PDF")
            
            # Generate summary using Gemini
            logger.info("Generating summary with Gemini AI")
            summary = await gemini_client.generate_summary(text_content)
            
            # Create summary PDF
            summary_pdf_path = pdf_processor.create_summary_pdf(summary, file.filename)
            
            # Return the summary PDF
            return FileResponse(
                summary_pdf_path,
                media_type="application/pdf",
                filename=f"summary_{file.filename}",
                headers={"Content-Disposition": f"attachment; filename=summary_{file.filename}"}
            )
            
        finally:
            # Clean up temporary file
            if os.path.exists(temp_pdf_path):
                os.unlink(temp_pdf_path)
                
    except Exception as e:
        logger.error(f"Error processing PDF: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)