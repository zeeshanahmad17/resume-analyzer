import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Keys
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    
    # MongoDB Configuration
    MONGODB_URI = os.getenv('MONGODB_URI')
    
    # Rate Limits
    GEMINI_RPM = 15
    GEMINI_TPM = 1_000_000
    EMBEDDING_RPO = 1500 # Requests per day

    # Application Settings
    MAX_FILE_SIZE = 1024 * 1024 * 10 # 10MB
    ALLOWED_EXTENSIONS = {'pdf', 'txt', 'doc', 'docx'}

    @staticmethod
    def validate():
        """Validate the required configs are set."""
        if not Config.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is not set")
        if not Config.MONGODB_URI:
            raise ValueError("MONGODB_URI is not set")