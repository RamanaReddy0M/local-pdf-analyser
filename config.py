"""Configuration settings for the PDF analyzer."""

import os
from typing import Optional


class Settings:
    """Application settings."""
    
    def __init__(self):
        # Ollama Configuration
        self.ollama_host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        self.ollama_model = os.getenv("OLLAMA_MODEL", "llama2:7b")
        
        # Application Settings
        self.debug = os.getenv("DEBUG", "False").lower() == "true"
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        
        # PDF Processing
        self.max_pdf_pages = int(os.getenv("MAX_PDF_PAGES", "10"))
        self.chunk_size = int(os.getenv("CHUNK_SIZE", "2000"))


# Global settings instance
settings = Settings()
