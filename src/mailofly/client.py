from __future__ import annotations

from typing import Any

from ._http import API_PREFIX, enc, normalize_base_url, request


class Mailofly:
    """Mailofly REST API client."""

    def __init__(self, api_key: str, *, base_url: str | None = None) -> None:
        if not api_key or not api_key.strip():
            raise ValueError("Mailofly: api_key is required")
        self._api_key = api_key.strip()
        self._base_url = normalize_base_url(base_url)
        self.accounts = _Accounts(self)
        self.contacts = _Contacts(self)
        self.templates = _Templates(self)
        self.segments = _Segments(self)
        self.campaigns = _Campaigns(self)
        self.compose = _Compose(self)
        self.emails = _Emails(self)
        self.batch = _Batch(self)
        self.mail_logs = _MailLogs(self)

    @staticmethod
    def discovery(*, base_url: str | None = None) -> Any:
        """Unauthenticated discovery (`GET /api/v1`)."""
        return request(
            base_url=normalize_base_url(base_url),
            path=API_PREFIX,
            method="GET",
        )

    def _req(
        self,
        path: str,
        *,
        method: str = "GET",
        body: Any = None,
        query: dict[str, Any] | None = None,
    ) -> Any:
        return request(
            base_url=self._base_url,
            path=f"{API_PREFIX}{path if path.startswith('/') else '/' + path}",
            method=method,
            api_key=self._api_key,
            body=body,
            query=query,
        )


class _Accounts:
    def __init__(self, client: Mailofly) -> None:
        self._c = client

    def list(self) -> Any:
        return self._c._req("/accounts")

    def create(self, body: dict[str, Any]) -> Any:
        return self._c._req("/accounts", method="POST", body=body)

    def get(self, id: str) -> Any:
        return self._c._req(f"/accounts/{enc(id)}")

    def update(self, id: str, body: dict[str, Any]) -> Any:
        return self._c._req(f"/accounts/{enc(id)}", method="PATCH", body=body)

    def delete(self, id: str) -> Any:
        return self._c._req(f"/accounts/{enc(id)}", method="DELETE")


class _Contacts:
    def __init__(self, client: Mailofly) -> None:
        self._c = client

    def list(self, *, segment_id: str | None = None) -> Any:
        return self._c._req(
            "/contacts",
            query={"segment_id": segment_id} if segment_id else None,
        )

    def create(self, body: dict[str, Any]) -> Any:
        return self._c._req("/contacts", method="POST", body=body)

    def get(self, id: str) -> Any:
        return self._c._req(f"/contacts/{enc(id)}")

    def update(self, id: str, body: dict[str, Any]) -> Any:
        return self._c._req(f"/contacts/{enc(id)}", method="PATCH", body=body)

    def delete(self, id: str) -> Any:
        return self._c._req(f"/contacts/{enc(id)}", method="DELETE")


class _Templates:
    def __init__(self, client: Mailofly) -> None:
        self._c = client

    def list(self) -> Any:
        return self._c._req("/templates")

    def create(self, body: dict[str, Any]) -> Any:
        return self._c._req("/templates", method="POST", body=body)

    def get(self, id: str) -> Any:
        return self._c._req(f"/templates/{enc(id)}")

    def update(self, id: str, body: dict[str, Any]) -> Any:
        return self._c._req(f"/templates/{enc(id)}", method="PATCH", body=body)

    def delete(self, id: str) -> Any:
        return self._c._req(f"/templates/{enc(id)}", method="DELETE")


class _SegmentContacts:
    def __init__(self, client: Mailofly) -> None:
        self._c = client

    def list(self, segment_id: str) -> Any:
        return self._c._req(f"/segments/{enc(segment_id)}/contacts")

    def add(self, segment_id: str, body: dict[str, Any]) -> Any:
        return self._c._req(
            f"/segments/{enc(segment_id)}/contacts",
            method="POST",
            body=body,
        )

    def remove(self, segment_id: str, contact_id: str) -> Any:
        return self._c._req(
            f"/segments/{enc(segment_id)}/contacts/{enc(contact_id)}",
            method="DELETE",
        )


