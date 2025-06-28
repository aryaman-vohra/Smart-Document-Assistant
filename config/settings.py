import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # API Configuration
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    
    # Model Configuration
    GEMINI_MODEL = "gemini-1.5-flash"  # Free tier model
    
    # Generation Parameters
    MAX_TOKENS = 1000
    TEMPERATURE = 0.3
    
    # File Configuration
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS = ['.pdf', '.txt']
    SUPPORTED_FORMATS = ['.pdf', '.txt']  # Added for validators.py
    UPLOAD_FOLDER = 'uploads'
    
    # Processing Configuration
    CHUNK_SIZE = 1500
    CHUNK_OVERLAP = 150
    MAX_KEY_SENTENCES = 8
    
    # UI Configuration
    PAGE_TITLE = "Smart Document Assistant"
    PAGE_ICON = "📚"
    
    # Validation
    def validate(self):
        """Validate required settings"""
        if not self.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is required. Please set it in your .env file")
        return True

# Create settings instance
settings = Settings()