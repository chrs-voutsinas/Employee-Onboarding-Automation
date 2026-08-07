from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)

    page = browser.new_page()

    page.goto("https://www.wikipedia.org")

    search_box = page.locator("input[name='search']")

    search_box.fill("Playwright")
    search_box.press("Enter")
    
    input("Πάτησε Enter για να κλείσει...")