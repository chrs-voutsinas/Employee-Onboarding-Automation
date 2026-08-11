from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

BASE_URL = "https://opensource-demo.orangehrmlive.com/"

INPUT_FILE = BASE_DIR / "input" / "employees.csv"

OUTPUT_DIR = BASE_DIR / "output"
SCREENSHOTS_DIR = BASE_DIR / "screenshots"
LOGS_DIR = BASE_DIR / "logs"

TEST_FAILURE = False

HEADLESS = False