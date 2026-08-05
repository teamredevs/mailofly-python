from __future__ import annotations

from typing import Any


class MailoflyError(Exception):
    """Raised when the API returns a non-2xx response."""

    def __init__(
        self,
        status: int,
        error: str,
        detail_message: str | None = None,
        body: Any = None,
    ) -> None:
        message = f"{error}: {detail_message}" if detail_message else error
        super().__init__(message)
        self.status = status
        self.error = error
        self.detail_message = detail_message
        self.body = body
