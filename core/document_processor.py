import os
import PyPDF2
from typing import Optional, Tuple
from utils.text_utils import clean_text
from utils.validators import validate_file

class DocumentProcessor:
    def __init__(self):
        self.supported_formats = ['.pdf', '.txt']
    
    def process_file(self, uploaded_file) -> Tuple[bool, str, Optional[str]]:
        """Process uploaded file and extract text content."""
        # Validate file
        is_valid, error_msg = validate_file(uploaded_file)
        if not is_valid:
            return False, "", error_msg
        
        try:
            file_extension = os.path.splitext(uploaded_file.name)[1].lower()
            
            if file_extension == '.pdf':
                text = self._extract_pdf_text(uploaded_file)
            elif file_extension == '.txt':
                text = self._extract_txt_text(uploaded_file)
            else:
                return False, "", f"Unsupported file format: {file_extension}"
            
            if not text.strip():
                return False, "", "No readable text found in the document"
            
            cleaned_text = clean_text(text)
            return True, cleaned_text, None
            
        except Exception as e:
            return False, "", f"Error processing file: {str(e)}"
    
    def _extract_pdf_text(self, file) -> str:
        """Extract text from PDF file."""
        text = ""
        pdf_reader = PyPDF2.PdfReader(file)
        
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        
        return text
    
    def _extract_txt_text(self, file) -> str:
        """Extract text from TXT file."""
        try:
            # Try UTF-8 first, then fallback to other encodings
            content = file.read()
            if isinstance(content, bytes):
                try:
                    return content.decode('utf-8')
                except UnicodeDecodeError:
                    return content.decode('latin-1')
            return content
        except Exception as e:
            raise Exception(f"Error reading text file: {str(e)}")