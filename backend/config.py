import os
from dotenv import load_dotenv

# Find the project root (where run.py is)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

load_dotenv(os.path.join(BASE_DIR, '.env'))


class Config:
    # Embedding settings
    EMBEDDING_MODEL = "BAAI/bge-large-en-v1.5"
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 1000))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 275))
    
    # Bulletproof absolute paths
    DATA_DIR = os.path.join(BASE_DIR, "data")
    CHROMA_DIR = os.path.join(BASE_DIR, "backend", "chroma_db")
    
    TOP_K = 5

    # LLM settings
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "groq")
    LLM_MODEL = os.getenv("LLM_MODEL", "llama-3.3-70b-versatile")
    LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", 0.1))

    # API Keys
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")