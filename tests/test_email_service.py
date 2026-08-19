from services.email_service import build_html_report


def test_build_html_report_all_success():
    results = [
        {
            "first_name": "John",
            "middle_name": "",
            "last_name": "Smith",
            "employee_id": "12345",
            "status": "Success",
            "error_message": ""
        },
        {
            "first_name": "Maria",
            "middle_name": "Elena",
            "last_name": "Papadopoulou",
            "employee_id": "67890",
            "status": "Success",
            "error_message": ""
        }
    ]

    html = build_html_report(results)

    assert "Total Employees" in html
    assert "Successful" in html
    assert "Failed" in html

    assert "John" in html
    assert "Smith" in html
    assert "12345" in html

    assert "Maria" in html
    assert "Elena" in html
    assert "Papadopoulou" in html
    assert "67890" in html

    assert html.count("Success") >= 2


def test_build_html_report_with_failure():
    results = [
        {
            "first_name": "John",
            "middle_name": "",
            "last_name": "Smith",
            "employee_id": "12345",
            "status": "Success",
            "error_message": ""
        },
        {
            "first_name": "Alex",
            "middle_name": "",
            "last_name": "Brown",
            "employee_id": "",
            "status": "Failed",
            "error_message": "Employee creation failed"
        }
    ]

    html = build_html_report(results)

    assert "Alex" in html
    assert "Brown" in html
    assert "Failed" in html
    assert "Employee creation failed" in html


def test_build_html_report_escapes_html():
    results = [
        {
            "first_name": "<John>",
            "middle_name": "",
            "last_name": "Smith & Jones",
            "employee_id": "12345",
            "status": "Failed",
            "error_message": "<script>alert('test')</script>"
        }
    ]

    html = build_html_report(results)

    assert "&lt;John&gt;" in html
    assert "Smith &amp; Jones" in html
    assert "&lt;script&gt;" in html

    assert "<script>" not in html