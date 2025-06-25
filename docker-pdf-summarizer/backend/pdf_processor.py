import PyPDF2
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import tempfile
import os
import logging

logger = logging.getLogger(__name__)

class PDFProcessor:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        
    def extract_text(self, pdf_path: str) -> str:
        """Extract text content from PDF file."""
        try:
            text_content = ""
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                for page_num, page in enumerate(pdf_reader.pages):
                    try:
                        page_text = page.extract_text()
                        text_content += f"\n--- Page {page_num + 1} ---\n{page_text}\n"
                    except Exception as e:
                        logger.warning(f"Error extracting text from page {page_num + 1}: {e}")
                        continue
                        
            return text_content.strip()
            
        except Exception as e:
            logger.error(f"Error reading PDF: {e}")
            raise Exception(f"Failed to extract text from PDF: {e}")
    
    def create_summary_pdf(self, summary_text: str, original_filename: str) -> str:
        """Create a new PDF with the summary content."""
        try:
            # Create temporary file for summary PDF
            temp_dir = tempfile.gettempdir()
            summary_filename = f"summary_{original_filename}"
            summary_path = os.path.join(temp_dir, summary_filename)
            
            # Create PDF document
            doc = SimpleDocTemplate(summary_path, pagesize=letter)
            story = []
            
            # Title
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=self.styles['Heading1'],
                fontSize=18,
                spaceAfter=30,
                textColor='darkblue'
            )
            title = Paragraph(f"Summary of {original_filename}", title_style)
            story.append(title)
            story.append(Spacer(1, 12))
            
            # Summary content
            content_style = ParagraphStyle(
                'CustomNormal',
                parent=self.styles['Normal'],
                fontSize=12,
                lineHeight=14,
                spaceAfter=12
            )
            
            # Split summary into paragraphs for better formatting
            paragraphs = summary_text.split('\n\n')
            for paragraph in paragraphs:
                if paragraph.strip():
                    p = Paragraph(paragraph.strip(), content_style)
                    story.append(p)
                    story.append(Spacer(1, 6))
            
            # Build PDF
            doc.build(story)
            logger.info(f"Summary PDF created: {summary_path}")
            
            return summary_path
            
        except Exception as e:
            logger.error(f"Error creating summary PDF: {e}")
            raise Exception(f"Failed to create summary PDF: {e}")