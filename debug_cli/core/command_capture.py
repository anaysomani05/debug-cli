"""Command capture functionality for retrieving failed commands."""

import os
from pathlib import Path
from typing import List, Optional

from ..models.command import Command, CommandResult


class CommandCapture:
    """Handles capturing and retrieving failed terminal commands."""

    def __init__(self) -> None:
        self.shell_history_files = {
            "bash": [".bash_history", ".bashrc"],
            "zsh": [".zsh_history", ".zshrc"],
            "fish": [".local/share/fish/fish_history"],
        }

    def get_last_failed_commands(self, count: int = 1) -> List[CommandResult]:
        """
        Retrieve the last N failed commands from shell history.

        Args:
            count: Number of failed commands to retrieve

        Returns:
            List of CommandResult objects representing failed commands
        """
        # For now, we'll implement a simple approach
        # In a real implementation, this would parse shell history files
        # and identify failed commands based on exit codes

        # This is a placeholder implementation
        # In practice, you'd need to:
        # 1. Parse shell history files
        # 2. Track command exit codes
        # 3. Identify failed commands

        return self._get_mock_failed_commands(count)

    def _get_mock_failed_commands(self, count: int) -> List[CommandResult]:
        """Mock implementation for demonstration purposes."""
        mock_commands = [
            CommandResult(
                command=Command(
                    text="python nonexistent_script.py",
                    working_directory="/home/user/project",
                    shell="bash",  # nosec B604
                    exit_code=2,
                ),
                stdout="",
                stderr=(
                    "python: can't open file 'nonexistent_script.py': "
                    "[Errno 2] No such file or directory"
                ),
                exit_code=2,
                execution_time=0.1,
            ),
            CommandResult(
                command=Command(
                    text="npm install missing-package",
                    working_directory="/home/user/project",
                    shell="bash",  # nosec B604
                    exit_code=1,
                ),
                stdout="",
                stderr=(
                    "npm ERR! code E404\nnpm ERR! 404 Not Found - GET "
                    "https://registry.npmjs.org/missing-package"
                ),
                exit_code=1,
                execution_time=2.5,
            ),
            CommandResult(
                command=Command(
                    text="git push origin main",
                    working_directory="/home/user/project",
                    shell="bash",  # nosec B604
                    exit_code=1,
                ),
                stdout="",
                stderr=(
                    "error: failed to push some refs to 'origin'\n"
                    "hint: Updates were rejected because the remote contains work "
                    "that you do\nhint: not have locally."
                ),
                exit_code=1,
                execution_time=1.2,
            ),
        ]

        return mock_commands[:count]

    def capture_current_command(
        self, command_text: str, error_output: str, exit_code: int = 1
    ) -> CommandResult:
        """
        Capture a command that just failed.

        Args:
            command_text: The command that was executed
            error_output: The error output from stderr
            exit_code: The exit code of the command

        Returns:
            CommandResult object representing the failed command
        """
        return CommandResult(
            command=Command(
                text=command_text,
                working_directory=os.getcwd(),
                shell=os.environ.get("SHELL", "unknown"),  # nosec B604
                exit_code=exit_code,
            ),
            stdout="",
            stderr=error_output,
            exit_code=exit_code,
            execution_time=None,
        )

    def get_shell_type(self) -> str:
        """Get the current shell type."""
        shell = os.environ.get("SHELL", "")
        if "bash" in shell:
            return "bash"
        elif "zsh" in shell:
            return "zsh"
        elif "fish" in shell:
            return "fish"
        else:
            return "unknown"

    def get_history_file_path(self, shell_type: Optional[str] = None) -> Optional[Path]:
        """
        Get the path to the shell history file.

        Args:
            shell_type: Shell type, defaults to current shell

        Returns:
            Path to history file or None if not found
        """
        if shell_type is None:
            shell_type = self.get_shell_type()

        if shell_type not in self.shell_history_files:
            return None

        home_dir = Path.home()
        for history_file in self.shell_history_files[shell_type]:
            history_path = home_dir / history_file
            if history_path.exists():
                return history_path

        return None
