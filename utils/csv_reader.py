import csv


REQUIRED_COLUMNS = [
    "first_name",
    "middle_name",
    "last_name"
]


def validate_csv_headers(fieldnames):
    if not fieldnames:
        raise ValueError("CSV file does not contain headers")

    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in fieldnames
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required CSV column(s): {', '.join(missing_columns)}"
        )


def validate_employee(employee):
    required_fields = [
        "first_name",
        "last_name"
    ]

    missing_fields = []

    for field in required_fields:
        if not employee.get(field) or not employee[field].strip():
            missing_fields.append(field)

    if missing_fields:
        return False, (
            f"Missing required field(s): {', '.join(missing_fields)}"
        )

    return True, ""


def read_employees(file_path):
    employees = []

    with open(
        file_path,
        mode="r",
        encoding="utf-8",
        newline=""
    ) as file:

        reader = csv.DictReader(file)

        validate_csv_headers(reader.fieldnames)

        for row in reader:
            is_valid, validation_error = validate_employee(row)

            row["is_valid"] = is_valid
            row["validation_error"] = validation_error

            employees.append(row)

    return employees