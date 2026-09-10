# Project 665

**665 small, tested AI-engineering building blocks — one published each day.**

This is a public learning log and a portfolio of practical, dependency-light utilities for ML systems, data pipelines, and production AI.

## Structure

Each daily project lives in `projects/day-XXX-<topic>/` and contains:

- a concise problem statement and usage example;
- a focused, runnable Python module in `src/`;
- tests that demonstrate the expected behaviour;
- metadata that makes the series easy to browse.

| Day | Project | Status |
| --- | --- | --- |
| 001 | Retry with exponential backoff | Ready |
| 002 | Expense tracker | Ready |

## Daily publishing

GitHub Actions runs every day at **09:00 India Standard Time** (03:30 UTC). It generates the next self-contained project, runs its tests, and commits it to `main`. You can also run **Actions → Publish daily Project 665 entry → Run workflow** to publish the next entry manually.

The workflow only writes inside this repository and requires the repository setting **Actions → General → Workflow permissions → Read and write permissions**.

## Run locally

```bash
python scripts/generate_daily_project.py --dry-run
python scripts/generate_daily_project.py
python -m unittest discover -s projects/day-001-retry-backoff/tests
```

## Principles

1. Keep every entry small enough to understand in one sitting.
2. Include runnable code and a test — no empty contribution commits.
3. Prefer clear interfaces, type hints, and standard-library dependencies.
4. Treat the series as a record of learning, not a substitute for thoughtful engineering.

Licensed under [MIT](LICENSE).
