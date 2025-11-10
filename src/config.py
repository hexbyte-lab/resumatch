import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration"""
    
    # Flask settings
    DEBUG = os.getenv('DEBUG', 'True') == 'True'
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5000))
    
    # Matching algorithm settings
    MIN_MATCH_SCORE = 0.0
    MAX_MATCH_SCORE = 100.0
    
    # Keywords settings
    MIN_KEYWORD_LENGTH = 3
    MAX_KEYWORDS_TO_EXTRACT = 20