class _Segments:
    def __init__(self, client: Mailofly) -> None:
        self._c = client
        self.contacts = _SegmentContacts(client)

    def list(self) -> Any:
        return self._c._req("/segments")

    def create(self, body: dict[str, Any]) -> Any:
        return self._c._req("/segments", method="POST", body=body)

    def get(self, id: str) -> Any:
        return self._c._req(f"/segments/{enc(id)}")

    def update(self, id: str, body: dict[str, Any]) -> Any:
        return self._c._req(f"/segments/{enc(id)}", method="PATCH", body=body)

    def delete(self, id: str) -> Any:
        return self._c._req(f"/segments/{enc(id)}", method="DELETE")


class _Campaigns:
    def __init__(self, client: Mailofly) -> None:
        self._c = client

    def list(self) -> Any:
        return self._c._req("/campaigns")

    def create(self, body: dict[str, Any]) -> Any:
        return self._c._req("/campaigns", method="POST", body=body)

    def get(self, id: str) -> Any:
        return self._c._req(f"/campaigns/{enc(id)}")

    def update(self, id: str, body: dict[str, Any]) -> Any:
        return self._c._req(f"/campaigns/{enc(id)}", method="PATCH", body=body)

    def delete(self, id: str) -> Any:
        return self._c._req(f"/campaigns/{enc(id)}", method="DELETE")

    def runs(self, id: str) -> Any:
        return self._c._req(f"/campaigns/{enc(id)}/runs")

    def send(self, id: str, body: dict[str, Any] | None = None) -> Any:
        return self._c._req(
            f"/campaigns/{enc(id)}/send",
            method="POST",
            body=body if body is not None else {"send_now": True},
        )


class _Compose:
    def __init__(self, client: Mailofly) -> None:
        self._c = client

    def send(self, params: dict[str, Any]) -> Any:
        """Send email via POST /emails (deprecated — use client.emails)."""
        return self._c._req("/emails", method="POST", body=params)


class _Emails:
    def __init__(self, client: Mailofly) -> None:
        self._c = client

    def send(self, params: dict[str, Any]) -> Any:
        """Send transactional email via POST /emails."""
        return self._c._req("/emails", method="POST", body=params)

    def get(self, email_id: str) -> Any:
        """Retrieve sent email via GET /emails/{id}."""
        return self._c._req(f"/emails/{enc(email_id)}")

    def list(
        self,
        *,
        limit: int | None = None,
        after: str | None = None,
        before: str | None = None,
    ) -> Any:
        """List sent emails via GET /emails (Resend cursor pagination)."""
        query: dict[str, Any] = {}
        if limit is not None:
            query["limit"] = limit
        if after:
            query["after"] = after
        if before:
            query["before"] = before
        return self._c._req("/emails", query=query or None)


class _Batch:
    def __init__(self, client: Mailofly) -> None:
        self._c = client

    def send(self, emails: list[dict[str, Any]]) -> Any:
        """Send up to 100 emails via POST /emails/batch."""
        return self._c._req("/emails/batch", method="POST", body=emails)


class _MailLogs:
    def __init__(self, client: Mailofly) -> None:
        self._c = client

    def list(
        self,
        *,
        page: int | None = None,
        page_size: int | None = None,
        campaign_id: str | None = None,
        account_id: str | None = None,
        campaign_run_id: str | None = None,
        status: str | None = None,
    ) -> Any:
        return self._c._req(
            "/mail-logs",
            query={
                "page": page,
                "page_size": page_size,
                "campaign_id": campaign_id,
                "account_id": account_id,
                "campaign_run_id": campaign_run_id,
                "status": status,
            },
        )
