from __future__ import annotations

import asyncio
from collections.abc import Coroutine
from typing import Any, TypeVar

T = TypeVar("T")


def run_async(coro: Coroutine[Any, Any, T]) -> T:
    """Run one SDK coroutine from synchronous code (scripts, one-off CLIs).

    Do not call from inside an already running event loop; prefer ``async`` entrypoints
    in ASGI apps.
    """
    return asyncio.run(coro)
