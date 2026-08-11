from __future__ import annotations

from typing import Any
from urllib.parse import quote, urlencode

import httpx

from .errors import MailoflyError

DEFAULT_BASE_URL = "https://www.mailofly.com"
API_PREFIX = "/api/v1"


def normalize_base_url(base_url: str | None) -> str:
    return (base_url or DEFAULT_BASE_URL).rstrip("/")


def request(
    *,
    base_url: str,
    path: str,
    method: str = "GET",
    api_key: str | None = None,
    body: Any = None,
    query: dict[str, Any] | None = None,
    timeout: float = 30.0,
) -> Any:
    path = path if path.startswith("/") else f"/{path}"
    if query:
        filtered = {k: v for k, v in query.items() if v is not None}
        if filtered:
            path += ("&" if "?" in path else "?") + urlencode(
                {k: str(v) for k, v in filtered.items()}
            )

    url = f"{base_url.rstrip('/')}{path}"
    headers: dict[str, str] = {
        "Accept": "application/json",
        "X-Mailofly-Client": "sdk/python",
    }
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    if body is not None:
        headers["Content-Type"] = "application/json"

    with httpx.Client(timeout=timeout) as client:
        res = client.request(method, url, headers=headers, json=body)

    try:
        parsed: Any = res.json() if res.content else None
    except Exception:
        parsed = res.text

    if res.is_error:
        err = "error"
        detail = None
        if isinstance(parsed, dict):
            if isinstance(parsed.get("error"), str):
                err = parsed["error"]
            if isinstance(parsed.get("message"), str):
                detail = parsed["message"]
        elif isinstance(parsed, str):
            detail = parsed
            err = res.reason_phrase or err
        else:
            err = res.reason_phrase or err
        raise MailoflyError(res.status_code, err, detail, parsed)

    return parsed


def enc(value: str) -> str:
    return quote(value, safe="")
