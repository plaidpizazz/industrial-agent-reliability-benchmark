from __future__ import annotations

import os
from collections.abc import Callable
from typing import TypeVar

T = TypeVar("T", bound=Callable)


def maybe_traceable(name: str, run_type: str = "chain") -> Callable[[T], T]:
    """Return a LangSmith trace decorator when tracing is explicitly enabled."""

    tracing_enabled = os.getenv("LANGSMITH_TRACING", "").lower() == "true"
    if not tracing_enabled:
        return lambda func: func

    try:
        from langsmith import traceable
    except ImportError:
        return lambda func: func

    return traceable(name=name, run_type=run_type)
