# Employee Onboarding Automation

Enterprise-style RPA automation project built with Python and Playwright.

The automation reads employee data from a CSV file, logs into OrangeHRM, creates employees through the PIM module, validates the generated employee IDs, and produces run-specific reports, logs, and screenshots for failed transactions.

## Features

- Automated login to OrangeHRM
- Employee data input from CSV
- Employee creation through the PIM module
- Employee ID validation
- Success and failure handling per employee
- CSV execution reports
- Automatic screenshots on errors
- Run-specific logging
- Unique Run ID for each execution
- Environment-based credential management
- Centralized configuration
- Headless browser support
- Test failure mode for exception-handling demonstration

## Project Structure

```text
Employee Onboarding Automation/
│
├── config/
│   └── settings.py
│
├── input/
│   └── employees.csv
│
├── logs/
├── output/
├── pages/
│   ├── login_page.py
│   └── pim_page.py
│
├── screenshots/
├── utils/
│   ├── csv_reader.py
│   ├── logger.py
│   └── report_writer.py
│
├── .env.example
├── .gitignore
├── main.py
├── README.md
└── requirements.txt
```

## Requirements

- Python 3.12
- Playwright
- Chromium

## Installation

Clone the repository and open the project directory.

Install the required Python packages:

```bash
pip install -r requirements.txt
```

Install the Chromium browser used by Playwright:

```bash
playwright install chromium
```

## Environment Variables

Create a `.env` file in the project root based on `.env.example`.

Example:

```env
ORANGEHRM_USERNAME=your_username
ORANGEHRM_PASSWORD=your_password
```

The `.env` file contains credentials and is excluded from Git through `.gitignore`.

## Configuration

Application settings are stored in:

```text
config/settings.py
```

Available settings include:

```python
BASE_URL = "https://opensource-demo.orangehrmlive.com/"
INPUT_FILE = "input/employees.csv"
TEST_FAILURE = False
HEADLESS = False
```

`TEST_FAILURE` can be enabled to demonstrate exception handling and screenshot creation.

`HEADLESS` controls whether the Chromium browser is displayed during execution.

## Running the Automation

Run:

```bash
python main.py
```

Each execution generates a unique Run ID.

The same Run ID is used to associate the execution artifacts:

```text
logs/automation_<RUN_ID>.log

output/employee_results_<RUN_ID>.csv

screenshots/<RUN_ID>_<EMPLOYEE>_error.png
```

Screenshots are generated only when an employee transaction fails.

## Input

Employee data is read from:

```text
input/employees.csv
```

Example:

```csv
first_name,middle_name,last_name
John,,Smith
Maria,Elena,Papadopoulou
Alex,,Brown
```

## Output

For every employee, the automation records:

- First name
- Middle name
- Last name
- Employee ID
- Status
- Error message
- Screenshot path

A successful transaction contains the generated employee ID and a `Success` status.

A failed transaction contains a `Failed` status, the error message, and the path to the captured screenshot.

## Status

In Progress 🚧