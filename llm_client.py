"""Local LLM client using Ollama."""

import ollama
from typing import List, Dict, Optional
import logging
import time
from config import settings

logger = logging.getLogger(__name__)


class LLMClient:
    """Client for interacting with local LLM via Ollama."""
    
    def __init__(self, model: str = None, host: str = None):
        self.model = model or settings.ollama_model
        self.host = host or settings.ollama_host
        self.client = ollama.Client(host=self.host)
    
    def extract_document_data(self, text: str, document_type: str = "generic") -> Dict[str, any]:
        """
        Extract structured data from any document text.
        
        Args:
            text: Document text content
            document_type: Type of document (contract, resume, report, etc.)
            
        Returns:
            Dictionary with extracted document data and timing information
        """
        start_time = time.time()
        
        # Define extraction patterns based on document type
        extraction_patterns = {
            "contract": """
            Analyze the following contract document and extract key information. 
            Return a structured response with the following fields:
            
            - parties: Names/entities of all parties involved
            - contract_type: Type of contract (employment, service, lease, etc.)
            - effective_date: When the contract becomes effective
            - expiration_date: When the contract expires (if applicable)
            - key_terms: Important terms and conditions
            - payment_terms: Payment structure and amounts
            - obligations: Key obligations of each party
            - termination_conditions: How the contract can be terminated
            - governing_law: Applicable law/jurisdiction
            - summary: Brief overview of the contract
            
            Document text:
            {text_placeholder}
            
            Please provide a structured response focusing on the most important contract elements.
            """,
            
            "resume": """
            Analyze the following resume text and extract key information. 
            Return a structured response with the following fields:
            
            - name: Full name of the person
            - email: Email address if found
            - phone: Phone number if found
            - location: Current location/address
            - skills: List of technical and professional skills
            - experience: List of work experience with company, position, duration
            - education: Educational background
            - summary: Brief professional summary
            
            Document text:
            {text_placeholder}
            
            Please provide a structured response focusing on the most important information.
            """,
            
            "generic": """
            Analyze the following document and extract key information. 
            Return a structured response with the following fields:
            
            - document_type: What type of document this appears to be
            - key_entities: Important people, organizations, or entities mentioned
            - dates: Important dates mentioned
            - key_terms: Important terms, conditions, or concepts
            - financial_info: Any monetary amounts, costs, or financial terms
            - obligations: Any responsibilities or requirements mentioned
            - summary: Brief overview of the document content
            
            Document text:
            {text_placeholder}
            
            Please provide a structured response focusing on the most important information.
            """
        }
        
        prompt_prep_start = time.time()
        
        # Get appropriate prompt based on document type
        prompt_template = extraction_patterns.get(document_type.lower(), extraction_patterns["generic"])
        
        # Format the prompt with the actual text content
        if document_type.lower() == "contract":
            prompt = prompt_template.replace("{text_placeholder}", text[:4000])
        elif document_type.lower() == "resume":
            prompt = prompt_template.replace("{text_placeholder}", text[:3000])
        else:  # generic
            prompt = prompt_template.replace("{text_placeholder}", text[:3500])
        
        prompt_prep_end = time.time()
        
        # Define system messages based on document type
        system_messages = {
            "contract": "You are an expert contract analyst. Extract key contract information and return structured data.",
            "resume": "You are an expert resume parser. Extract key information and return structured data.",
            "generic": "You are an expert document analyst. Extract key information from any document type and return structured data."
        }
        
        system_message = system_messages.get(document_type.lower(), system_messages["generic"])
        
        llm_request_start = time.time()
        
        try:
            response = self.client.chat(
                model=self.model,
                messages=[
                    {
                        'role': 'system',
                        'content': system_message
                    },
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ]
            )
            
            llm_request_end = time.time()
            total_time = llm_request_end - start_time
            
            return {
                'success': True,
                'data': response['message']['content'],
                'model': self.model,
                'document_type': document_type,
                'timing': {
                    'total_extraction_time': total_time,
                    'prompt_preparation_time': prompt_prep_end - prompt_prep_start,
                    'llm_request_time': llm_request_end - llm_request_start,
                    'text_length': len(text),
                    'prompt_length': len(prompt),
                    'response_length': len(response['message']['content']),
                    'tokens_per_second': len(response['message']['content']) / (llm_request_end - llm_request_start) if (llm_request_end - llm_request_start) > 0 else 0
                }
            }
            
        except Exception as e:
            error_time = time.time()
            total_time = error_time - start_time
            
            logger.error(f"Error extracting document data: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'data': None,
                'document_type': document_type,
                'timing': {
                    'total_extraction_time': total_time,
                    'prompt_preparation_time': prompt_prep_end - prompt_prep_start,
                    'llm_request_time': 0,
                    'text_length': len(text),
                    'prompt_length': len(prompt),
                    'response_length': 0,
                    'tokens_per_second': 0
                }
            }
    
    def answer_question(self, question: str, document_data: str, document_type: str = "generic") -> Dict[str, any]:
        """
        Answer a question about any document.
        
        Args:
            question: User's question
            document_data: Document text or extracted data
            document_type: Type of document (contract, resume, etc.)
            
        Returns:
            Dictionary with answer and metadata including timing information
        """
        start_time = time.time()
        
        # Define context-aware prompts based on document type
        context_prompts = {
            "contract": f"""
            Based on the following contract information, answer this question: "{question}"
            
            Contract information:
            {document_data[:4000]}  # Limit context size
            
            Provide a clear, concise answer based on the information available in the contract.
            If the information is not available, say "Information not found in the contract."
            """,
            
            "resume": f"""
            Based on the following resume information, answer this question: "{question}"
            
            Resume information:
            {document_data[:4000]}  # Limit context size
            
            IMPORTANT: Look carefully at the structured data above. If the information is present in any form, provide the answer. 
            
            For percentage/grade questions:
            - Look for any numerical values like "75%", "90%", "9.8 GPA", etc.
            - "BTech" typically refers to "Bachelor of Technology" or "Bachelor of Computer Science and Engineering"
            - "B.Tech", "BE", "Bachelor of Engineering", "Bachelor of Computer Science" are all equivalent to BTech
            
            For degree questions:
            - "Bachelor of Computer Science and Engineering" = BTech/BE
            - "Bachelor of Technology" = BTech
            - "Bachelor of Engineering" = BE
            
            Provide a clear, concise answer based on the information available in the resume.
            If the information is truly not available, say "Information not found in the resume."
            """,
            
            "generic": f"""
            Based on the following document information, answer this question: "{question}"
            
            Document information:
            {document_data[:4000]}  # Limit context size
            
            Provide a clear, concise answer based on the information available in the document.
            If the information is not available, say "Information not found in the document."
            """
        }
        
        prompt_prep_start = time.time()
        
        prompt = context_prompts.get(document_type.lower(), context_prompts["generic"])
        
        prompt_prep_end = time.time()
        
        # Define system messages based on document type
        system_messages = {
            "contract": "You are a helpful assistant that answers questions about contracts based on the provided information.",
            "resume": "You are a helpful assistant that answers questions about resumes based on the provided information.",
            "generic": "You are a helpful assistant that answers questions about documents based on the provided information."
        }
        
        system_message = system_messages.get(document_type.lower(), system_messages["generic"])
        
        llm_request_start = time.time()
        
        try:
            response = self.client.chat(
                model=self.model,
                messages=[
                    {
                        'role': 'system',
                        'content': system_message
                    },
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ]
            )
            
            llm_request_end = time.time()
            total_time = llm_request_end - start_time
            
            return {
                'success': True,
                'answer': response['message']['content'],
                'question': question,
                'model': self.model,
                'document_type': document_type,
                'timing': {
                    'total_answer_time': total_time,
                    'prompt_preparation_time': prompt_prep_end - prompt_prep_start,
                    'llm_request_time': llm_request_end - llm_request_start,
                    'question_length': len(question),
                    'context_length': len(document_data),
                    'prompt_length': len(prompt),
                    'answer_length': len(response['message']['content']),
                    'tokens_per_second': len(response['message']['content']) / (llm_request_end - llm_request_start) if (llm_request_end - llm_request_start) > 0 else 0
                }
            }
            
        except Exception as e:
            error_time = time.time()
            total_time = error_time - start_time
            
            logger.error(f"Error answering question: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'answer': None,
                'document_type': document_type,
                'timing': {
                    'total_answer_time': total_time,
                    'prompt_preparation_time': prompt_prep_end - prompt_prep_start,
                    'llm_request_time': 0,
                    'question_length': len(question),
                    'context_length': len(document_data),
                    'prompt_length': len(prompt),
                    'answer_length': 0,
                    'tokens_per_second': 0
                }
            }
    
    def check_model_availability(self) -> bool:
        """
        Check if the specified model is available.
        
        Returns:
            True if model is available, False otherwise
        """
        try:
            models = self.client.list()
            available_models = [model['name'] for model in models['models']]
            return self.model in available_models
        except Exception as e:
            logger.error(f"Error checking model availability: {str(e)}")
            return False
