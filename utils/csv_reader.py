import csv

def read_employees(file_path):
    employees = []

    with open(file_path, mode="r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            employees.append(row)

    return employees