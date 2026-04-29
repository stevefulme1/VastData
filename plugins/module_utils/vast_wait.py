"""Retry utilities for VAST Data API calls."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import time


def call_with_retry(fn, *args, max_retries=3, retry_on=(429, 500, 503), **kwargs):
    """Call a VAST API function with exponential backoff retry."""
    last_error = None
    for attempt in range(max_retries + 1):
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            last_error = e
            status = getattr(e, "status", None) or getattr(e, "status_code", None)
            if status not in retry_on or attempt == max_retries:
                raise
            time.sleep(2 ** attempt)
    raise last_error
