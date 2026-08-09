import csv


def write_report(results, file_path):
    fieldnames = [
        "first_name",
        "middle_name",
        "last_name",
        "employee_id",
        "status",
        "error_message",
        "screenshot_path"
    ]

    with open(file_path, mode="w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(results)