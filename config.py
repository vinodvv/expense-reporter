from pathlib import Path

# Folder where config.py lives = project root
BASE_DIR = Path(__file__).resolve().parent

# Input file
DATA_FILE = BASE_DIR / "data" / "ledger_2026-11.xlsx"

# Reports folder
REPORTS_DIR = BASE_DIR / "reports"

RECIPIENT = "vinovijayan@gmail.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
