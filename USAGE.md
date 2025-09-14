# PDF Document Analyzer - Usage Guide

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Install and start Ollama:**
   ```bash
   brew install ollama
   brew services start ollama
   ollama pull llama2:7b
   ```

3. **Analyze any document:**
   ```bash
   python3 main.py --pdf document.pdf --type contract --question "Who are the parties involved?"
   ```

## Usage Examples

### Document Type Analysis
```bash
# Contract analysis
python3 main.py --pdf contract.pdf --type contract
python3 main.py --pdf contract.pdf --type contract --question "What are the payment terms?"

# Resume analysis
python3 main.py --pdf resume.pdf --type resume
python3 main.py --pdf resume.pdf --type resume --question "What are their technical skills?"

# Generic document analysis
python3 main.py --pdf report.pdf --type generic
python3 main.py --pdf report.pdf --type generic --question "What is this document about?"

# Interactive mode
python3 main.py --pdf document.pdf --type contract --interactive
```

### Contract Questions
- "Who are the parties involved in this contract?"
- "What type of contract is this?"
- "What are the key terms and conditions?"
- "What are the payment terms?"
- "When does this contract expire?"
- "What are the termination conditions?"
- "What are the obligations of each party?"
- "What is the governing law?"

### Resume Questions
- "What is this person's name?"
- "What programming languages do they know?"
- "What is their educational background?"
- "What projects have they worked on?"
- "What are their key skills?"
- "Where do they live?"
- "What is their work experience?"

### Generic Document Questions
- "What is this document about?"
- "Who are the key people or entities mentioned?"
- "What are the important dates?"
- "What are the key terms or concepts?"
- "What are the main obligations or requirements?"
- "What financial information is mentioned?"

### Interactive Mode Commands
- `help` - Show available commands (context-aware)
- `summary` - Get a document summary
- `quit` or `exit` - Exit the program

## Document Types

### Contract (`--type contract`)
- **Best for**: Legal agreements, service contracts, employment contracts
- **Extracts**: Parties, contract type, key terms, payment terms, obligations, termination conditions
- **Questions**: Contract-specific questions about parties, terms, payments, etc.

### Resume (`--type resume`)
- **Best for**: CVs, professional profiles, job applications
- **Extracts**: Name, contact info, skills, experience, education, projects
- **Questions**: Person-specific questions about background, skills, experience

### Report (`--type report`)
- **Best for**: Business reports, technical documents, analytical reports
- **Extracts**: Key entities, dates, financial info, obligations, summary
- **Questions**: Document-specific questions about content, findings, recommendations

### Generic (`--type generic`)
- **Best for**: Any other PDF document
- **Extracts**: Document type, key entities, dates, terms, financial info, obligations
- **Questions**: General questions about document content and purpose

## Features

✅ **Privacy-Focused**: All processing happens locally  
✅ **No API Calls**: Uses local LLM via Ollama  
✅ **Multi-Document Support**: Contracts, resumes, reports, and more  
✅ **Document-Type Aware**: Optimized extraction for each document type  
✅ **Natural Language**: Ask questions in plain English  
✅ **Structured Extraction**: Automatically extracts relevant data  
✅ **Rich Interface**: Beautiful terminal output with context-aware help  
✅ **Error Handling**: Robust error handling and logging  

## Architecture

- **PDF Processing**: PyPDF2 for reliable text extraction
- **LLM Integration**: Ollama with Llama 2 7B model
- **Document Analysis**: Type-aware extraction patterns
- **CLI Interface**: Click-based command-line interface
- **Rich Output**: Beautiful terminal formatting
- **Configuration**: Environment-based settings

## Troubleshooting

### Ollama Issues
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Restart Ollama service
brew services restart ollama

# Check available models
ollama list
```

### PDF Issues
- Ensure PDF contains extractable text (not scanned images)
- Check file permissions
- Verify PDF is not corrupted
- Large PDFs (>10 pages) may take longer to process

### Performance
- First run may be slower as model loads
- Subsequent questions are faster
- Contract documents may take longer due to complexity
- Consider using smaller models for faster responses