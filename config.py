import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for the chat-to-excel application"""
    
    # API Keys
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    
    # Application Settings
    MAX_FILE_SIZE_MB = 50
    ALLOWED_EXTENSIONS = ['.xlsx', '.xls']
    DATA_DIR = "data"
    PROMPTS_DIR = "prompts"
    
    # LLM Settings
    DEFAULT_MODEL = "openai/gpt-oss-20b"  # Fast Groq model
    MAX_TOKENS = 15000
    TEMPERATURE = 0.2
    
    # UI Settings
    PAGE_TITLE = "Chat to Excel"
    PAGE_ICON = "📊"
    LAYOUT = "wide"
    
    @classmethod
    def validate_config(cls):
        """Validate that all required configurations are set"""
        if not cls.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY environment variable is not set")
        
        # Create directories if they don't exist
        os.makedirs(cls.DATA_DIR, exist_ok=True)
        os.makedirs(cls.PROMPTS_DIR, exist_ok=True) 