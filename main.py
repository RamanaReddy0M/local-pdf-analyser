"""Main CLI interface for the PDF Document Analyzer."""

import click
import logging
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt
from rich.table import Table
from rich.columns import Columns

from resume_analyzer import DocumentAnalyzer
from config import settings

# Setup logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

console = Console()


def format_time(seconds: float) -> str:
    """Format time in seconds to human readable format."""
    if seconds < 1:
        return f"{seconds*1000:.1f}ms"
    elif seconds < 60:
        return f"{seconds:.2f}s"
    else:
        minutes = int(seconds // 60)
        secs = seconds % 60
        return f"{minutes}m {secs:.1f}s"


def display_timing_info(timing_data: dict, title: str = "Performance Analysis"):
    """Display comprehensive timing information."""
    if not timing_data:
        return
    
    console.print(f"\n[bold cyan]{title}[/bold cyan]")
    
    # Create timing table
    timing_table = Table(show_header=True, header_style="bold magenta")
    timing_table.add_column("Operation", style="cyan", no_wrap=True)
    timing_table.add_column("Time", justify="right", style="green")
    timing_table.add_column("Details", style="dim")
    
    # Overall timing
    if 'total_analysis_time' in timing_data:
        timing_table.add_row(
            "Total Analysis",
            format_time(timing_data['total_analysis_time']),
            "Complete document processing"
        )
    
    if 'total_question_time' in timing_data:
        timing_table.add_row(
            "Question Answering",
            format_time(timing_data['total_question_time']),
            "LLM response time"
        )
    
    if 'total_answer_time' in timing_data:
        timing_table.add_row(
            "Question Answering",
            format_time(timing_data['total_answer_time']),
            "LLM response time"
        )
    
    # PDF extraction timing
    if 'pdf_extraction_time' in timing_data:
        timing_table.add_row(
            "PDF Extraction",
            format_time(timing_data['pdf_extraction_time']),
            "Text extraction from PDF"
        )
    
    # LLM timing
    if 'llm_extraction_time' in timing_data:
        timing_table.add_row(
            "LLM Data Extraction",
            format_time(timing_data['llm_extraction_time']),
            "Structured data extraction"
        )
    
    if 'model_check_time' in timing_data:
        timing_table.add_row(
            "Model Check",
            format_time(timing_data['model_check_time']),
            "Ollama model availability"
        )
    
    # Detailed PDF timing
    pdf_timing = timing_data.get('pdf_timing', {})
    if pdf_timing:
        timing_table.add_row("", "", "")  # Separator
        timing_table.add_row(
            "  File Open",
            format_time(pdf_timing.get('file_open_time', 0)),
            "PDF file access"
        )
        timing_table.add_row(
            "  Reader Init",
            format_time(pdf_timing.get('reader_init_time', 0)),
            "PyPDF2 initialization"
        )
        timing_table.add_row(
            "  Page Extraction",
            format_time(pdf_timing.get('page_extraction_time', 0)),
            f"Processing {pdf_timing.get('pages_per_second', 0):.1f} pages/sec"
        )
        timing_table.add_row(
            "  Text Processing",
            format_time(pdf_timing.get('text_processing_time', 0)),
            "Text concatenation"
        )
    
    # Detailed LLM timing
    llm_timing = timing_data.get('llm_timing', {})
    if llm_timing:
        timing_table.add_row("", "", "")  # Separator
        
        # Show prompt preparation time
        if 'prompt_preparation_time' in llm_timing:
            timing_table.add_row(
                "  Prompt Prep",
                format_time(llm_timing.get('prompt_preparation_time', 0)),
                "Prompt formatting"
            )
        
        timing_table.add_row(
            "  LLM Request",
            format_time(llm_timing.get('llm_request_time', 0)),
            f"Model: {llm_timing.get('tokens_per_second', 0):.1f} tokens/sec"
        )
        
        # Show text lengths
        if 'text_length' in llm_timing:
            timing_table.add_row(
                "  Input Text",
                f"{llm_timing['text_length']:,} chars",
                "Document text length"
            )
        if 'prompt_length' in llm_timing:
            timing_table.add_row(
                "  Prompt",
                f"{llm_timing['prompt_length']:,} chars",
                "Formatted prompt length"
            )
        if 'response_length' in llm_timing:
            timing_table.add_row(
                "  Response",
                f"{llm_timing['response_length']:,} chars",
                "LLM response length"
            )
        
        # Show question-specific details
        if 'question_length' in llm_timing:
            timing_table.add_row(
                "  Question",
                f"{llm_timing['question_length']:,} chars",
                "Question text length"
            )
        if 'context_length' in llm_timing:
            timing_table.add_row(
                "  Context",
                f"{llm_timing['context_length']:,} chars",
                "Context data length"
            )
        if 'answer_length' in llm_timing:
            timing_table.add_row(
                "  Answer",
                f"{llm_timing['answer_length']:,} chars",
                "Answer text length"
            )
    
    console.print(timing_table)


@click.command()
@click.option('--pdf', '-p', help='Path to PDF document file')
@click.option('--type', '-t', 'document_type', 
              type=click.Choice(['contract', 'resume', 'report', 'generic'], case_sensitive=False),
              default='generic', help='Type of document (contract, resume, report, generic)')
@click.option('--interactive', '-i', is_flag=True, help='Start interactive mode')
@click.option('--question', '-q', help='Ask a specific question about the document')
def main(pdf: str, document_type: str, interactive: bool, question: str):
    """PDF Document Analyzer - Privacy-focused local analysis."""
    
    console.print(Panel.fit(
        "[bold blue]PDF Document Analyzer[/bold blue]\n"
        "[dim]Privacy-focused local analysis using Ollama LLM[/dim]",
        border_style="blue"
    ))
    
    analyzer = DocumentAnalyzer()
    
    # If PDF is provided, analyze it
    if pdf:
        pdf_path = Path(pdf)
        if not pdf_path.exists():
            console.print(f"[red]Error: PDF file not found: {pdf}[/red]")
            return
        
        console.print(f"[yellow]Analyzing {document_type} document: {pdf_path.name}[/yellow]")
        
        result = analyzer.analyze_document(str(pdf_path), document_type)
        
        if result['success']:
            console.print(f"[green]✓ {document_type.title()} document analysis completed successfully![/green]")
            
            # Display basic info
            pdf_data = result['pdf_data']
            console.print(f"[dim]Pages processed: {pdf_data['page_count']}[/dim]")
            console.print(f"[dim]File size: {pdf_data['file_size']:,} bytes[/dim]")
            console.print(f"[dim]Document type: {document_type}[/dim]")
            
            # Display timing information
            if 'timing' in result:
                display_timing_info(result['timing'], "Document Analysis Performance")
            
            # Show structured data if available
            if result.get('structured_data'):
                console.print(f"\n[bold]Extracted Information:[/bold]")
                console.print(Panel(result['structured_data'], title=f"{document_type.title()} Data"))
            
            # Ask specific question if provided
            if question:
                console.print(f"\n[yellow]Answering: {question}[/yellow]")
                answer_result = analyzer.ask_question(question)
                
                if answer_result['success']:
                    console.print(Panel(answer_result['answer'], title="Answer"))
                    
                    # Display question timing
                    if 'timing' in answer_result:
                        display_timing_info(answer_result['timing'], "Question Answering Performance")
                else:
                    console.print(f"[red]Error: {answer_result['error']}[/red]")
            
            # Start interactive mode if requested
            if interactive:
                start_interactive_mode(analyzer)
        else:
            console.print(f"[red]Error analyzing document: {result['error']}[/red]")
            return
    
    # Interactive mode without PDF
    elif interactive:
        start_interactive_mode(analyzer)
    
    else:
        console.print("[yellow]Use --help to see available options[/yellow]")
        console.print("\n[bold]Quick start:[/bold]")
        console.print("  python main.py --pdf document.pdf --type contract --interactive")
        console.print("  python main.py --pdf resume.pdf --type resume --question 'What are their skills?'")


def start_interactive_mode(analyzer: DocumentAnalyzer):
    """Start interactive question-answering mode."""
    
    console.print("\n[bold green]Interactive Mode[/bold green]")
    console.print("[dim]Type 'quit' or 'exit' to stop. Type 'help' for commands.[/dim]")
    
    while True:
        try:
            # Get user input
            user_input = Prompt.ask("\n[bold cyan]Question[/bold cyan]").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                console.print("[yellow]Goodbye![/yellow]")
                break
            
            if user_input.lower() == 'help':
                show_help(analyzer.get_document_type())
                continue
            
            if user_input.lower() == 'summary':
                if analyzer.is_document_loaded():
                    console.print("[yellow]Generating summary...[/yellow]")
                    summary_result = analyzer.get_document_summary()
                    
                    if summary_result['success']:
                        doc_type = analyzer.get_document_type()
                        console.print(Panel(summary_result['answer'], title=f"{doc_type.title()} Summary"))
                    else:
                        console.print(f"[red]Error: {summary_result['error']}[/red]")
                else:
                    console.print("[red]No document loaded. Please analyze a document first.[/red]")
                continue
            
            if not user_input:
                continue
            
            # Check if document is loaded
            if not analyzer.is_document_loaded():
                console.print("[red]No document loaded. Please analyze a document first.[/red]")
                console.print("[dim]Usage: python main.py --pdf document.pdf --type contract --interactive[/dim]")
                continue
            
            # Answer the question
            console.print("[yellow]Thinking...[/yellow]")
            result = analyzer.ask_question(user_input)
            
            if result['success']:
                console.print(Panel(result['answer'], title="Answer"))
                
                # Display timing for interactive questions
                if 'timing' in result:
                    display_timing_info(result['timing'], "Question Performance")
            else:
                console.print(f"[red]Error: {result['error']}[/red]")
                
        except KeyboardInterrupt:
            console.print("\n[yellow]Goodbye![/yellow]")
            break
        except Exception as e:
            console.print(f"[red]Unexpected error: {str(e)}[/red]")


def show_help(document_type: str = "generic"):
    """Show help information for interactive mode."""
    
    # Define help content based on document type
    help_content = {
        "contract": """
[bold]Available Commands:[/bold]

[cyan]help[/cyan] - Show this help message
[cyan]summary[/cyan] - Get a summary of the loaded contract
[cyan]quit/exit/q[/cyan] - Exit the program

[bold]Example Contract Questions:[/bold]
• Who are the parties involved in this contract?
• What type of contract is this?
• What are the key terms and conditions?
• What are the payment terms?
• When does this contract expire?
• What are the termination conditions?
• What are the obligations of each party?
• What is the governing law?
• What are the key dates mentioned?
""",
        
        "resume": """
[bold]Available Commands:[/bold]

[cyan]help[/cyan] - Show this help message
[cyan]summary[/cyan] - Get a summary of the loaded resume
[cyan]quit/exit/q[/cyan] - Exit the program

[bold]Example Resume Questions:[/bold]
• What is this person's name?
• Where is this person from?
• What are their key skills?
• What is their current job?
• How many years of experience do they have?
• What programming languages do they know?
• What is their educational background?
• What companies have they worked for?
""",
        
        "generic": """
[bold]Available Commands:[/bold]

[cyan]help[/cyan] - Show this help message
[cyan]summary[/cyan] - Get a summary of the loaded document
[cyan]quit/exit/q[/cyan] - Exit the program

[bold]Example Questions:[/bold]
• What is this document about?
• Who are the key people or entities mentioned?
• What are the important dates?
• What are the key terms or concepts?
• What are the main obligations or requirements?
• What financial information is mentioned?
• What is the main purpose of this document?
"""
    }
    
    help_text = help_content.get(document_type, help_content["generic"])
    console.print(Panel(help_text, title="Help", border_style="green"))


if __name__ == "__main__":
    main()
