import google.generativeai as genai
import os
from typing import Optional
import logging
import asyncio
from functools import wraps

logger = logging.getLogger(__name__)

def async_retry(max_retries: int = 3, delay: float = 1.0):
    """Decorator for async retry logic"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise e
                    logger.warning(f"Attempt {attempt + 1} failed: {str(e)}. Retrying in {delay} seconds...")
                    await asyncio.sleep(delay * (attempt + 1))
            return None
        return wrapper
    return decorator

class GeminiService:
    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Configuration for the model
        self.generation_config = {
            "temperature": 0.3,
            "top_p": 0.8,
            "top_k": 40,
            "max_output_tokens": 2048,
        }
        
        logger.info("Gemini service initialized successfully")
    
    def _create_summary_prompt(self, text: str) -> str:
        """
        Create a well-structured prompt for PDF summarization
        """
        prompt = f"""
You are an expert document summarizer. Please analyze the following document text and create a comprehensive, well-structured summary.

INSTRUCTIONS:
1. Create a clear, concise summary that captures the main points and key insights
2. Organize the summary with appropriate headings and bullet points where relevant
3. Maintain the logical flow and structure of the original document
4. Include important details, statistics, or quotes if they add value
5. Write in a professional, clear style suitable for business or academic use
6. Aim for a summary that is about 20-30% of the original length
7. If the document has multiple sections, reflect that structure in your summary

DOCUMENT TEXT:
{text}

SUMMARY:
"""
        return prompt
    
    @async_retry(max_retries=3, delay=1.0)
    async def generate_summary(self, text: str) -> str:
        """
        Generate a summary of the provided text using Gemini AI
        """
        try:
            # Check text length and truncate if necessary
            max_input_tokens = 30000  # Conservative limit for Gemini
            if len(text) > max_input_tokens:
                logger.warning(f"Text too long ({len(text)} chars), truncating to {max_input_tokens} chars")
                text = text[:max_input_tokens] + "..."
            
            # Create the prompt
            prompt = self._create_summary_prompt(text)
            
            logger.info("Sending request to Gemini API...")
            
            # Generate content using the model
            response = await asyncio.to_thread(
                self.model.generate_content,
                prompt,
                generation_config=self.generation_config
            )
            
            if not response or not response.text:
                raise Exception("Empty response from Gemini API")
            
            summary = response.text.strip()
            
            logger.info(f"Summary generated successfully. Length: {len(summary)} characters")
            return summary
        
        except Exception as e:
            logger.error(f"Error generating summary with Gemini: {str(e)}")
            raise Exception(f"Failed to generate summary: {str(e)}")
    
    async def generate_custom_summary(self, text: str, custom_instructions: str) -> str:
        """
        Generate a summary with custom instructions
        """
        try:
            prompt = f"""
You are an expert document summarizer. Please analyze the following document text and create a summary based on these specific instructions:

CUSTOM INSTRUCTIONS:
{custom_instructions}

DOCUMENT TEXT:
{text}

SUMMARY:
"""
            
            response = await asyncio.to_thread(
                self.model.generate_content,
                prompt,
                generation_config=self.generation_config
            )
            
            if not response or not response.text:
                raise Exception("Empty response from Gemini API")
            
            return response.text.strip()
        
        except Exception as e:
            logger.error(f"Error generating custom summary: {str(e)}")
            raise Exception(f"Failed to generate custom summary: {str(e)}")
    
    def test_connection(self) -> bool:
        """
        Test the connection to Gemini API
        """
        try:
            test_prompt = "Hello, please respond with 'Connection successful'"
            response = self.model.generate_content(test_prompt)
            
            if response and response.text:
                logger.info("Gemini API connection test successful")
                return True
            else:
                logger.error("Gemini API connection test failed - no response")
                return False
        
        except Exception as e:
            logger.error(f"Gemini API connection test failed: {str(e)}")
            return False