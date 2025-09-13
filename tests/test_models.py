"""Tests for data models."""

from datetime import datetime

from debug_cli.models.command import Command, CommandResult
from debug_cli.models.explanation import Explanation, FixSuggestion


class TestCommand:
    """Test Command model."""

    def test_command_creation(self):
        """Test basic command creation."""
        cmd = Command(text="python script.py")
        assert cmd.text == "python script.py"
        assert isinstance(cmd.timestamp, datetime)

    def test_command_with_optional_fields(self):
        """Test command with optional fields."""
        cmd = Command(
            text="npm install",
            working_directory="/home/user/project",
            shell="bash",
            exit_code=1,
        )
        assert cmd.working_directory == "/home/user/project"
        assert cmd.shell == "bash"
        assert cmd.exit_code == 1


class TestCommandResult:
    """Test CommandResult model."""

    def test_command_result_creation(self):
        """Test basic command result creation."""
        cmd = Command(text="python script.py")
        result = CommandResult(
            command=cmd, stdout="Hello World", stderr="", exit_code=0
        )
        assert result.is_successful
        assert not result.has_error
        assert result.error_summary == ""

    def test_failed_command_result(self):
        """Test failed command result."""
        cmd = Command(text="python nonexistent.py")
        result = CommandResult(
            command=cmd,
            stdout="",
            stderr="python: can't open file 'nonexistent.py'",
            exit_code=2,
        )
        assert not result.is_successful
        assert result.has_error
        assert "can't open file" in result.error_summary


class TestFixSuggestion:
    """Test FixSuggestion model."""

    def test_fix_suggestion_creation(self):
        """Test basic fix suggestion creation."""
        fix = FixSuggestion(
            description="Install missing package",
            command="pip install package",
            explanation="The package is required for the script to run",
            confidence=0.9,
        )
        assert fix.description == "Install missing package"
        assert fix.command == "pip install package"
        assert fix.confidence == 0.9


class TestExplanation:
    """Test Explanation model."""

    def test_explanation_creation(self):
        """Test basic explanation creation."""
        fix = FixSuggestion(
            description="Test fix", explanation="Test explanation", confidence=0.8
        )

        explanation = Explanation(
            summary="Test summary",
            detailed_explanation="Test detailed explanation",
            root_cause="Test root cause",
            fix_suggestions=[fix],
            confidence=0.7,
        )

        assert explanation.summary == "Test summary"
        assert len(explanation.fix_suggestions) == 1
        assert explanation.primary_fix == fix
        assert not explanation.has_high_confidence

    def test_high_confidence_explanation(self):
        """Test high confidence explanation."""
        explanation = Explanation(
            summary="Test",
            detailed_explanation="Test",
            root_cause="Test",
            confidence=0.9,
        )
        assert explanation.has_high_confidence
