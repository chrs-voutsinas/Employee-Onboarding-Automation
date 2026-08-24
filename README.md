# Employee Onboarding Automation

Enterprise-style RPA automation project built with Python and Playwright.

The project automates employee creation in OrangeHRM using employee data from CSV input files and provides business-friendly Excel and email reporting.

## Features

- Browser automation with Playwright
- Page Object Model (POM)
- Environment-based credential management
- CSV input processing
- Employee input validation
- CSV header validation
- Configurable test modes
- Error handling
- Automatic screenshots on failures
- Retry mechanism for temporary failures
- Execution logging
- Business-friendly Excel result reports
- HTML email reporting
- Excel report attachment
- Run summary metrics
- Automated unit tests with pytest
- Continuous Integration with GitHub Actions
- GitLab CI automated test pipeline
- Modular project architecture
- Process Design Document (PDD)

## Project Structure

```text
Employee Onboarding Automation/
│
├── .github/
│   └── workflows/
│       └── tests.yml
│
├── config/
│   └── settings.py
│
├── input/
│   ├── employees.csv
│   ├── employees_validation_test.csv
│   └── employees_header_test.csv
│
├── logs/
├── output/
│
├── pages/
│   ├── login_page.py
│   └── pim_page.py
│
├── screenshots/
│
├── services/
│   ├── email_service.py
│   └── employee_processor.py
│
├── tests/
│   ├── test_csv_reader.py
│   ├── test_email_service.py
│   ├── test_report_writer.py
│   ├── test_result_builder.py
│   ├── test_retry.py
│   └── test_run_summary.py
│
├── utils/
│   ├── csv_reader.py
│   ├── logger.py
│   ├── report_writer.py
│   ├── result_builder.py
│   ├── retry.py
│   └── run_summary.py
│
├── .env.example
├── .gitignore
├── .gitlab-ci.yml
├── main.py
├── PDD.md
├── README.md
└── requirements.txt
```

## Requirements

- Python 3.12+
- Playwright
- python-dotenv
- pytest
- openpyxl

Install the required Python packages:

```bash
pip install -r requirements.txt
```

Install the Playwright browser:

```bash
playwright install chromium
```

## Environment Variables

Credentials and email configuration are not stored in the repository.

Create a `.env` file in the project root based on `.env.example`:

```env
ORANGEHRM_USERNAME=your_username
ORANGEHRM_PASSWORD=your_password

SMTP_EMAIL=your_gmail_address
SMTP_APP_PASSWORD=your_google_app_password
REPORT_RECIPIENT_EMAIL=recipient_email_address
```

The `.env` file is excluded from Git through `.gitignore`.

### Email Configuration

Email reporting uses Gmail SMTP.

`SMTP_EMAIL` is the Gmail account used to send the report.

`SMTP_APP_PASSWORD` is a Google App Password used for SMTP authentication. The regular Gmail account password should not be stored or used by the automation.

`REPORT_RECIPIENT_EMAIL` defines the recipient of the automation report. This can be changed without modifying the Python code.

Email reporting can be enabled or disabled in `config/settings.py`:

```python
SEND_EMAIL_REPORT = True
```

The email subject can also be configured:

```python
EMAIL_SUBJECT = "Employee Onboarding Automation Report"
```

## Input

The default employee input file is:

```text
input/employees.csv
```

Expected CSV structure:

```csv
first_name,middle_name,last_name
John,,Smith
Maria,Elena,Papadopoulou
Alex,,Brown
```

`first_name` and `last_name` are required fields.

The automation validates both the CSV headers and employee data before browser processing.

## Configuration

Runtime and demo settings are managed through:

```text
config/settings.py
```

Available demo switches include:

```python
USE_VALIDATION_TEST_INPUT = False
USE_HEADER_TEST_INPUT = False
TEST_FAILURE = False
TEST_RETRY = False
HEADLESS = False
PAUSE_BEFORE_EXIT = True
SEND_EMAIL_REPORT = True
```

Retry behavior is configurable through:

