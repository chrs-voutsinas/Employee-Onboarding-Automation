from pathlib import Path


# ============================================================
# BASE CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

BASE_URL = "https://opensource-demo.orangehrmlive.com/"


# ============================================================
# DEMO SETTINGS
# ============================================================

USE_VALIDATION_TEST_INPUT = False
USE_HEADER_TEST_INPUT = False
USE_EMPTY_TEST_INPUT = False

TEST_FAILURE = False
TEST_RETRY = False

HEADLESS = False
PAUSE_BEFORE_EXIT = True


# ============================================================
# EMAIL REPORT SETTINGS
# ============================================================

SEND_EMAIL_REPORT = False

EMAIL_SUBJECT = "Employee Onboarding Automation Report"


# ============================================================
# RETRY SETTINGS
# ============================================================

MAX_RETRIES = 2
RETRY_DELAY = 2


# ============================================================
# VALIDATE DEMO CONFIGURATION
# ============================================================

enabled_input_test_modes = sum([
    USE_VALIDATION_TEST_INPUT,
    USE_HEADER_TEST_INPUT,
    USE_EMPTY_TEST_INPUT
])

if enabled_input_test_modes > 1:
    raise ValueError(
        "Only one input test mode can be enabled at a time"
    )


# ============================================================
# INPUT FILES
# ============================================================

DEFAULT_INPUT_FILE = (
    BASE_DIR / "input" / "employees.csv"
)

VALIDATION_TEST_INPUT_FILE = (
    BASE_DIR / "input" / "employees_validation_test.csv"
)

HEADER_TEST_INPUT_FILE = (
    BASE_DIR / "input" / "employees_header_test.csv"
)

EMPTY_TEST_INPUT_FILE = (
    BASE_DIR / "input" / "employees_empty_test.csv"
)


# ============================================================
# SELECT INPUT FILE
# ============================================================

if USE_EMPTY_TEST_INPUT:
    INPUT_FILE = EMPTY_TEST_INPUT_FILE

elif USE_HEADER_TEST_INPUT:
    INPUT_FILE = HEADER_TEST_INPUT_FILE

elif USE_VALIDATION_TEST_INPUT:
    INPUT_FILE = VALIDATION_TEST_INPUT_FILE

else:
    INPUT_FILE = DEFAULT_INPUT_FILE


# ============================================================
# RUNTIME DIRECTORIES
# ============================================================

OUTPUT_DIR = BASE_DIR / "output"

SCREENSHOTS_DIR = BASE_DIR / "screenshots"

LOGS_DIR = BASE_DIR / "logs"