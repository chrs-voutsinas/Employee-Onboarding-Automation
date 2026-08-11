from utils.run_summary import calculate_run_summary


def test_run_summary_all_success():
    results = [
        {"status": "Success"},
        {"status": "Success"},
        {"status": "Success"}
    ]

    summary = calculate_run_summary(results)

    assert summary["total"] == 3
    assert summary["successful"] == 3
    assert summary["failed"] == 0
    assert summary["success_rate"] == 100.0


def test_run_summary_with_failures():
    results = [
        {"status": "Success"},
        {"status": "Failed"},
        {"status": "Success"}
    ]

    summary = calculate_run_summary(results)

    assert summary["total"] == 3
    assert summary["successful"] == 2
    assert summary["failed"] == 1
    assert round(summary["success_rate"], 1) == 66.7


def test_run_summary_empty_results():
    results = []

    summary = calculate_run_summary(results)

    assert summary["total"] == 0
    assert summary["successful"] == 0
    assert summary["failed"] == 0
    assert summary["success_rate"] == 0