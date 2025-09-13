"""Tests for command capture functionality."""

from pathlib import Path
from unittest.mock import patch

from debug_cli.core.command_capture import CommandCapture
from debug_cli.models.command import CommandResult


class TestCommandCapture:
    """Test CommandCapture class."""

    def test_init(self):
        """Test CommandCapture initialization."""
        capture = CommandCapture()
        assert capture.shell_history_files is not None
        assert "bash" in capture.shell_history_files
        assert "zsh" in capture.shell_history_files

    def test_get_shell_type(self):
        """Test shell type detection."""
        capture = CommandCapture()

        with patch.dict("os.environ", {"SHELL": "/bin/bash"}):
            assert capture.get_shell_type() == "bash"

        with patch.dict("os.environ", {"SHELL": "/bin/zsh"}):
            assert capture.get_shell_type() == "zsh"

        with patch.dict("os.environ", {"SHELL": "/usr/bin/fish"}):
            assert capture.get_shell_type() == "fish"

        with patch.dict("os.environ", {"SHELL": "/bin/unknown"}):
            assert capture.get_shell_type() == "unknown"

    def test_capture_current_command(self):
        """Test capturing current command."""
        capture = CommandCapture()

        with patch("os.getcwd", return_value="/home/user/project"):
            with patch.dict("os.environ", {"SHELL": "/bin/bash"}):
                result = capture.capture_current_command(
                    command_text="python script.py",
                    error_output="ModuleNotFoundError: No module named 'script'",
                    exit_code=1,
                )

        assert result.command.text == "python script.py"
        assert result.command.working_directory == "/home/user/project"
        assert result.command.shell == "/bin/bash"
        assert result.stderr == "ModuleNotFoundError: No module named 'script'"
        assert result.exit_code == 1
        assert not result.is_successful
        assert result.has_error

    def test_get_last_failed_commands(self):
        """Test getting last failed commands."""
        capture = CommandCapture()

        # This tests the mock implementation
        results = capture.get_last_failed_commands(count=2)

        assert len(results) == 2
        assert all(isinstance(result, CommandResult) for result in results)
        assert all(not result.is_successful for result in results)

    def test_get_history_file_path(self):
        """Test getting history file path."""
        capture = CommandCapture()

        with patch("pathlib.Path.exists", return_value=True):
            with patch("pathlib.Path.home", return_value=Path("/home/user")):
                path = capture.get_history_file_path("bash")
                assert path is not None
                assert "bash_history" in str(path)

    def test_get_history_file_path_not_found(self):
        """Test getting history file path when not found."""
        capture = CommandCapture()

        with patch("pathlib.Path.exists", return_value=False):
            path = capture.get_history_file_path("bash")
            assert path is None
