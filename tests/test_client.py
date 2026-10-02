from mailofly import Mailofly, MailoflyError


def test_requires_api_key() -> None:
    try:
        Mailofly("")
        assert False, "expected ValueError"
    except ValueError:
        pass


def test_error_message() -> None:
    err = MailoflyError(401, "unauthorized", "Invalid key")
    assert err.status == 401
    assert "unauthorized" in str(err)
    assert err.detail_message == "Invalid key"


def test_automations_and_events_resources() -> None:
    client = Mailofly("mf_live_test123")
    assert hasattr(client, "automations")
    assert hasattr(client.automations, "runs")
    assert hasattr(client, "events")
    assert callable(client.automations.list)
    assert callable(client.automations.create)
    assert callable(client.automations.get)
    assert callable(client.automations.update)
    assert callable(client.automations.delete)
    assert callable(client.automations.stop)
    assert callable(client.automations.duplicate)
    assert callable(client.automations.runs.list)
    assert callable(client.automations.runs.get)
    assert callable(client.events.send)
    assert callable(client.events.list)
    assert callable(client.events.get)

