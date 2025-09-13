"""Data models for the debug CLI application."""

from .command import Command, CommandResult
from .explanation import Explanation, FixSuggestion

__all__ = ["Command", "CommandResult", "Explanation", "FixSuggestion"]
