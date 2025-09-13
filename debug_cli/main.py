"""Main CLI interface for the debug tool."""

from typing import List, Optional

import typer
from rich.console import Console

from .ai.explanation_service import ExplanationService
from .core.command_capture import CommandCapture
from .utils.clipboard import ClipboardManager
from .utils.config import Config
from .utils.output_formatter import OutputFormatter

# Initialize Typer app
app = typer.Typer(
    name="debug",
    help="A CLI tool that explains failed terminal commands using AI",
    add_completion=False,
    rich_markup_mode="rich",
)

# Global console for consistent output
console = Console()


@app.command()
def main(
    last_n: int = typer.Option(
        1, "--last-n", "-n", help="Explain the last N failed commands"
    ),
    raw: bool = typer.Option(
        False, "--raw", "-r", help="Print raw AI output without formatting"
    ),
    copy: bool = typer.Option(
        False, "--copy", "-c", help="Copy explanation to clipboard"
    ),
    command: Optional[str] = typer.Option(
        None,
        "--command",
        help="Specific command to analyze (instead of capturing from history)",
    ),
    error: Optional[str] = typer.Option(
        None, "--error", help="Specific error output to analyze (used with --command)"
    ),
    exit_code: int = typer.Option(
        1, "--exit-code", help="Exit code for the command (used with --command)"
    ),
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Enable verbose output"
    ),
):
    """
    Explain failed terminal commands using AI.

    This tool captures failed commands and provides AI-powered explanations
    and fix suggestions.

    Examples:
        debug                    # Explain the last failed command
        debug --last-n 3         # Explain the last 3 failed commands
        debug --raw              # Get raw AI output
        debug --copy             # Copy explanation to clipboard
        debug --command "npm install" --error "package not found"
    """
    try:
        # Initialize configuration
        config = Config()

        # Validate configuration
        config_errors = config.validate()
        if config_errors:
            console.print("[red]Configuration errors:[/red]")
            for key, error in config_errors.items():
                console.print(f"  [red]{key}:[/red] {error}")
            console.print(
                "\n[yellow]Please set the required environment variables or create a .env file.[/yellow]"
            )
            raise typer.Exit(1)

        # Initialize services
        command_capture = CommandCapture()
        explanation_service = ExplanationService()
        output_formatter = OutputFormatter(enable_colors=config.enable_colors)
        clipboard_manager = ClipboardManager()

        if verbose:
            console.print(f"[blue]Configuration loaded:[/blue] {config.to_dict()}")

        # Get command results to analyze
        command_results = []

        if command:
            # Analyze specific command
            if not error:
                console.print(
                    "[red]Error: --error is required when using --command[/red]"
                )
                raise typer.Exit(1)

            command_result = command_capture.capture_current_command(
                command_text=command, error_output=error, exit_code=exit_code
            )
            command_results = [command_result]
        else:
            # Capture from history
            command_results = command_capture.get_last_failed_commands(count=last_n)

            if not command_results:
                console.print("[yellow]No failed commands found in history.[/yellow]")
                console.print(
                    "[blue]Try running a command that fails, then run 'debug' again.[/blue]"
                )
                raise typer.Exit(0)

        if verbose:
            console.print(
                f"[blue]Found {len(command_results)} command(s) to analyze[/blue]"
            )

        # Generate explanations
        explanations = explanation_service.explain_multiple_commands(command_results)

        # Display explanations
        output_formatter.display_multiple_explanations(explanations, raw_output=raw)

        # Copy to clipboard if requested
        if copy:
            if clipboard_manager.is_clipboard_available():
                # Combine all explanations into a single text
                combined_text = _combine_explanations_for_clipboard(explanations)
                if clipboard_manager.copy_to_clipboard(combined_text):
                    console.print("\n[green]Explanation copied to clipboard![/green]")
                else:
                    console.print("\n[red]Failed to copy to clipboard[/red]")
            else:
                console.print(
                    "\n[yellow]Clipboard functionality not available on this system[/yellow]"
                )

    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled by user[/yellow]")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"\n[red]An error occurred:[/red] {str(e)}")
        if verbose:
            console.print_exception()
        raise typer.Exit(1)


@app.command()
def setup():
    """Set up shell integration for automatic command capture."""
    console.print("[blue]Setting up shell integration...[/blue]")

    # This would implement shell integration setup
    # For now, just show instructions
    console.print("\n[yellow]Shell integration setup is not yet implemented.[/yellow]")
    console.print("For now, you can use the tool by:")
    console.print("1. Running a command that fails")
    console.print("2. Running 'debug' to get an explanation")
    console.print("\nOr use the --command and --error flags for specific analysis.")


@app.command()
def config():
    """Show current configuration."""
    config = Config()

    console.print("[blue]Current Configuration:[/blue]")
    config_dict = config.to_dict()

    # Hide sensitive information
    if config_dict.get("openai_api_key"):
        config_dict["openai_api_key"] = "***" + config_dict["openai_api_key"][-4:]

    for key, value in config_dict.items():
        console.print(f"  [cyan]{key}:[/cyan] {value}")

    # Show validation status
    errors = config.validate()
    if errors:
        console.print("\n[red]Configuration Issues:[/red]")
        for key, error in errors.items():
            console.print(f"  [red]{key}:[/red] {error}")
    else:
        console.print("\n[green]Configuration is valid![/green]")


@app.command()
def version():
    """Show version information."""
    from . import __version__

    console.print(f"debug-cli version {__version__}")


def _combine_explanations_for_clipboard(explanations: List) -> str:
    """Combine multiple explanations into a single text for clipboard."""
    combined = []

    for i, explanation in enumerate(explanations, 1):
        if len(explanations) > 1:
            combined.append(f"=== Explanation {i} of {len(explanations)} ===")

        combined.append(f"Summary: {explanation.summary}")
        combined.append(f"Detailed: {explanation.detailed_explanation}")
        combined.append(f"Root Cause: {explanation.root_cause}")

        if explanation.fix_suggestions:
            combined.append("\nFix Suggestions:")
            for j, fix in enumerate(explanation.fix_suggestions, 1):
                combined.append(f"{j}. {fix.description}")
                if fix.command:
                    combined.append(f"   Command: {fix.command}")
                combined.append(f"   Explanation: {fix.explanation}")
                combined.append(f"   Confidence: {fix.confidence:.1%}")

        if explanation.related_errors:
            combined.append(
                f"\nRelated Errors: {', '.join(explanation.related_errors)}"
            )

        if explanation.prevention_tips:
            combined.append(
                f"\nPrevention Tips: {', '.join(explanation.prevention_tips)}"
            )

        combined.append(f"\nOverall Confidence: {explanation.confidence:.1%}")

        if i < len(explanations):
            combined.append("\n" + "=" * 50 + "\n")

    return "\n".join(combined)


if __name__ == "__main__":
    app()
