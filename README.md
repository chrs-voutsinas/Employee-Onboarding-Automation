# Employee Onboarding Automation

Enterprise-style RPA automation project built with Python and Playwright.

The project automates employee creation in OrangeHRM using employee data from CSV input files.

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
- CSV result reports
- Run summary metrics
- Automated unit tests with pytest
- Modular project architecture

## Project Structure

```text
Employee Onboarding Automation/
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
│   └── employee_processor.py
│
├── tests/
│   ├── test_csv_reader.py
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
├── main.py
├── README.md
└── requirements.txt
```

## Requirements

- Python 3.12+
- Playwright
- python-dotenv
- pytest

Install the required Python packages:

```bash
pip install -r requirements.txt
```

Install the Playwright browser:

```bash
playwright install chromium
```

## Environment Variables

Credentials are not stored in the repository.

Create a `.env` file in the project root based on `.env.example`:

```env
ORANGEHRM_USERNAME=your_username
ORANGEHRM_PASSWORD=your_password
```

The `.env` file is excluded from Git through `.gitignore`.

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
```

Retry behavior is configurable through:

```python
MAX_RETRIES = 2
RETRY_DELAY = 2
```

## Running the Automation

Run the automation from the project root:

```bash
python main.py
```

The automation will:

1. Load configuration and credentials
2. Read and validate employee input
3. Launch the browser
4. Log in to OrangeHRM
5. Process each employee
6. Retry temporary failures when applicable
7. Capture screenshots for final failures
8. Generate a CSV result report
9. Generate run summary metrics
10. Write execution details to the log

## Output

Each automation run generates a timestamped CSV report inside:

```text
output/
```

The report contains:

```text
first_name
middle_name
last_name
employee_id
status
error_message
screenshot_path
```

Failed browser-processing scenarios can also generate screenshots inside:

```text
screenshots/
```

Execution logs are stored inside:

```text
logs/
```

## Automated Testing

The project uses `pytest` for automated unit testing.

Run the complete test suite from the project root:

```bash
python -m pytest -v
```

The current automated tests cover:

- Employee input validation
- CSV header validation
- Success and failure result creation
- Retry success on the first attempt
- Successful recovery after retries
- Final failure after all retry attempts
- Run summary calculations
- Empty run summary handling

The unit tests run independently of the browser, allowing core Python logic to be validated quickly without executing the full Playwright automation.

## Status

In Progress 🚧