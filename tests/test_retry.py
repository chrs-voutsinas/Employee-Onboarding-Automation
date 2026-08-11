import pytest

from utils.retry import retry_action


def test_retry_action_success_first_attempt():
    attempts = {"count": 0}

    def test_action():
        attempts["count"] += 1
        return "Success"

    result = retry_action(
        test_action,
        max_retries=2,
        retry_delay=0
    )

    assert result == "Success"
    assert attempts["count"] == 1


def test_retry_action_succeeds_after_retries():
    attempts = {"count": 0}

    def test_action():
        attempts["count"] += 1

        if attempts["count"] < 3:
            raise Exception("Temporary failure")

        return "Success"

    result = retry_action(
        test_action,
        max_retries=2,
        retry_delay=0
    )

    assert result == "Success"
    assert attempts["count"] == 3


def test_retry_action_raises_after_final_attempt():
    attempts = {"count": 0}

    def test_action():
        attempts["count"] += 1
        raise Exception("Permanent failure")

    with pytest.raises(
        Exception,
        match="Permanent failure"
    ):
        retry_action(
            test_action,
            max_retries=2,
            retry_delay=0
        )

    assert attempts["count"] == 3