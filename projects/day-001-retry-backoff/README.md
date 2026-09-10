# Day 001: Retry with exponential backoff

Computes a predictable capped delay for retryable AI API or data-pipeline operations. The function is intentionally deterministic; add random jitter at the caller when a distributed workload needs it.

```python
from main import backoff_delay

assert backoff_delay(3) == 8.0
```

Run the test with `python -m unittest discover -s tests`.
