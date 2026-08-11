import os
import logging

from datetime import datetime
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

from pages.login_page import LoginPage
from pages.pim_page import PIMPage
from utils.csv_reader import read_employees
from utils.report_writer import write_report
from utils.logger import setup_logger
from utils.retry import retry_action

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


# Read employees from CSV
employees = read_employees(INPUT_FILE)

results = []


with sync_playwright() as p:
    browser = p.chromium.launch(headless=HEADLESS)
    page = browser.new_page()

    login = LoginPage(page)
    login.open()
    login.login(USERNAME, PASSWORD)

    logging.info("Login successful")

    pim_page = PIMPage(page)

    for employee in employees:

        # Validate input data before browser processing
        if not employee["is_valid"]:
            validation_error = employee["validation_error"]

            print(
                f"Employee input validation failed: "
                f"{validation_error}"
            )

            logging.error(
                f"Employee input validation failed - "
                f"{employee.get('first_name', '')} "
                f"{employee.get('last_name', '')}: "
                f"{validation_error}"
            )

            results.append({
                "first_name": employee.get("first_name", ""),
                "middle_name": employee.get("middle_name", ""),
                "last_name": employee.get("last_name", ""),
                "employee_id": "",
                "status": "Failed",
                "error_message": validation_error,
                "screenshot_path": ""
            })

            continue

        try:
            full_name = " ".join(
                part for part in [
                    employee["first_name"],
                    employee["middle_name"],
                    employee["last_name"]
                ]
                if part
            )

            logging.info(
                f"Processing employee: {full_name}"
            )

            # Final failure demo
            if TEST_FAILURE and employee["first_name"] == "Maria":
                raise Exception("Test failure for Maria")

            # Counter used only for retry demonstration
            retry_test_attempts = {"count": 0}

            def create_employee():
                retry_test_attempts["count"] += 1

                # Simulate a temporary failure only on Maria's first attempt
                if (
                    TEST_RETRY
                    and employee["first_name"] == "Maria"
                    and retry_test_attempts["count"] == 1
                ):
                    raise Exception(
                        "Simulated temporary failure for retry test"
                    )

                pim_page.open_pim()
                pim_page.click_add_employee()

                return pim_page.create_employee(
                    employee["first_name"],
                    employee["middle_name"],
                    employee["last_name"]
                )

            employee_id = retry_action(
                create_employee,
                MAX_RETRIES,
                RETRY_DELAY
            )

            is_valid = pim_page.validate_employee_id(employee_id)

            if is_valid:
                print(
                    f"Employee {full_name} "
                    f"created successfully with ID: {employee_id}"
                )

                logging.info(
                    f"Employee {full_name} created successfully "
                    f"with ID: {employee_id}"
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

                logging.error(
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
                SCREENSHOTS_DIR
                / f"{run_id}_{employee['first_name']}_{employee['last_name']}_error.png"
            )

            page.screenshot(
                path=str(screenshot_path),
                full_page=True
            )

            print(
                f"Employee {employee['first_name']} "
                f"{employee['last_name']} "
                f"failed with error: {error}"
            )

            logging.error(
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
                "screenshot_path": str(screenshot_path)
            })

    write_report(
        results,
        report_path
    )

    print(f"Report created: {report_path}")

    logging.info(f"Report created: {report_path}")

    # Calculate run summary
    total = len(results)

    successful = sum(
        1
        for result in results
        if result["status"] == "Success"
    )

    failed = total - successful

    success_rate = (
        (successful / total) * 100
        if total > 0
        else 0
    )

    # Print run summary
    print("=" * 60)
    print(f"RUN SUMMARY - {run_id}")
    print("=" * 60)
    print(f"Total Employees : {total}")
    print(f"Successful      : {successful}")
    print(f"Failed          : {failed}")
    print(f"Success Rate    : {success_rate:.1f}%")
    print("=" * 60)

    # Log run summary
    logging.info("=" * 60)
    logging.info(f"RUN SUMMARY - {run_id}")
    logging.info("=" * 60)
    logging.info(f"Total Employees : {total}")
    logging.info(f"Successful      : {successful}")
    logging.info(f"Failed          : {failed}")
    logging.info(f"Success Rate    : {success_rate:.1f}%")
    logging.info("=" * 60)

    logging.info("Automation completed")

    logging.info("=" * 60)
    logging.info(f"RUN END - Run ID: {run_id}")
    logging.info("=" * 60)

    input("Πάτησε Enter για να κλείσει...")