```python
MAX_RETRIES = 2
RETRY_DELAY = 2
```

Only one input test mode can be enabled at a time.

## Running the Automation

Run the automation from the project root:

```bash
python main.py
```

The automation will:

1. Load configuration and credentials.
2. Read and validate employee input.
3. Launch the browser.
4. Log in to OrangeHRM.
5. Process each employee.
6. Retry temporary failures when applicable.
7. Capture screenshots for final browser-processing failures.
8. Generate a formatted Excel result report.
9. Generate run summary metrics.
10. Send an HTML email report when email reporting is enabled.
11. Attach the Excel report to the email.
12. Write execution details to the log.

Email delivery is handled separately from the core employee-processing flow. If email delivery fails, the completed employee processing and generated Excel report remain unaffected, and the email failure is recorded in the execution log.

## Excel Report

Each processed automation run generates a timestamped Excel workbook inside:

```text
output/
```

Example:

```text
employee_results_20260819_123732.xlsx
```

The business-facing report contains:

```text
First Name
Middle Name
Last Name
Employee ID
Status
Error Message
```

The workbook includes formatting, filters, frozen headers, readable column widths, and visual distinction between successful and failed records.

Technical information such as screenshot paths is intentionally excluded from the business report.

## Email Report

When email reporting is enabled, the recipient receives an HTML report containing:

- Total employees processed
- Successful employees
- Failed employees
- Employee results in a formatted HTML table
- Error information for failed records
- The detailed Excel report as an attachment

This allows the recipient to review the run directly from the email while retaining the Excel workbook for further analysis or record keeping.

## Technical Diagnostics

Technical execution information is kept separate from the business-facing output.

Failed browser-processing scenarios can generate screenshots inside:

```text
screenshots/
```

Execution logs are stored inside:

```text
logs/
```

Logs include execution progress, run summary information, errors, and email-delivery failures.

## Automated Testing

The project uses `pytest` for automated unit testing.

Run the complete test suite from the project root:

```bash
python -m pytest -v
```

The current test suite contains **20 automated tests** covering:

- Employee input validation
- CSV header validation
- Success and failure result creation
- Retry success on the first attempt
- Successful recovery after retries
- Final failure after all retry attempts
- Run summary calculations
- Empty run summary handling
- HTML email report generation
- Failure information in email reports
- HTML escaping of report data
- Excel report creation
- Business-facing Excel columns
- Exclusion of technical screenshot paths from the Excel report
- Employee result data written to the Excel workbook

The unit tests run independently of the browser, allowing core Python logic to be validated quickly without executing the full Playwright automation.

## Continuous Integration

Automated testing is integrated with both **GitHub Actions** and **GitLab CI**.

The same pytest test suite is executed in clean CI environments to verify that application logic continues to work after repository changes.

### GitHub Actions

The GitHub Actions workflow is configured through:

```text
.github/workflows/tests.yml
```

The workflow runs automatically on:

- Pushes to the `master` branch
- Pull requests targeting the `master` branch

The workflow:

1. Checks out the repository.
2. Sets up Python 3.12.
3. Installs the project dependencies.
4. Runs the complete pytest test suite.

This provides automatic verification directly within the GitHub repository whenever relevant code changes are pushed or proposed.

### GitLab CI

GitLab CI is configured through:

```text
.gitlab-ci.yml
```

When changes are pushed to the GitLab repository, the CI pipeline creates a clean Python environment, installs the project dependencies, and runs the automated pytest suite.

A JUnit test report is also generated and uploaded as a GitLab pipeline artifact.

Maintaining CI configurations for both platforms demonstrates that the automated test suite can be executed independently of the developer's local environment.

## Process Documentation

A Process Design Document (PDD) is included in the repository:

```text
PDD.md
```

The document describes:

- Business objective
- Process flow
- Input validation
- Transaction handling
- Retry behavior
- Exception handling
- Business reporting
- Technical diagnostics
- Security and configuration
- Testing and quality assurance

The PDD is maintained alongside the application so that the documented process reflects the implemented automation.

## Status

Implemented and tested