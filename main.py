from playwright.sync_api import sync_playwright
from pages.login_page import LoginPage
from pages.pim_page import PIMPage

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    login = LoginPage(page)
    login.open()
    login.login("Admin", "admin123")

    pim_page = PIMPage(page)
    pim_page.open_pim()
    pim_page.click_add_employee()

    employee_id = pim_page.create_employee(
        "John",
        "",
        "Smith"
    )

    is_valid = pim_page.validate_employee_id(employee_id)

    if is_valid:
        print(f"Employee created successfully with ID: {employee_id}")
    else:
        print("Employee creation validation failed")


    input("Πάτησε Enter για να κλείσει...")
