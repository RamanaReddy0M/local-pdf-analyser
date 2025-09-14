"""PDF parsing and text extraction module."""

import PyPDF2
from typing import List, Dict, Optional
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class PDFParser:
    """Handles PDF text extraction and processing."""
    
    def __init__(self, max_pages: int = 10):
        self.max_pages = max_pages
    
    def extract_text(self, pdf_path: str) -> Dict[str, any]:
        """
        Extract text from PDF file.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Dictionary containing extracted text and metadata
        """
        try:
            pdf_path = Path(pdf_path)
            if not pdf_path.exists():
                raise FileNotFoundError(f"PDF file not found: {pdf_path}")
            
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                # Extract metadata
                metadata = pdf_reader.metadata or {}
                
                # Extract text from pages
                text_content = []
                page_count = min(len(pdf_reader.pages), self.max_pages)
                
                for page_num in range(page_count):
                    page = pdf_reader.pages[page_num]
                    text = page.extract_text()
                    if text.strip():  # Only add non-empty pages
                        text_content.append({
                            'page': page_num + 1,
                            'text': text.strip()
                        })
                
                # Combine all text
                full_text = "\n\n".join([page['text'] for page in text_content])
                
                return {
                    'full_text': full_text,
                    'pages': text_content,
                    'metadata': metadata,
                    'page_count': page_count,
                    'file_name': pdf_path.name,
                    'file_size': pdf_path.stat().st_size
                }
            
        except Exception as e:
            logger.error(f"Error extracting text from PDF {pdf_path}: {str(e)}")
            raise
    
    def chunk_text(self, text: str, chunk_size: int = 2000) -> List[str]:
        """
        Split text into chunks for processing.
        
        Args:
            text: Input text to chunk
            chunk_size: Maximum size of each chunk
            
        Returns:
            List of text chunks
        """
        if len(text) <= chunk_size:
            return [text]
        
        chunks = []
        words = text.split()
        current_chunk = []
        current_size = 0
        
        for word in words:
            word_size = len(word) + 1  # +1 for space
            
            if current_size + word_size > chunk_size and current_chunk:
                chunks.append(" ".join(current_chunk))
                current_chunk = [word]
                current_size = word_size
            else:
                current_chunk.append(word)
                current_size += word_size
        
        if current_chunk:
            chunks.append(" ".join(current_chunk))
        
        return chunks
