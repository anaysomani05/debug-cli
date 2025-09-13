"""OpenAI API client for generating error explanations."""

import json
import os
from typing import Optional

from openai import OpenAI

from ..models.command import CommandResult
from ..models.explanation import Explanation, FixSuggestion


class OpenAIClient:
    """Client for interacting with OpenAI API to generate error explanations."""

    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo"):
        """
        Initialize the OpenAI client.

        Args:
            api_key: OpenAI API key, defaults to environment variable
            model: Model to use for explanations
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "OpenAI API key is required. Set OPENAI_API_KEY environment variable."
            )

        self.client = OpenAI(api_key=self.api_key)
        self.model = model

    def generate_explanation(self, command_result: CommandResult) -> Explanation:
        """
        Generate an AI explanation for a failed command.

        Args:
            command_result: The failed command result to explain

        Returns:
            Explanation object with AI-generated analysis
        """
        prompt = self._build_prompt(command_result)

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.3,
                max_tokens=1000,
            )

            content = response.choices[0].message.content
            return self._parse_response(content, command_result)

        except Exception as e:
            return self._create_fallback_explanation(command_result, str(e))

    def _get_system_prompt(self) -> str:
        """Get the system prompt for the AI."""
        return """You are an expert software engineer and system administrator.
Your job is to analyze failed terminal commands and provide clear, actionable
explanations and fix suggestions.

When analyzing a failed command, you should:
1. Identify the root cause of the error
2. Explain what went wrong in simple terms
3. Provide specific, actionable fix suggestions
4. Include confidence levels for your suggestions
5. Mention any related common errors
6. Provide prevention tips

Format your response as a JSON object with the following structure:
{
    "summary": "Brief summary of what went wrong",
    "detailed_explanation": "Detailed explanation of the error",
    "root_cause": "Root cause analysis",
    "fix_suggestions": [
        {
            "description": "Description of the fix",
            "command": "Suggested command (if applicable)",
            "explanation": "Why this fix works",
            "confidence": 0.9
        }
    ],
    "confidence": 0.8,
    "related_errors": ["List of related common errors"],
    "prevention_tips": ["Tips to prevent similar errors"]
}"""

    def _build_prompt(self, command_result: CommandResult) -> str:
        """Build the user prompt for the AI."""
        prompt = f"""Please analyze this failed command and provide an explanation:

Command: {command_result.command.text}
Working Directory: {command_result.command.working_directory or 'Unknown'}
Shell: {command_result.command.shell or 'Unknown'}
Exit Code: {command_result.exit_code}

Error Output:
{command_result.stderr}

Standard Output:
{command_result.stdout}

Please provide a detailed analysis and fix suggestions in the JSON format
specified in the system prompt."""

        return prompt

    def _parse_response(
        self, content: str, command_result: CommandResult
    ) -> Explanation:
        """Parse the AI response into an Explanation object."""
        try:
            # Try to extract JSON from the response
            json_start = content.find("{")
            json_end = content.rfind("}") + 1

            if json_start != -1 and json_end > json_start:
                json_str = content[json_start:json_end]
                data = json.loads(json_str)

                # Parse fix suggestions
                fix_suggestions = []
                for fix_data in data.get("fix_suggestions", []):
                    fix_suggestions.append(
                        FixSuggestion(
                            description=fix_data.get("description", ""),
                            command=fix_data.get("command"),
                            explanation=fix_data.get("explanation", ""),
                            confidence=float(fix_data.get("confidence", 0.5)),
                        )
                    )

                return Explanation(
                    summary=data.get("summary", "Error analysis"),
                    detailed_explanation=data.get("detailed_explanation", ""),
                    root_cause=data.get("root_cause", ""),
                    fix_suggestions=fix_suggestions,
                    confidence=float(data.get("confidence", 0.5)),
                    related_errors=data.get("related_errors"),
                    prevention_tips=data.get("prevention_tips"),
                )

        except (json.JSONDecodeError, KeyError, ValueError):
            pass

        # Fallback: create explanation from raw content
        return self._create_fallback_explanation(command_result, content)

    def _create_fallback_explanation(
        self, command_result: CommandResult, error_or_content: str
    ) -> Explanation:
        """Create a fallback explanation when AI response parsing fails."""
        return Explanation(
            summary="Unable to generate detailed analysis",
            detailed_explanation=f"Raw AI response: {error_or_content}",
            root_cause="Analysis failed due to response parsing error",
            fix_suggestions=[
                FixSuggestion(
                    description="Check the command syntax and try again",
                    explanation=(
                        "The command may have syntax errors or missing dependencies"
                    ),
                    confidence=0.3,
                )
            ],
            confidence=0.2,
            related_errors=["Command parsing error", "AI service unavailable"],
            prevention_tips=[
                "Verify command syntax",
                "Check dependencies",
                "Try running with verbose flags",
            ],
        )
