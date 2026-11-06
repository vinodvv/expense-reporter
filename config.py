from pathlib import Path
import os
from dotenv import load_dotenv


load_dotenv()  # reads the .env file

# Folder where config.py lives = project root
BASE_DIR = Path(__file__).resolve().parent

# Input file
# DATA_FILE = BASE_DIR / "data" / "ledger_2026-11.xlsx"
DATA_DIR = BASE_DIR / "data"

def find_latest_ledger():
    """Return the newest ledger_".xlsx in the Data folder (e.g. ledger_2026-12.xlsx"""
    files = sorted(
        f for f in DATA_DIR.glob("ledger_*.xlsx")
        if not f.name.startswith("~$")  # skip Excel's temporary lock files
    )
    if not files:
        raise FileNotFoundError(f"No ledger_*.xlsx file found in {DATA_DIR}")
    return files[-1]


DATA_FILE = find_latest_ledger()


# Reports folder
REPORTS_DIR = BASE_DIR / "reports"

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
RECIPIENT = os.getenv("RECIPIENTS", "vinovijayan@gmail.com")
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

OPENING_BALANCE = 0  # change if starting bank balance
CURRENCY = "&#8377;"  # "₹"
