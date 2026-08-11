from utils.result_builder import (
    create_success_result,
    create_failure_result
)


def test_create_success_result():
    employee = {
        "first_name": "John",
        "middle_name": "",
        "last_name": "Smith"
    }

    employee_id = "123456"

    result = create_success_result(
        employee,
        employee_id
    )

    assert result["first_name"] == "John"
    assert result["last_name"] == "Smith"
    assert result["employee_id"] == "123456"
    assert result["status"] == "Success"
    assert result["error_message"] == ""
    assert result["screenshot_path"] == ""


def test_create_failure_result():
    employee = {
        "first_name": "Maria",
        "middle_name": "Elena",
        "last_name": "Papadopoulou"
    }

    error_message = "Test failure"
    screenshot_path = "screenshots/test_error.png"

    result = create_failure_result(
        employee,
        error_message,
        screenshot_path=screenshot_path
    )

    assert result["first_name"] == "Maria"
    assert result["middle_name"] == "Elena"
    assert result["last_name"] == "Papadopoulou"
    assert result["employee_id"] == ""
    assert result["status"] == "Failed"
    assert result["error_message"] == "Test failure"
    assert result["screenshot_path"] == "screenshots/test_error.png"