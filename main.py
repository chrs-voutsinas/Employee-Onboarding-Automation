from playwright.sync_api import sync_playwright

from pages.login_page import LoginPage
from pages.pim_page import PIMPage
from utils.csv_reader import read_employees


employees = read_employees("input/employees.csv")

print(employees)


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    login = LoginPage(page)
    login.open()
    login.login("Admin", "admin123")

    pim_page = PIMPage(page)

    for employee in employees:
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
        else:
            print(
                f"Employee {full_name} "
                "creation validation failed"
            )

    input("Πάτησε Enter για να κλείσει...")
