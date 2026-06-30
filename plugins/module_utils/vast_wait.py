"""Retry utilities for VAST Data API calls."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module_utils: vast_wait
short_description: Retry utilities for VAST Data API calls
description:
  - Provides call_with_retry, a wrapper that executes VAST API calls with
    exponential backoff retry on transient HTTP errors (429, 500, 503).
  - Configurable max retries and retryable status codes allow callers to
    tune resilience for different API operations.
author:
  - Steve Fulmer (@stevefulme1)
"""

import time


def call_with_retry(fn, *args, **kwargs):
    """Call a VAST API function with exponential backoff retry."""
    max_retries = kwargs.pop("max_retries", 3)
    retry_on = kwargs.pop("retry_on", (429, 500, 503))
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
