# PDF Summarizer AI

A comprehensive AI-powered PDF summarization application built with FastAPI and Streamlit, utilizing Google Gemini AI for intelligent document analysis.

## 🚀 Features

- **AI-Powered Summarization**: Uses Google Gemini Flash 2.0 for intelligent document analysis
- **PDF Processing**: Extract text from PDF documents with advanced parsing
- **REST API**: Robust FastAPI backend with comprehensive error handling
- **User-Friendly Interface**: Clean Streamlit web interface for easy interaction
- **PDF Generation**: Create downloadable PDF summaries
- **Async Processing**: Efficient async operations for better performance
- **Comprehensive Logging**: Detailed logging for debugging and monitoring

## 📋 Prerequisites

- Python 3.8 or higher
- uv package manager (recommended) or pip
- Google Gemini API key

## 🛠️ Installation

### 1. Setup Main Project

```bash
# Create and navigate to project directory
mkdir pdf-summarizer
cd pdf-summarizer

# Initialize with uv
uv init --name pdf-summarizer

# Add dependencies
uv add fastapi uvicorn python-multipart google-generativeai PyPDF2 reportlab python-dotenv pydantic

# Add development dependencies
uv add --dev pytest httpx black flake8
```

### 2. Setup Client Project

```bash
# Create client directory
mkdir client
cd client

# Initialize client project
uv init --name pdf-summarizer-client

# Add client dependencies
uv add streamlit requests python-dotenv

# Return to main directory
cd ..
```

### 3. Environment Configuration

Create `.env` file in the main project root:

```env
GEMINI_API_KEY=your_gemini_api_key_here
ENVIRONMENT=development
LOG_LEVEL=INFO
```

Create `client/.env` file:

```env
API_BASE_URL=http://localhost:8000
ENVIRONMENT=development
```

## 🏗️ Project Structure

```
pdf-summarizer/
├── .env                          # Environment variables
├── pyproject.toml               # Main project configuration
├── README.md
├── src/
│   ├── __init__.py
│   ├── main.py                  # FastAPI application
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py           # Pydantic models
│   └── services/
│       ├── __init__.py
│       ├── pdf_processor.py     # PDF processing service
│       └── gemini_service.py    # Gemini AI service
├── tests/
│   └── test_main.py            # API tests
└── client/
    ├── .env                    # Client environment variables
    ├── pyproject.toml         # Client project configuration
    └── app.py                 # Streamlit interface
```

## 🚀 Running the Application

### Start the FastAPI Server

```bash
# From the main project directory
uv run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Start the Streamlit Client

```bash
# Navigate to client directory
cd client

# Run Streamlit app
uv run streamlit run app.py
```

## 📚 API Documentation

### Endpoints

- **GET `/`**: API information and available endpoints
- **GET `/health`**: Health check endpoint
- **POST `/summarize`**: Upload PDF and generate summary
- **GET `/download/{filename}`**: Download generated summary PDF

### API Usage Example

```python
import requests

# Upload and summarize PDF
with open('document.pdf', 'rb') as file:
    response = requests.post(
        'http://localhost:8000/summarize',
        files={'file': file}
    )
    
if response.status_code == 200:
    result = response.json()
    print(f"Summary: {result['summary_text']}")
```

## 🌐 Web Interface

Access the Streamlit interface at `http://localhost:8501`

Features:
- Drag-and-drop PDF upload
- Real-time processing status
- Summary display with formatting options
- Download capabilities
- API health monitoring

## 🧪 Testing

Run tests using pytest:

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src

# Run specific test file
uv run pytest tests/test_main.py
```

## 🔧 Configuration

### Gemini AI Configuration

The application uses Google Gemini Flash 2.0 with the following configuration:
- Temperature: 0.3 (for consistent outputs)
- Top-p: 0.8
- Top-k: 40
- Max output tokens: 2048

### File Limits

- Maximum file size: 10MB
- Supported format: PDF only
- Maximum input tokens: 30,000 characters

## 📝 Customization

### Custom Summary Instructions

You can extend the `GeminiService` to support custom summarization instructions:

```python
summary = await gemini_service.generate_custom_summary(
    text, 
    "Create a technical summary focusing on methodology and results"
)
```

### PDF Styling

Customize PDF output by modifying the styles in `PDFProcessor`:

```python
self.custom_style = ParagraphStyle(
    'Custom',
    fontSize=12,
    textColor='blue'
)
```

## 🔍 Monitoring and Logging

The application includes comprehensive logging:

- Request/response logging
- Error tracking
- Performance monitoring
- API health checks

Logs are configured in the main application and can be customized via environment variables.

## 🚨 Error Handling

The application includes robust error handling for:

- Invalid file formats
- File size limitations
- API failures
- Network timeouts
- Processing errors

## 🔒 Security Considerations

- API key stored in environment variables
- File size validation
- Input sanitization
- CORS configuration
- Temporary file cleanup

## 📈 Performance Optimization

- Async request processing
- Retry mechanisms for API calls
- Memory-efficient file handling
- Connection pooling
- Progress tracking for long operations

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new features
5. Run the test suite
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions:
- Check the API documentation at `http://localhost:8000/docs`
- Review the logs for error details
- Ensure your Gemini API key is valid and has sufficient quota

## 🔮 Future Enhancements

- Support for multiple document formats (DOCX, TXT)
- Batch processing capabilities
- Summary customization options
- Integration with cloud storage
- Multi-language support
- Advanced analytics and reporting