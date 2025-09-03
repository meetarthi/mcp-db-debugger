import os
from dotenv import load_dotenv

# Load .env file from project root, override system environment variables
load_dotenv(override=True)

class Config:
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///test.db')
    
    # Query limits for safety
    MAX_QUERY_RESULTS = 1000
    QUERY_TIMEOUT = 30
    
    # Streamlit config
    PAGE_TITLE = "🔧 Database Error Debugger"
    PAGE_ICON = "🔧"