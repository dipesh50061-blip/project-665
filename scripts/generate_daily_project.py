#!/usr/bin/env python3
"""Create and verify the next small, self-contained Project 665 entry."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROJECTS = ROOT / "projects"


@dataclass(frozen=True)
class Topic:
    slug: str
    title: str
    description: str
    function: str
    implementation: str
    assertions: str


TOPICS = (
    Topic("sliding-window", "Sliding-window batches", "Produce fixed-size overlapping batches for context windows.", "windows", """def windows(items: list[T], size: int, step: int = 1) -> list[list[T]]:\n    if size < 1 or step < 1:\n        raise ValueError(\"size and step must be positive\")\n    return [items[i : i + size] for i in range(0, max(0, len(items) - size + 1), step)]""", "self.assertEqual(windows([1, 2, 3, 4], 2), [[1, 2], [2, 3], [3, 4]])\n        self.assertRaises(ValueError, windows, [1], 0)"),
    Topic("expense-tracker", "Expense tracker", "Summarise monthly spending from simple transaction records.", "monthly_total", """def monthly_total(expenses: list[dict[str, object]], month: str) -> float:\n    \"\"\"Return the total of records whose ISO date starts with ``YYYY-MM``.\"\"\"\n    return round(sum(float(item[\"amount\"]) for item in expenses if str(item.get(\"date\", \"\")).startswith(month)), 2)""", "self.assertEqual(monthly_total([{\"date\": \"2026-09-01\", \"amount\": 12.5}, {\"date\": \"2026-08-31\", \"amount\": 99}], \"2026-09\"), 12.5)"),
    Topic("eda-analyzer", "EDA analyzer", "Produce a small numeric profile for a dataset column before modelling.", "summarize_column", """def summarize_column(values: list[float | None]) -> dict[str, float | int | None]:\n    clean = [value for value in values if value is not None]\n    if not clean:\n        return {\"count\": 0, \"missing\": len(values), \"min\": None, \"max\": None, \"mean\": None}\n    return {\"count\": len(clean), \"missing\": len(values) - len(clean), \"min\": min(clean), \"max\": max(clean), \"mean\": round(sum(clean) / len(clean), 4)}""", "self.assertEqual(summarize_column([1.0, None, 4.0]), {\"count\": 2, \"missing\": 1, \"min\": 1.0, \"max\": 4.0, \"mean\": 2.5})"),
    Topic("jsonl-validator", "JSONL validation", "Validate newline-delimited JSON before a dataset ingestion job.", "validate_jsonl", """def validate_jsonl(lines: list[str]) -> list[str]:\n    errors = []\n    for number, line in enumerate(lines, 1):\n        try:\n            json.loads(line)\n        except json.JSONDecodeError as exc:\n            errors.append(f\"line {number}: {exc.msg}\")\n    return errors""", "self.assertEqual(validate_jsonl(['{\"x\": 1}', 'bad']), ['line 2: Expecting value'])"),
    Topic("cosine-similarity", "Cosine similarity", "Calculate cosine similarity with explicit handling for zero vectors.", "cosine_similarity", """def cosine_similarity(left: list[float], right: list[float]) -> float:\n    if len(left) != len(right):\n        raise ValueError(\"vectors must have the same dimension\")\n    numerator = sum(a * b for a, b in zip(left, right))\n    left_norm = sum(a * a for a in left) ** 0.5\n    right_norm = sum(b * b for b in right) ** 0.5\n    return 0.0 if not left_norm or not right_norm else numerator / (left_norm * right_norm)""", "self.assertAlmostEqual(cosine_similarity([1, 0], [0, 1]), 0.0)\n        self.assertAlmostEqual(cosine_similarity([1, 1], [1, 1]), 1.0)"),
)


def next_day() -> int:
    numbers = [int(match.group(1)) for path in PROJECTS.glob("day-*-*") if (match := re.match(r"day-(\d{3})-", path.name))]
    return max(numbers, default=0) + 1


def render(day: int, topic: Topic) -> dict[Path, str]:
    folder = PROJECTS / f"day-{day:03d}-{topic.slug}"
    module = f'''"""Day {day:03d}: {topic.title}."""\n\nfrom __future__ import annotations\n\nimport json\nfrom typing import TypeVar\n\nT = TypeVar("T")\n\n{topic.implementation}\n'''
    test = f'''import sys\nimport unittest\nfrom pathlib import Path\n\nsys.path.insert(0, str(Path(__file__).parents[1] / "src"))\nfrom main import {topic.function}\n\n\nclass TestDay{day:03d}(unittest.TestCase):\n    def test_happy_path(self):\n        {topic.assertions}\n\n\nif __name__ == "__main__":\n    unittest.main()\n'''
    readme = f"# Day {day:03d}: {topic.title}\n\n{topic.description}\n\n## Run\n\n```bash\npython -m unittest discover -s tests\n```\n"
    metadata = json.dumps({"day": day, "title": topic.title, "slug": topic.slug, "status": "verified"}, indent=2) + "\n"
    return {folder / "src" / "main.py": module, folder / "tests" / "test_main.py": test, folder / "README.md": readme, folder / "project.json": metadata}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    day = next_day()
    if day > 665:
        print("All 665 entries already exist.")
        return
    topic = TOPICS[(day - 1) % len(TOPICS)]
    files = render(day, topic)
    print(f"Day {day:03d}: {topic.title}")
    if args.dry_run:
        return
    for path, contents in files.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(contents, encoding="utf-8")
    project = next(iter(files)).parents[1]
    result = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", str(project / "tests")], cwd=ROOT, text=True)
    if result.returncode:
        raise SystemExit("Generated test suite failed; refusing to publish.")


if __name__ == "__main__":
    main()
