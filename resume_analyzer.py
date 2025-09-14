"""Main document analyzer class that orchestrates PDF parsing and LLM analysis."""

from typing import Dict, List, Optional
import logging
import time
from pdf_parser import PDFParser
from llm_client import LLMClient
from config import settings

logger = logging.getLogger(__name__)


class DocumentAnalyzer:
    """Main class for analyzing any type of document."""
    
    def __init__(self):
        self.pdf_parser = PDFParser(max_pages=settings.max_pdf_pages)
        self.llm_client = LLMClient()
        self.current_document_data = None
        self.current_document_text = None
        self.current_document_type = "generic"
    
    def analyze_document(self, pdf_path: str, document_type: str = "generic") -> Dict[str, any]:
        """
        Analyze any PDF document.
        
        Args:
            pdf_path: Path to the PDF file
            document_type: Type of document (contract, resume, report, etc.)
            
        Returns:
            Dictionary with analysis results and comprehensive timing information
        """
        overall_start_time = time.time()
        
        try:
            logger.info(f"Starting analysis of {document_type} document: {pdf_path}")
            
            # Extract text from PDF
            pdf_extraction_start = time.time()
            pdf_data = self.pdf_parser.extract_text(pdf_path)
            pdf_extraction_end = time.time()
            
            self.current_document_text = pdf_data['full_text']
            self.current_document_type = document_type
            
            logger.info(f"Extracted text from {pdf_data['page_count']} pages")
            
            # Check if LLM model is available
            model_check_start = time.time()
            if not self.llm_client.check_model_availability():
                model_check_end = time.time()
                return {
                    'success': False,
                    'error': f"LLM model '{settings.ollama_model}' not available. Please install it with: ollama pull {settings.ollama_model}",
                    'pdf_data': pdf_data,
                    'timing': {
                        'total_analysis_time': model_check_end - overall_start_time,
                        'pdf_extraction_time': pdf_extraction_end - pdf_extraction_start,
                        'model_check_time': model_check_end - model_check_start,
                        'llm_extraction_time': 0
                    }
                }
            model_check_end = time.time()
            
            # Extract structured data using LLM
            llm_extraction_start = time.time()
            llm_result = self.llm_client.extract_document_data(self.current_document_text, document_type)
            llm_extraction_end = time.time()
            
            if llm_result['success']:
                self.current_document_data = llm_result['data']
                logger.info(f"Successfully extracted structured data from {document_type} document")
            else:
                logger.warning(f"LLM extraction failed: {llm_result['error']}")
            
            overall_end_time = time.time()
            
            # Combine all timing information
            combined_timing = {
                'total_analysis_time': overall_end_time - overall_start_time,
                'pdf_extraction_time': pdf_extraction_end - pdf_extraction_start,
                'model_check_time': model_check_end - model_check_start,
                'llm_extraction_time': llm_extraction_end - llm_extraction_start,
                'pdf_timing': pdf_data.get('timing', {}),
                'llm_timing': llm_result.get('timing', {})
            }
            
            return {
                'success': True,
                'pdf_data': pdf_data,
                'llm_data': llm_result,
                'structured_data': self.current_document_data,
                'document_type': document_type,
                'timing': combined_timing
            }
            
        except Exception as e:
            error_time = time.time()
            logger.error(f"Error analyzing document: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'pdf_data': None,
                'llm_data': None,
                'document_type': document_type,
                'timing': {
                    'total_analysis_time': error_time - overall_start_time,
                    'pdf_extraction_time': 0,
                    'model_check_time': 0,
                    'llm_extraction_time': 0,
                    'pdf_timing': {},
                    'llm_timing': {}
                }
            }
    
    def ask_question(self, question: str) -> Dict[str, any]:
        """
        Ask a question about the currently loaded document.
        
        Args:
            question: Question to ask about the document
            
        Returns:
            Dictionary with answer and metadata including timing information
        """
        question_start_time = time.time()
        
        if not self.current_document_text:
            return {
                'success': False,
                'error': 'No document loaded. Please analyze a document first.',
                'answer': None,
                'timing': {
                    'total_question_time': 0,
                    'llm_timing': {}
                }
            }
        
        try:
            logger.info(f"Answering question: {question}")
            
            # Use structured data if available, otherwise use raw text
            data_source = self.current_document_data if self.current_document_data else self.current_document_text
            
            result = self.llm_client.answer_question(question, data_source, self.current_document_type)
            
            question_end_time = time.time()
            
            # Add overall question timing to the result
            if 'timing' not in result:
                result['timing'] = {}
            
            result['timing']['total_question_time'] = question_end_time - question_start_time
            
            if result['success']:
                logger.info("Successfully answered question")
            else:
                logger.warning(f"Failed to answer question: {result['error']}")
            
            return result
            
        except Exception as e:
            error_time = time.time()
            logger.error(f"Error answering question: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'answer': None,
                'timing': {
                    'total_question_time': error_time - question_start_time,
                    'llm_timing': {}
                }
            }
    
    def get_document_summary(self) -> Dict[str, any]:
        """
        Get a summary of the currently loaded document.
        
        Returns:
            Dictionary with document summary
        """
        if not self.current_document_text:
            return {
                'success': False,
                'error': 'No document loaded. Please analyze a document first.',
                'summary': None
            }
        
        # Create document-type specific summary prompts
        summary_prompts = {
            "contract": "Provide a brief summary of this contract including the parties involved, contract type, key terms, and important dates.",
            "resume": "Provide a brief summary of this resume including the person's name, current role, key skills, and experience.",
            "generic": "Provide a brief summary of this document including its main purpose, key entities mentioned, and important information."
        }
        
        prompt = summary_prompts.get(self.current_document_type, summary_prompts["generic"])
        return self.ask_question(prompt)
    
    def is_document_loaded(self) -> bool:
        """
        Check if a document is currently loaded.
        
        Returns:
            True if document is loaded, False otherwise
        """
        return self.current_document_text is not None
    
    def get_document_type(self) -> str:
        """
        Get the current document type.
        
        Returns:
            Current document type
        """
        return self.current_document_type
