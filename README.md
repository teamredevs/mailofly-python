# mailofly

Official **Python** client for the [Mailofly REST API](https://docs.mailofly.com/api).

Requires **Python 3.9+**.

> **Source of truth:** developed in the [mailofly monorepo](https://github.com/godstark82/mailofly) under `packages/python`. This public repo is mirrored automatically on change.

## Install

```bash
pip install mailofly
```

## Usage

```python
import os
from mailofly import Mailofly, MailoflyError

client = Mailofly(os.environ["MAILOFLY_API_KEY"])

try:
    result = client.emails.send({
        "from": "Acme <onboarding@example.com>",
        "to": ["you@example.com"],
        "subject": "Hello",
        "html": "<p>Hi from Mailofly</p>",
    })
    print(result["id"])
except MailoflyError as e:
    print(e.status, e.error, e.detail_message)
```

## Docs

- [Python guide](https://docs.mailofly.com/sdks/python)
- [API reference](https://docs.mailofly.com/api)

## Releasing

1. Bump `version` in `pyproject.toml` (and this changelog) in the **monorepo** PR.
2. Merge to `main`/`master` → GitHub Action syncs this folder to `teamredevs/mailofly-python`.
3. Publish workflow runs and publishes to PyPI only when the version is new.

## License

MIT
