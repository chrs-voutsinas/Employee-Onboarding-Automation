from playwright.sync_api import sync_playwright
from pages.login_page import LoginPage

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)

    page = browser.new_page()

    login = LoginPage(page)

    login.open()

    login.login("Admin", "admin123")

    input("Πάτησε Enter για να κλείσει...")
