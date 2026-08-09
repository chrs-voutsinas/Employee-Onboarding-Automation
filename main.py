import os

from playwright.sync_api import sync_playwright

from pages.login_page import LoginPage
from pages.pim_page import PIMPage
from utils.csv_reader import read_employees
from utils.report_writer import write_report


# Create runtime folders if they do not already exist
os.makedirs("output", exist_ok=True)
os.makedirs("screenshots", exist_ok=True)
os.makedirs("logs", exist_ok=True)


# Set to True only when we want to demonstrate failure handling
TEST_FAILURE = False


employees = read_employees("input/employees.csv")

print(employees)

results = []


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    login = LoginPage(page)
    login.open()
    login.login("Admin", "admin123")

    pim_page = PIMPage(page)

    for employee in employees:
        try:
            # Simulate a failure for demonstration/testing
            if TEST_FAILURE and employee["first_name"] == "Maria":
                raise Exception("Test failure for Maria")

            pim_page.open_pim()
            pim_page.click_add_employee()

            employee_id = pim_page.create_employee(
                employee["first_name"],
                employee["middle_name"],
                employee["last_name"]
            )

            full_name = " ".join(
                part for part in [
                    employee["first_name"],
                    employee["middle_name"],
                    employee["last_name"]
                ]
                if part
            )

            is_valid = pim_page.validate_employee_id(employee_id)

            if is_valid:
                print(
                    f"Employee {full_name} "
                    f"created successfully with ID: {employee_id}"
                )

                results.append({
                    "first_name": employee["first_name"],
                    "middle_name": employee["middle_name"],
                    "last_name": employee["last_name"],
                    "employee_id": employee_id,
                    "status": "Success",
                    "error_message": "",
                    "screenshot_path": ""
                })

            else:
                print(
                    f"Employee {full_name} "
                    "creation validation failed"
                )

                results.append({
                    "first_name": employee["first_name"],
                    "middle_name": employee["middle_name"],
                    "last_name": employee["last_name"],
                    "employee_id": employee_id,
                    "status": "Failed",
                    "error_message": "Employee ID validation failed",
                    "screenshot_path": ""
                })

        except Exception as error:
            screenshot_path = (
                f"screenshots/"
                f"{employee['first_name']}_{employee['last_name']}_error.png"
            )

            page.screenshot(
                path=screenshot_path,
                full_page=True
            )

            print(
                f"Employee {employee['first_name']} "
                f"{employee['last_name']} "
                f"failed with error: {error}"
            )

            results.append({
                "first_name": employee["first_name"],
                "middle_name": employee["middle_name"],
                "last_name": employee["last_name"],
                "employee_id": "",
                "status": "Failed",
                "error_message": str(error),
                "screenshot_path": screenshot_path
            })

    write_report(
        results,
        "output/employee_results.csv"
    )

    print("Report created: output/employee_results.csv")

    input("Πάτησε Enter για να κλείσει...")