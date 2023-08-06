"""Metadata configuration."""
import functools

import pytz
import tzlocal


@functools.lru_cache()
def tz() -> pytz.BaseTzInfo:
    """Return timezone to parse naive timestamps with."""
    return tzlocal.reload_localzone()  # type: ignore
