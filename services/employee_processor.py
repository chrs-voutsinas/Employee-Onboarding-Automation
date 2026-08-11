import logging

from utils.retry import retry_action
from utils.result_builder import (
    create_success_result,
    create_failure_result
)


def process_employee(
    employee,
    pim_page,
    page,
    run_id,
    screenshots_dir,
    max_retries,
    retry_delay,
    test_failure=False,
    test_retry=False
):
    # Validate employee input before browser processing
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

        return create_failure_result(
            employee,
            validation_error
        )

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

    try:
        # Final failure demo
        if test_failure and employee["first_name"] == "Maria":
            raise Exception("Test failure for Maria")

        # Counter used only for retry demonstration
        retry_test_attempts = {"count": 0}

        def create_employee():
            retry_test_attempts["count"] += 1

            # Simulate a temporary failure on Maria's first attempt
            if (
                test_retry
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
            max_retries,
            retry_delay
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

            return create_success_result(
                employee,
                employee_id
            )

        print(
            f"Employee {full_name} "
            "creation validation failed"
        )

        logging.error(
            f"Employee {full_name} "
            "creation validation failed"
        )

        return create_failure_result(
            employee,
            "Employee ID validation failed",
            employee_id=employee_id
        )

    except Exception as error:
        screenshot_path = (
            screenshots_dir
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

        return create_failure_result(
            employee,
            str(error),
            screenshot_path=str(screenshot_path)
        )