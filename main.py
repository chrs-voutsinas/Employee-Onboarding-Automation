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
    RETRY_DELAY,
    PAUSE_BEFORE_EXIT
)


# Load environment variables
load_dotenv()


# Read credentials
USERNAME = os.getenv("ORANGEHRM_USERNAME")
PASSWORD = os.getenv("ORANGEHRM_PASSWORD")


# Validate credentials
if not USERNAME or not PASSWORD:
    raise ValueError(
        "Missing ORANGEHRM_USERNAME or ORANGEHRM_PASSWORD in .env"
    )


# Create runtime folders
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)


# Create unique Run ID
run_id = datetime.now().strftime("%Y%m%d_%H%M%S")


# Setup logging
setup_logger(run_id)


# Create report path
report_path = OUTPUT_DIR / f"employee_results_{run_id}.csv"


def run_automation():
    results = []

    logging.info("=" * 60)
    logging.info(f"RUN START - Run ID: {run_id}")
    logging.info("=" * 60)
    logging.info("Automation started")

    # Read and validate employees
    employees = read_employees(INPUT_FILE)

    # Stop gracefully if the input file contains no employees
    if not employees:
        message = "No employees found in input file."

        print(message)
        logging.warning(message)
        logging.info("Automation completed - no employees to process")

        return

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=HEADLESS
        )

        try:
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

            logging.info(
                f"Report created: {report_path}"
            )

            # Generate run summary
            generate_run_summary(
                results,
                run_id
            )

            logging.info("Automation completed")

        finally:
            browser.close()
            logging.info("Browser closed")


def main():
    try:
        run_automation()

    except Exception as error:
        print(f"Automation failed: {error}")

        logging.exception(
            f"Automation failed with unexpected error: {error}"
        )

    finally:
        logging.info("=" * 60)
        logging.info(f"RUN END - Run ID: {run_id}")
        logging.info("=" * 60)

        if PAUSE_BEFORE_EXIT:
            input("Πάτησε Enter για να κλείσει...")


if __name__ == "__main__":
    main()