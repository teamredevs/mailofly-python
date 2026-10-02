## 0.2.0

- Added `client.automations` resource (list, get, create, update, delete, stop, duplicate).
- Added `client.automations.runs` resource (list, get).
- Added `client.events` resource (send, list, get).

## 0.1.0

- Initial release: Python client for Mailofly REST API v1.
- Resources: accounts, contacts, templates, segments (incl. membership), campaigns (runs & send), compose, mail logs.
- `Mailofly.discovery()` for unauthenticated `GET /api/v1`.
- `MailoflyError` for API errors.
