"""Shell integration utilities for command capture and execution."""

import os
import subprocess  # nosec B404
from pathlib import Path
from typing import Any, Dict, Optional


class ShellIntegration:
    """Handles shell integration and command execution."""

    def __init__(self) -> None:
        self.shell_type = self._detect_shell()
        self.history_file = self._get_history_file()

    def _detect_shell(self) -> str:
        """Detect the current shell type."""
        shell = os.environ.get("SHELL", "")
        if "bash" in shell:
            return "bash"
        elif "zsh" in shell:
            return "zsh"
        elif "fish" in shell:
            return "fish"
        else:
            return "unknown"

    def _get_history_file(self) -> Optional[Path]:
        """Get the path to the shell history file."""
        home_dir = Path.home()

        history_files = {
            "bash": ".bash_history",
            "zsh": ".zsh_history",
            "fish": ".local/share/fish/fish_history",
        }

        if self.shell_type in history_files:
            history_path = home_dir / history_files[self.shell_type]
            if history_path.exists():
                return history_path

        return None

    def get_environment_info(self) -> Dict[str, Any]:
        """Get current environment information."""
        return {
            "shell": self.shell_type,
            "shell_path": os.environ.get("SHELL", ""),
            "working_directory": os.getcwd(),
            "user": os.environ.get("USER", ""),
            "home": os.environ.get("HOME", ""),
            "path": os.environ.get("PATH", ""),
            "python_version": self._get_python_version(),
            "os": os.name,
            "platform": os.uname().sysname if hasattr(os, "uname") else "unknown",
        }

    def _get_python_version(self) -> str:
        """Get the current Python version."""
        try:
            result = subprocess.run(  # nosec B603, B607
                ["python", "--version"], capture_output=True, text=True, timeout=5
            )
            return result.stdout.strip()
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return "unknown"

    def execute_command(
        self, command: str, timeout: int = 30
    ) -> subprocess.CompletedProcess:
        """
        Execute a command and return the result.

        Args:
            command: Command to execute
            timeout: Timeout in seconds

        Returns:
            CompletedProcess object with result
        """
        try:
            return subprocess.run(  # nosec B602
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=os.getcwd(),
            )
        except subprocess.TimeoutExpired:
            # Return a mock result for timeout
            return subprocess.CompletedProcess(
                args=command,
                returncode=124,  # Standard timeout exit code
                stdout="",
                stderr=f"Command timed out after {timeout} seconds",
            )

    def setup_shell_integration(self) -> bool:
        """
        Set up shell integration for automatic command capture.

        Returns:
            True if setup was successful, False otherwise
        """
        # This would typically involve:
        # 1. Adding a function to shell rc files
        # 2. Setting up command tracking
        # 3. Configuring error capture

        # For now, return True as a placeholder
        return True

    def get_recent_commands(self, count: int = 10) -> list[str]:
        """
        Get recent commands from shell history.

        Args:
            count: Number of recent commands to retrieve

        Returns:
            List of recent command strings
        """
        if not self.history_file or not self.history_file.exists():
            return []

        try:
            with open(self.history_file, "r", encoding="utf-8") as f:
                lines = f.readlines()

            # Get the last N non-empty lines
            recent_commands = []
            for line in reversed(lines):
                line = line.strip()
                if line and not line.startswith("#"):
                    recent_commands.append(line)
                    if len(recent_commands) >= count:
                        break

            return list(reversed(recent_commands))

        except (IOError, UnicodeDecodeError):
            return []
