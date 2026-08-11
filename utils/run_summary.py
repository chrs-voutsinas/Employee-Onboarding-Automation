import logging


def calculate_run_summary(results):
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

    return {
        "total": total,
        "successful": successful,
        "failed": failed,
        "success_rate": success_rate
    }


def generate_run_summary(results, run_id):
    summary = calculate_run_summary(results)

    # Print summary to terminal
    print("=" * 60)
    print(f"RUN SUMMARY - {run_id}")
    print("=" * 60)
    print(f"Total Employees : {summary['total']}")
    print(f"Successful      : {summary['successful']}")
    print(f"Failed          : {summary['failed']}")
    print(f"Success Rate    : {summary['success_rate']:.1f}%")
    print("=" * 60)

    # Write summary to log
    logging.info("=" * 60)
    logging.info(f"RUN SUMMARY - {run_id}")
    logging.info("=" * 60)
    logging.info(f"Total Employees : {summary['total']}")
    logging.info(f"Successful      : {summary['successful']}")
    logging.info(f"Failed          : {summary['failed']}")
    logging.info(
        f"Success Rate    : {summary['success_rate']:.1f}%"
    )
    logging.info("=" * 60)

    return summary