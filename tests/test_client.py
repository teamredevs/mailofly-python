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
