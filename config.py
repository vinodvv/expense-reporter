from pathlib import Path
import os
from dotenv import load_dotenv


load_dotenv()  # reads the .env file

# Folder where config.py lives = project root
BASE_DIR = Path(__file__).resolve().parent

# Input file
DATA_FILE = BASE_DIR / "data" / "ledger_2026-11.xlsx"

# Reports folder
REPORTS_DIR = BASE_DIR / "reports"

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
RECIPIENT = "vinovijayan@gmail.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

OPENING_BALANCE = 0  # change if starting bank balance
CURRENCY = "&#8377;"  # "₹"
