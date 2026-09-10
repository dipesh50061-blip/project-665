"""Day 002: Expense tracker."""

from __future__ import annotations

import json
from typing import TypeVar

T = TypeVar("T")

def monthly_total(expenses: list[dict[str, object]], month: str) -> float:
    """Return the total of records whose ISO date starts with ``YYYY-MM``."""
    return round(sum(float(item["amount"]) for item in expenses if str(item.get("date", "")).startswith(month)), 2)
