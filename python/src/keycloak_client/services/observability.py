from __future__ import annotations

import time
import uuid
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from ..redaction import redact_value

EventHook = Callable[[dict[str, Any]], None]


@dataclass
class Observability:
    event_hook: EventHook | None = None

    def correlation_id(self) -> str:
        return str(uuid.uuid4())

    def emit(self, event: str, payload: dict[str, Any]) -> None:
        if self.event_hook is None:
            return
        data = dict(payload)
        data["event"] = event
        self.event_hook(redact_value(data))

    def start_timer(self) -> float:
        return time.monotonic()

    def elapsed_ms(self, start: float) -> int:
        return int((time.monotonic() - start) * 1000)
