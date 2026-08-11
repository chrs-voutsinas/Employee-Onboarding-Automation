def create_success_result(employee, employee_id):
    return {
        "first_name": employee["first_name"],
        "middle_name": employee["middle_name"],
        "last_name": employee["last_name"],
        "employee_id": employee_id,
        "status": "Success",
        "error_message": "",
        "screenshot_path": ""
    }


def create_failure_result(
    employee,
    error_message,
    employee_id="",
    screenshot_path=""
):
    return {
        "first_name": employee.get("first_name", ""),
        "middle_name": employee.get("middle_name", ""),
        "last_name": employee.get("last_name", ""),
        "employee_id": employee_id,
        "status": "Failed",
        "error_message": error_message,
        "screenshot_path": screenshot_path
    }