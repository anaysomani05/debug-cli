"""Explanation-related data models."""

from typing import List, Optional

from pydantic import BaseModel, Field


class FixSuggestion(BaseModel):
    """Represents a suggested fix for a command error."""

    description: str = Field(..., description="Description of the fix")
    command: Optional[str] = Field(None, description="Suggested command to run")
    explanation: str = Field(..., description="Explanation of why this fix works")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence level (0-1)")


class Explanation(BaseModel):
    """Represents an AI-generated explanation for a failed command."""

    summary: str = Field(..., description="Brief summary of what went wrong")
    detailed_explanation: str = Field(
        ..., description="Detailed explanation of the error"
    )
    root_cause: str = Field(..., description="Root cause analysis")
    fix_suggestions: List[FixSuggestion] = Field(
        default_factory=list, description="List of suggested fixes"
    )
    confidence: float = Field(
        ..., ge=0.0, le=1.0, description="Overall confidence level (0-1)"
    )
    related_errors: Optional[List[str]] = Field(
        None, description="Related common errors"
    )
    prevention_tips: Optional[List[str]] = Field(
        None, description="Tips to prevent similar errors"
    )

    @property
    def primary_fix(self) -> Optional[FixSuggestion]:
        """Get the highest confidence fix suggestion."""
        if not self.fix_suggestions:
            return None
        return max(self.fix_suggestions, key=lambda x: x.confidence)

    @property
    def has_high_confidence(self) -> bool:
        """Check if the explanation has high confidence."""
        return self.confidence >= 0.8
