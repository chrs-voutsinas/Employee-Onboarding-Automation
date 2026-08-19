import os
import smtplib
from email.message import EmailMessage
from pathlib import Path
from html import escape


SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465


def build_html_report(results):
    total = len(results)

    successful = sum(
        1 for result in results
        if result.get("status") == "Success"
    )

    failed = total - successful

    # Build employee table rows
    table_rows = ""

    for result in results:
        first_name = escape(
            str(result.get("first_name", ""))
        )

        middle_name = escape(
            str(result.get("middle_name", ""))
        )

        last_name = escape(
            str(result.get("last_name", ""))
        )

        employee_id = escape(
            str(result.get("employee_id", ""))
        )

        status = escape(
            str(result.get("status", ""))
        )

        error_message = escape(
            str(result.get("error_message", ""))
        )

        if status == "Success":
            status_style = (
                "background-color: #d9ead3;"
                "color: #274e13;"
                "font-weight: bold;"
            )
        else:
            status_style = (
                "background-color: #f4cccc;"
                "color: #990000;"
                "font-weight: bold;"
            )

        table_rows += f"""
            <tr>
                <td>{first_name}</td>
                <td>{middle_name}</td>
                <td>{last_name}</td>
                <td>{employee_id}</td>
                <td style="{status_style}">
                    {status}
                </td>
                <td>{error_message}</td>
            </tr>
        """

    html_body = f"""
    <html>
        <body style="
            font-family: Arial, sans-serif;
            color: #333333;
        ">

            <h2>
                Employee Onboarding Automation Report
            </h2>

            <p>
                The employee onboarding process has completed.
            </p>

            <table style="
                border-collapse: collapse;
                margin-bottom: 20px;
            ">
                <tr>
                    <td style="
                        padding: 6px 12px;
                        font-weight: bold;
                    ">
                        Total Employees
                    </td>

                    <td style="
                        padding: 6px 12px;
                    ">
                        {total}
                    </td>
                </tr>

                <tr>
                    <td style="
                        padding: 6px 12px;
                        font-weight: bold;
                    ">
                        Successful
                    </td>

                    <td style="
                        padding: 6px 12px;
                    ">
                        {successful}
                    </td>
                </tr>

                <tr>
                    <td style="
                        padding: 6px 12px;
                        font-weight: bold;
                    ">
                        Failed
                    </td>

                    <td style="
                        padding: 6px 12px;
                    ">
                        {failed}
                    </td>
                </tr>
            </table>

            <h3>
                Employee Results
            </h3>

            <table style="
                border-collapse: collapse;
                width: 100%;
                max-width: 1000px;
            ">

                <thead>
                    <tr style="
                        background-color: #1f4e78;
                        color: white;
                    ">
                        <th style="
                            border: 1px solid #dddddd;
                            padding: 8px;
                        ">
                            First Name
                        </th>

                        <th style="
                            border: 1px solid #dddddd;
                            padding: 8px;
                        ">
                            Middle Name
                        </th>

                        <th style="
                            border: 1px solid #dddddd;
                            padding: 8px;
                        ">
                            Last Name
                        </th>

                        <th style="
                            border: 1px solid #dddddd;
                            padding: 8px;
                        ">
                            Employee ID
                        </th>

                        <th style="
                            border: 1px solid #dddddd;
                            padding: 8px;
                        ">
                            Status
                        </th>

                        <th style="
                            border: 1px solid #dddddd;
                            padding: 8px;
                        ">
                            Error Message
                        </th>
                    </tr>
                </thead>

                <tbody>
                    {table_rows}
                </tbody>

            </table>

            <p style="
                margin-top: 20px;
                color: #666666;
            ">
                The detailed Excel report is attached
                to this email.
            </p>

            <p>
                Regards,<br>
                Employee Onboarding Automation
            </p>

        </body>
    </html>
    """

    return html_body


def send_report_email(
    results,
    report_path,
    subject
):
    smtp_email = os.getenv("SMTP_EMAIL")
    smtp_app_password = os.getenv(
        "SMTP_APP_PASSWORD"
    )
    recipient_email = os.getenv(
        "REPORT_RECIPIENT_EMAIL"
    )

    # Validate email configuration
    missing_settings = []

    if not smtp_email:
        missing_settings.append("SMTP_EMAIL")

    if not smtp_app_password:
        missing_settings.append(
            "SMTP_APP_PASSWORD"
        )

    if not recipient_email:
        missing_settings.append(
            "REPORT_RECIPIENT_EMAIL"
        )

    if missing_settings:
        raise ValueError(
            "Missing email configuration: "
            + ", ".join(missing_settings)
        )

    report_path = Path(report_path)

    if not report_path.exists():
        raise FileNotFoundError(
            f"Report attachment not found: {report_path}"
        )

    # Create email
    message = EmailMessage()

    message["From"] = smtp_email
    message["To"] = recipient_email
    message["Subject"] = subject

    # Plain-text fallback
    message.set_content(
        "Employee Onboarding Automation completed. "
        "The detailed report is attached."
    )

    # HTML report
    html_body = build_html_report(results)

    message.add_alternative(
        html_body,
        subtype="html"
    )

    # Attach Excel report
    with open(report_path, "rb") as file:
        report_data = file.read()

    message.add_attachment(
        report_data,
        maintype="application",
        subtype=(
            "vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet"
        ),
        filename=report_path.name
    )

    # Send through Gmail SMTP over SSL
    with smtplib.SMTP_SSL(
        SMTP_SERVER,
        SMTP_PORT
    ) as smtp:
        smtp.login(
            smtp_email,
            smtp_app_password
        )

        smtp.send_message(message)