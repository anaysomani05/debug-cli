"""Output formatting utilities using Rich."""

from typing import List

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from ..models.explanation import Explanation, FixSuggestion


class OutputFormatter:
    """Handles formatting and displaying explanations in the terminal."""

    def __init__(self, enable_colors: bool = True):
        """
        Initialize the output formatter.

        Args:
            enable_colors: Whether to enable colored output
        """
        self.console = Console(force_terminal=enable_colors)
        self.enable_colors = enable_colors

    def display_explanation(
        self, explanation: Explanation, raw_output: bool = False
    ) -> None:
        """
        Display an explanation in a formatted way.

        Args:
            explanation: The explanation to display
            raw_output: Whether to display raw output without formatting
        """
        if raw_output:
            self._display_raw_explanation(explanation)
        else:
            self._display_formatted_explanation(explanation)

    def _display_formatted_explanation(self, explanation: Explanation) -> None:
        """Display a formatted explanation."""
        # Summary panel
        self.console.print()
        self.console.print(
            Panel(
                explanation.summary,
                title="[bold blue]Error Summary[/bold blue]",
                border_style="blue",
            )
        )

        # Detailed explanation
        self.console.print()
        self.console.print(
            Panel(
                explanation.detailed_explanation,
                title="[bold yellow]Detailed Explanation[/bold yellow]",
                border_style="yellow",
            )
        )

        # Root cause
        self.console.print()
        self.console.print(
            Panel(
                explanation.root_cause,
                title="[bold red]Root Cause[/bold red]",
                border_style="red",
            )
        )

        # Fix suggestions
        if explanation.fix_suggestions:
            self.console.print()
            self._display_fix_suggestions(explanation.fix_suggestions)

        # Related errors
        if explanation.related_errors:
            self.console.print()
            self._display_related_errors(explanation.related_errors)

        # Prevention tips
        if explanation.prevention_tips:
            self.console.print()
            self._display_prevention_tips(explanation.prevention_tips)

        # Confidence indicator
        self.console.print()
        self._display_confidence(explanation.confidence)

    def _display_raw_explanation(self, explanation: Explanation) -> None:
        """Display raw explanation without formatting."""
        self.console.print(f"Summary: {explanation.summary}")
        self.console.print(f"Detailed: {explanation.detailed_explanation}")
        self.console.print(f"Root Cause: {explanation.root_cause}")

        if explanation.fix_suggestions:
            self.console.print("Fix Suggestions:")
            for i, fix in enumerate(explanation.fix_suggestions, 1):
                self.console.print(f"  {i}. {fix.description}")
                if fix.command:
                    self.console.print(f"     Command: {fix.command}")
                self.console.print(f"     Explanation: {fix.explanation}")
                self.console.print(f"     Confidence: {fix.confidence}")

        self.console.print(f"Overall Confidence: {explanation.confidence}")

    def _display_fix_suggestions(self, fix_suggestions: List[FixSuggestion]) -> None:
        """Display fix suggestions in a table."""
        table = Table(title="[bold green]Fix Suggestions[/bold green]")
        table.add_column("Description", style="cyan")
        table.add_column("Command", style="magenta")
        table.add_column("Confidence", style="green")

        for fix in fix_suggestions:
            confidence_color = self._get_confidence_color(fix.confidence)
            table.add_row(
                fix.description,
                fix.command or "N/A",
                f"[{confidence_color}]{fix.confidence:.1%}[/{confidence_color}]",
            )

        self.console.print(table)

        # Display detailed explanations for each fix
        for i, fix in enumerate(fix_suggestions, 1):
            self.console.print()
            self.console.print(
                Panel(
                    fix.explanation,
                    title=f"[bold green]Fix {i} Details[/bold green]",
                    border_style="green",
                )
            )

    def _display_related_errors(self, related_errors: List[str]) -> None:
        """Display related errors."""
        error_list = "\n".join(f"• {error}" for error in related_errors)
        self.console.print(
            Panel(
                error_list,
                title="[bold magenta]Related Errors[/bold magenta]",
                border_style="magenta",
            )
        )

    def _display_prevention_tips(self, prevention_tips: List[str]) -> None:
        """Display prevention tips."""
        tips_list = "\n".join(f"• {tip}" for tip in prevention_tips)
        self.console.print(
            Panel(
                tips_list,
                title="[bold cyan]Prevention Tips[/bold cyan]",
                border_style="cyan",
            )
        )

    def _display_confidence(self, confidence: float) -> None:
        """Display confidence indicator."""
        confidence_color = self._get_confidence_color(confidence)
        confidence_text = f"[{confidence_color}]{confidence:.1%}[/{confidence_color}]"

        self.console.print(
            Panel(
                f"Overall Confidence: {confidence_text}",
                title="[bold]Confidence Level[/bold]",
                border_style="white",
            )
        )

    def _get_confidence_color(self, confidence: float) -> str:
        """Get color for confidence level."""
        if confidence >= 0.8:
            return "green"
        elif confidence >= 0.6:
            return "yellow"
        else:
            return "red"

    def display_multiple_explanations(
        self, explanations: List[Explanation], raw_output: bool = False
    ) -> None:
        """
        Display multiple explanations.

        Args:
            explanations: List of explanations to display
            raw_output: Whether to display raw output
        """
        for i, explanation in enumerate(explanations, 1):
            if len(explanations) > 1:
                self.console.print(
                    f"\n[bold]Explanation {i} of {len(explanations)}[/bold]"
                )
                self.console.print("=" * 50)

            self.display_explanation(explanation, raw_output)

            if i < len(explanations):
                self.console.print("\n" + "=" * 50)

    def display_error(self, error_message: str) -> None:
        """Display an error message."""
        self.console.print()
        self.console.print(
            Panel(error_message, title="[bold red]Error[/bold red]", border_style="red")
        )

    def display_success(self, message: str) -> None:
        """Display a success message."""
        self.console.print()
        self.console.print(
            Panel(
                message, title="[bold green]Success[/bold green]", border_style="green"
            )
        )
