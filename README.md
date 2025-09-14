# Local PDF Document Analyzer

A privacy-focused PDF document analyzer that uses local LLM models for analyzing any type of document (contracts, resumes, reports, etc.) and answering questions at runtime.

## Features

- **Multi-Document Support**: Analyze contracts, resumes, reports, and any PDF document
- **Document-Type Aware**: Optimized extraction patterns for different document types
- **Runtime Q&A**: Ask natural language questions about any document
- **Complete Privacy**: No external API calls - all processing happens locally
- **Local LLM**: Uses Ollama with Llama 2/3 models
- **Rich Interface**: Beautiful terminal output with context-aware help

## Supported Document Types

- **Contracts**: Employment, service, lease, and other legal agreements
- **Resumes**: Professional profiles and CVs
- **Reports**: Business, technical, and analytical documents
- **Generic**: Any other PDF document type

## Setup

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Install Ollama:
```bash
# macOS
brew install ollama

# Or download from https://ollama.ai
```

3. Pull a Llama model:
```bash
ollama pull llama2:7b
```

## Usage

### Basic Analysis
```bash
# Analyze any document
python main.py --pdf document.pdf --type contract

# Ask specific questions
python main.py --pdf contract.pdf --type contract --question "Who are the parties involved?"

# Interactive mode
python main.py --pdf document.pdf --type resume --interactive
```

### Document Types
- `--type contract` - For contracts and legal agreements
- `--type resume` - For resumes and CVs
- `--type report` - For business/technical reports
- `--type generic` - For any other document (default)

## Architecture

- **PDF Processing**: PyPDF2 for reliable text extraction
- **LLM Integration**: Ollama with Llama 2/3 models
- **Document Analysis**: Type-aware extraction patterns
- **Q&A System**: Context-aware natural language question answering
- **Privacy**: All processing happens locally
