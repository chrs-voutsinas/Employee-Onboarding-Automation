# Process Design Document

## Process Name

Employee Onboarding Automation

## Business Objective

Automate the creation of employee records in OrangeHRM using structured employee data from a CSV input file.

The process reduces manual data entry and provides business users with a clear execution report showing which employee records were processed successfully and which failed.

## Process Trigger

The automation starts when it is executed with a valid employee input file available in the `input` directory.

## Input

The process reads employee records from:

`input/employees.csv`

Expected fields:

- First Name
- Middle Name
- Last Name

First Name and Last Name are mandatory.

Before browser processing begins, the automation validates:

- Required CSV headers
- Required employee fields
- Input file contents

Invalid input is rejected before employee processing starts.

## High-Level Process

1. Load configuration and environment variables.
2. Read the employee CSV input file.
3. Validate the input structure and employee records.
4. Launch the browser using Playwright.
5. Log in to OrangeHRM.
6. Navigate to employee management.
7. Process each employee record individually.
8. Retry temporary processing failures when applicable.
9. Capture technical diagnostics for final failures.
10. Record the result of each employee transaction.
11. Generate a formatted Excel report.
12. Generate execution summary metrics.
13. Send an HTML email report when email reporting is enabled.
14. Attach the Excel report to the email.
15. Write execution details to the automation log.

## Transaction Processing

Each employee record is treated as an individual transaction.

A successful transaction records:

- Employee name
- Generated Employee ID
- Success status

A failed transaction records:

- Employee name
- Failed status
- Error information

A failure affecting one employee does not prevent the automation from processing the remaining employee records.

## Retry Handling

Temporary employee-processing failures can be retried automatically.

Retry behavior is configurable through:

- Maximum retry attempts
- Delay between retry attempts

If all retry attempts fail, the employee transaction is recorded as failed and technical diagnostics can be captured.

## Business Output

After employee processing, the automation generates a formatted Excel report containing:

- First Name
- Middle Name
- Last Name
- Employee ID
- Status
- Error Message

Technical diagnostic information such as screenshot paths is intentionally excluded from the business-facing report.

## Email Reporting

Email reporting can be enabled or disabled through configuration.

When enabled, the recipient receives an HTML email containing:

- Total employees processed
- Successful employees
- Failed employees
- A formatted employee results table
- Error information for failed transactions

The detailed Excel report is included as an attachment.

The report recipient is configured through environment variables and can be changed without modifying the application code.

## Exception Handling

The automation separates business-processing failures from technical/reporting failures.

### Employee Processing Failure

If an individual employee cannot be processed:

- The failure is recorded.
- Error information is captured.
- A screenshot can be generated for technical troubleshooting.
- Processing continues with the remaining employees.

### Email Delivery Failure

If the report email cannot be delivered:

- The failure is written to the execution log.
- Completed employee transactions remain valid.
- The generated Excel report remains available.
- The employee onboarding run is not marked as failed solely because email delivery failed.

## Technical Diagnostics

Technical troubleshooting information is kept separate from business-facing output.

Diagnostics can include:

- Execution logs
- Error tracebacks
- Failure screenshots
- Run identifiers

## Security and Configuration

Sensitive values are stored in environment variables and are not committed to the repository.

These include:

- Application credentials
- SMTP credentials
- Email recipient configuration

A `.env.example` file documents the required environment variables without containing real credentials.

## Testing and Quality Assurance

Core Python functionality is covered by automated tests using `pytest`.

Test coverage includes:

- Employee validation
- CSV header validation
- Result creation
- Retry behavior
- Run summary calculations
- HTML email generation
- HTML escaping
- Excel report generation
- Business-report column validation
- Exclusion of technical screenshot paths from business reports

Automated tests are also executed through the GitLab CI pipeline whenever repository changes are pushed.

## Status

Implemented and tested