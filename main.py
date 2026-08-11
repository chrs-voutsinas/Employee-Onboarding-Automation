import os
import logging

from datetime import datetime
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

from pages.login_page import LoginPage
from pages.pim_page import PIMPage

from services.employee_processor import process_employee

from utils.csv_reader import read_employees
from utils.report_writer import write_report
from utils.logger import setup_logger
from utils.run_summary import generate_run_summary

from config.settings import (
    INPUT_FILE,
    OUTPUT_DIR,
    SCREENSHOTS_DIR,
    LOGS_DIR,
    TEST_FAILURE,
    TEST_RETRY,
    HEADLESS,
    MAX_RETRIES,
    RETRY_DELAY
)


# Load environment variables from .env
load_dotenv()


# Read credentials from environment variables
USERNAME = os.getenv("ORANGEHRM_USERNAME")
PASSWORD = os.getenv("ORANGEHRM_PASSWORD")


# Validate credentials
if not USERNAME or not PASSWORD:
    raise ValueError(
        "Missing ORANGEHRM_USERNAME or ORANGEHRM_PASSWORD in .env"
    )


# Create runtime folders if they do not already exist
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)


# Create a unique Run ID
run_id = datetime.now().strftime("%Y%m%d_%H%M%S")


# Setup logging for this specific run
setup_logger(run_id)


# Create a unique report path for this run
report_path = OUTPUT_DIR / f"employee_results_{run_id}.csv"


# Log the beginning of the automation run
logging.info("=" * 60)
logging.info(f"RUN START - Run ID: {run_id}")
logging.info("=" * 60)
logging.info("Automation started")


# Read and validate employees from CSV
employees = read_employees(INPUT_FILE)

results = []


# Start browser automation
with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=HEADLESS
    )

    page = browser.new_page()

    # Login
    login = LoginPage(page)
    login.open()
    login.login(
        USERNAME,
        PASSWORD
    )

    logging.info("Login successful")

    # Initialize PIM page
    pim_page = PIMPage(page)

    # Process employees
    for employee in employees:
        result = process_employee(
            employee=employee,
            pim_page=pim_page,
            page=page,
            run_id=run_id,
            screenshots_dir=SCREENSHOTS_DIR,
            max_retries=MAX_RETRIES,
            retry_delay=RETRY_DELAY,
            test_failure=TEST_FAILURE,
            test_retry=TEST_RETRY
        )

        results.append(result)

    # Create CSV report
    write_report(
        results,
        report_path
    )

    print(f"Report created: {report_path}")
    logging.info(f"Report created: {report_path}")

    # Generate run summary
    generate_run_summary(
        results,
        run_id
    )

    logging.info("Automation completed")

    logging.info("=" * 60)
    logging.info(f"RUN END - Run ID: {run_id}")
    logging.info("=" * 60)

    input("Πάτησε Enter για να κλείσει...")