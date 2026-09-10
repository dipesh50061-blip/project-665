"""Day 001: deterministic exponential-backoff delay calculation."""

from __future__ import annotations


def backoff_delay(attempt: int, *, base_seconds: float = 1.0, maximum_seconds: float = 60.0) -> float:
    """Return a capped delay; attempt zero is the first retry."""
    if attempt < 0 or base_seconds <= 0 or maximum_seconds <= 0:
        raise ValueError("attempt, base_seconds, and maximum_seconds must be valid")
    return min(base_seconds * (2**attempt), maximum_seconds)
