from pydantic import BaseModel
from typing import Optional

class SummaryResponse(BaseModel):
    original_filename: str
    summary_text: str
    summary_pdf_path: str
    summary_filename: str
    message: str

class HealthResponse(BaseModel):
    status: str
    service: str

class ErrorResponse(BaseModel):
    detail: str
    error_code: Optional[str] = None