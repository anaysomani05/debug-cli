"""Command-related data models."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class Command(BaseModel):
    """Represents a terminal command."""

    text: str = Field(..., description="The command text")
    timestamp: datetime = Field(
        default_factory=datetime.now, description="When the command was executed"
    )
    working_directory: Optional[str] = Field(
        None, description="Working directory where command was run"
    )
    shell: Optional[str] = Field(None, description="Shell type (bash, zsh, fish, etc.)")
    exit_code: Optional[int] = Field(None, description="Command exit code")


class CommandResult(BaseModel):
    """Represents the result of executing a command."""

    command: Command = Field(..., description="The executed command")
    stdout: str = Field(default="", description="Standard output")
    stderr: str = Field(default="", description="Standard error output")
    exit_code: int = Field(..., description="Exit code of the command")
    execution_time: Optional[float] = Field(
        None, description="Execution time in seconds"
    )

    @property
    def is_successful(self) -> bool:
        """Check if the command was successful."""
        return self.exit_code == 0

    @property
    def has_error(self) -> bool:
        """Check if the command produced error output."""
        return bool(self.stderr.strip())

    @property
    def error_summary(self) -> str:
        """Get a summary of the error output."""
        if not self.has_error:
            return ""

        # Take first few lines of stderr for summary
        lines = self.stderr.strip().split("\n")
        if len(lines) <= 3:
            return self.stderr.strip()

        return "\n".join(lines[:3]) + "\n..."
