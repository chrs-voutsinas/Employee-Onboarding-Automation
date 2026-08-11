import pytest

from utils.csv_reader import (
    validate_employee,
    validate_csv_headers
)


def test_valid_employee():
    employee = {
        "first_name": "John",
        "middle_name": "",
        "last_name": "Smith"
    }

    is_valid, validation_error = validate_employee(employee)

    assert is_valid is True
    assert validation_error == ""


def test_missing_first_name():
    employee = {
        "first_name": "",
        "middle_name": "",
        "last_name": "Johnson"
    }

    is_valid, validation_error = validate_employee(employee)

    assert is_valid is False
    assert validation_error == "Missing required field(s): first_name"


def test_missing_last_name():
    employee = {
        "first_name": "John",
        "middle_name": "",
        "last_name": ""
    }

    is_valid, validation_error = validate_employee(employee)

    assert is_valid is False
    assert validation_error == "Missing required field(s): last_name"


def test_valid_csv_headers():
    fieldnames = [
        "first_name",
        "middle_name",
        "last_name"
    ]

    validate_csv_headers(fieldnames)


def test_missing_csv_header():
    fieldnames = [
        "firstname",
        "middle_name",
        "last_name"
    ]

    with pytest.raises(
        ValueError,
        match=r"Missing required CSV column\(s\): first_name"
    ):
        validate_csv_headers(fieldnames)