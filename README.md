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
   # Using sample files from the repository
   python3 main.py --pdf pdf-samples/SampleContract-Shuttle.pdf --type contract --question "Who are the parties involved?"
   python3 main.py --pdf pdf-samples/resume.pdf --type resume --question "What is this person's name?"
   ```

## Usage Examples

### Repository Setup
```bash
# Clone the repository
git clone https://github.com/RamanaReddy0M/local-pdf-analyser.git
cd local-pdf-analyser

# Install dependencies
pip install -r requirements.txt

# Install and start Ollama
brew install ollama
brew services start ollama
ollama pull llama2:7b
```

### Document Type Analysis Examples

#### Contract Analysis
```bash
# Basic contract analysis
python3 main.py --pdf pdf-samples/SampleContract-Shuttle.pdf --type contract

# Contract-specific questions
python3 main.py --pdf pdf-samples/SampleContract-Shuttle.pdf --type contract --question "Who are the parties involved?"
python3 main.py --pdf pdf-samples/SampleContract-Shuttle.pdf --type contract --question "What are the payment terms?"
python3 main.py --pdf pdf-samples/SampleContract-Shuttle.pdf --type contract --question "What are the termination conditions?"
python3 main.py --pdf pdf-samples/SampleContract-Shuttle.pdf --type contract --question "What is the contract duration?"

# Interactive contract analysis
python3 main.py --pdf pdf-samples/SampleContract-Shuttle.pdf --type contract --interactive
```

#### Resume Analysis
```bash
# Basic resume analysis
python3 main.py --pdf pdf-samples/resume.pdf --type resume

# Resume-specific questions
python3 main.py --pdf pdf-samples/resume.pdf --type resume --question "What is this person's name?"
python3 main.py --pdf pdf-samples/resume.pdf --type resume --question "What are their technical skills?"
python3 main.py --pdf pdf-samples/resume.pdf --type resume --question "What is their educational background?"
python3 main.py --pdf pdf-samples/resume.pdf --type resume --question "What projects have they worked on?"
python3 main.py --pdf pdf-samples/resume.pdf --type resume --question "What is his btech percentage?"

# Interactive resume analysis
python3 main.py --pdf pdf-samples/resume.pdf --type resume --interactive
```

#### Generic Document Analysis
```bash
# Basic generic analysis
python3 main.py --pdf pdf-samples/resume.pdf --type generic
python3 main.py --pdf pdf-samples/SampleContract-Shuttle.pdf --type generic

# Generic questions
python3 main.py --pdf pdf-samples/resume.pdf --type generic --question "What is this document about?"
python3 main.py --pdf pdf-samples/SampleContract-Shuttle.pdf --type generic --question "Who are the key entities mentioned?"
python3 main.py --pdf pdf-samples/resume.pdf --type generic --question "What are the important dates?"
python3 main.py --pdf pdf-samples/SampleContract-Shuttle.pdf --type generic --question "What financial information is mentioned?"

# Interactive generic analysis
python3 main.py --pdf pdf-samples/resume.pdf --type generic --interactive
```

#### Report Analysis
```bash
# Basic report analysis
python3 main.py --pdf report.pdf --type report

# Report-specific questions
python3 main.py --pdf report.pdf --type report --question "What are the key findings?"
python3 main.py --pdf report.pdf --type report --question "What are the main recommendations?"
python3 main.py --pdf report.pdf --type report --question "Who are the stakeholders mentioned?"

# Interactive report analysis
python3 main.py --pdf report.pdf --type report --interactive
```

### Advanced Usage Examples

#### Working with Your Own PDFs
```bash
# Place your PDFs in the project directory or specify full paths
python3 main.py --pdf /path/to/your/contract.pdf --type contract --question "What are the key terms?"
python3 main.py --pdf ./my-resume.pdf --type resume --question "What are their skills?"
python3 main.py --pdf ../documents/report.pdf --type report --interactive
```

#### Batch Analysis Examples
```bash
# Analyze multiple documents sequentially
python3 main.py --pdf pdf-samples/resume.pdf --type resume --question "What is their educational background?"
python3 main.py --pdf pdf-samples/SampleContract-Shuttle.pdf --type contract --question "What are the payment terms?"
python3 main.py --pdf pdf-samples/resume.pdf --type generic --question "What is this document about?"
```

#### Interactive Mode Examples
```bash
# Start interactive mode with different document types
python3 main.py --pdf pdf-samples/resume.pdf --type resume --interactive
# Then ask: "What is his name?", "What are his skills?", "What projects has he done?"

python3 main.py --pdf pdf-samples/SampleContract-Shuttle.pdf --type contract --interactive
# Then ask: "Who are the parties?", "What are the terms?", "When does it expire?"
```

#### Testing Different Document Types
```bash
# Test the same document with different types to see extraction differences
python3 main.py --pdf pdf-samples/resume.pdf --type resume --question "What is this person's name?"
python3 main.py --pdf pdf-samples/resume.pdf --type generic --question "What is this person's name?"
python3 main.py --pdf pdf-samples/SampleContract-Shuttle.pdf --type contract --question "Who are the parties?"
python3 main.py --pdf pdf-samples/SampleContract-Shuttle.pdf --type generic --question "Who are the parties?"
```

### Sample Questions by Document Type
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

### Repository-Specific Issues

#### Sample Files Not Found
```bash
# If you get "PDF file not found" errors, check the sample files exist:
ls -la pdf-samples/
# Should show: resume.pdf, SampleContract-Shuttle.pdf

# If missing, you can download them or use your own PDFs:
python3 main.py --pdf /path/to/your/document.pdf --type contract --question "What are the key terms?"
```

#### Virtual Environment Issues
```bash
# If you get import errors, make sure you're in the virtual environment:
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate     # On Windows

# Verify installation:
pip list | grep -E "(PyPDF2|ollama|rich|click)"
```

#### Ollama Connection Issues
```bash
# Check if Ollama is running:
curl http://localhost:11434/api/tags

# If not running:
brew services start ollama  # On macOS
# or
ollama serve               # Start manually

# Check available models:
ollama list
# Should show: llama2:7b
```

### Getting Help

- **Repository**: [https://github.com/RamanaReddy0M/local-pdf-analyser](https://github.com/RamanaReddy0M/local-pdf-analyser)
- **Issues**: Create an issue on GitHub for bugs or feature requests
- **Documentation**: Check README.md for project overview
- **Examples**: Use the sample PDFs in `pdf-samples/` directory for testing