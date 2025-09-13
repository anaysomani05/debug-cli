"""Service for generating and managing error explanations."""

import json
from datetime import datetime, timedelta
from typing import Any, Dict, List

from ..models.command import CommandResult
from ..models.explanation import Explanation
from .openai_client import OpenAIClient


class ExplanationService:
    """Service for generating and caching error explanations."""

    def __init__(self, cache_enabled: bool = True, cache_ttl: int = 3600):
        """
        Initialize the explanation service.

        Args:
            cache_enabled: Whether to enable caching
            cache_ttl: Cache time-to-live in seconds
        """
        self.cache_enabled = cache_enabled
        self.cache_ttl = cache_ttl
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.openai_client = OpenAIClient()

    def explain_command(self, command_result: CommandResult) -> Explanation:
        """
        Generate an explanation for a failed command.

        Args:
            command_result: The failed command result to explain

        Returns:
            Explanation object with analysis and fix suggestions
        """
        # Check cache first
        cache_key = self._generate_cache_key(command_result)
        if self.cache_enabled and cache_key in self.cache:
            cached_data = self.cache[cache_key]
            if self._is_cache_valid(cached_data):
                return self._load_from_cache(cached_data)

        # Generate new explanation
        explanation = self.openai_client.generate_explanation(command_result)

        # Cache the result
        if self.cache_enabled:
            self._save_to_cache(cache_key, explanation)

        return explanation

    def explain_multiple_commands(
        self, command_results: List[CommandResult]
    ) -> List[Explanation]:
        """
        Generate explanations for multiple failed commands.

        Args:
            command_results: List of failed command results to explain

        Returns:
            List of Explanation objects
        """
        explanations = []
        for command_result in command_results:
            explanation = self.explain_command(command_result)
            explanations.append(explanation)

        return explanations

    def _generate_cache_key(self, command_result: CommandResult) -> str:
        """Generate a cache key for a command result."""
        # Create a hash based on command text and error output
        key_data = {
            "command": command_result.command.text,
            "stderr": command_result.stderr,
            "exit_code": command_result.exit_code,
        }
        return str(hash(json.dumps(key_data, sort_keys=True)))

    def _is_cache_valid(self, cached_data: Dict[str, Any]) -> bool:
        """Check if cached data is still valid."""
        if not cached_data:
            return False

        cached_time = datetime.fromisoformat(cached_data.get("timestamp", ""))
        return datetime.now() - cached_time < timedelta(seconds=self.cache_ttl)

    def _load_from_cache(self, cached_data: Dict[str, Any]) -> Explanation:
        """Load explanation from cache data."""
        explanation_data = cached_data.get("explanation", {})

        # Reconstruct fix suggestions
        fix_suggestions = []
        for fix_data in explanation_data.get("fix_suggestions", []):
            from ..models.explanation import FixSuggestion

            fix_suggestions.append(FixSuggestion(**fix_data))

        return Explanation(
            summary=explanation_data.get("summary", ""),
            detailed_explanation=explanation_data.get("detailed_explanation", ""),
            root_cause=explanation_data.get("root_cause", ""),
            fix_suggestions=fix_suggestions,
            confidence=explanation_data.get("confidence", 0.5),
            related_errors=explanation_data.get("related_errors"),
            prevention_tips=explanation_data.get("prevention_tips"),
        )

    def _save_to_cache(self, cache_key: str, explanation: Explanation) -> None:
        """Save explanation to cache."""
        cache_data = {
            "timestamp": datetime.now().isoformat(),
            "explanation": {
                "summary": explanation.summary,
                "detailed_explanation": explanation.detailed_explanation,
                "root_cause": explanation.root_cause,
                "fix_suggestions": [
                    {
                        "description": fix.description,
                        "command": fix.command,
                        "explanation": fix.explanation,
                        "confidence": fix.confidence,
                    }
                    for fix in explanation.fix_suggestions
                ],
                "confidence": explanation.confidence,
                "related_errors": explanation.related_errors,
                "prevention_tips": explanation.prevention_tips,
            },
        }

        self.cache[cache_key] = cache_data

    def clear_cache(self) -> None:
        """Clear the explanation cache."""
        self.cache.clear()

    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        return {
            "cache_enabled": self.cache_enabled,
            "cache_size": len(self.cache),
            "cache_ttl": self.cache_ttl,
            "valid_entries": sum(
                1 for data in self.cache.values() if self._is_cache_valid(data)
            ),
        }
