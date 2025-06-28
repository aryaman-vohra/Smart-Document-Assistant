import os
from typing import Optional
from config.settings import settings

def validate_file(file) -> tuple[bool, Optional[str]]:
    """Validate uploaded file format and size."""
    if file is None:
        return False, "No file uploaded"
    
    file_extension = os.path.splitext(file.name)[1].lower()
    if file_extension not in settings.SUPPORTED_FORMATS:
        return False, f"Unsupported format. Please upload {', '.join(settings.SUPPORTED_FORMATS)} files"
    
    if file.size > settings.MAX_FILE_SIZE:
        return False, f"File too large. Maximum size: {settings.MAX_FILE_SIZE // (1024*1024)}MB"
    
    return True, None

def validate_question(question: str) -> tuple[bool, Optional[str]]:
    """Validate user question input."""
    if not question or not question.strip():
        return False, "Please enter a question"
    
    if len(question.strip()) < 5:
        return False, "Question too short. Please be more specific"
    
    if len(question) > 500:
        return False, "Question too long. Please keep it under 500 characters"
    
    return True, None

def validate_text_content(text: str) -> tuple[bool, Optional[str]]:
    """Validate extracted text content."""
    if not text or not text.strip():
        return False, "No readable content found in the document"
    
    if len(text.strip()) < 50:
        return False, "Document content too short for meaningful analysis"
    
    return True, None

def validate_api_key(api_key: str) -> tuple[bool, Optional[str]]:
    """Validate API key format."""
    if not api_key or not api_key.strip():
        return False, "API key is required"
    
    if len(api_key.strip()) < 10:
        return False, "API key appears to be invalid (too short)"
    
    return True, None