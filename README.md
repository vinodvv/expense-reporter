# Expense Reporter

A simple Python tool that reads a monthly Excel ledger, calculates income, expenses and a running balance, and emails a formatted HTML report. It can run automatically every day with Windows Task Scheduler.

## Features

- Reads the latest `ledger_YYYY-MM.xlsx` from the `Data/` folder automatically
- Uses the **Comments** column to decide what counts: `Received` is income, `Paid` is expense
- Calculates total income, total expense, closing balance and a **running balance by date**
- Shows a **pending summary** (items with no comment yet) kept separate from the balance
- Shows the **next expenses due** (the next date after the report date that has expenses)
- Formats amounts with Indian digit grouping (for example `₹2,78,977`)
- Sends an HTML email to one or more recipients and saves a dated copy in `reports/`

## Project structure

```
expense_reporter/
├── Data/                   # monthly ledger files (ledger_2026-11.xlsx, ...)
├── reports/                # generated reports and run_log.txt
├── tests/                  # small test scripts for each step
├── config.py               # settings (paths, recipients, SMTP, currency)
├── reader.py               # reads and cleans the Excel file
├── calculator.py           # income, expense, balance, pending, next due
├── report.py               # builds the HTML report
├── emailer.py              # sends the email over SMTP
├── main.py                 # runs the whole flow
├── run_report.bat          # helper for Windows Task Scheduler
├── requirements.txt
└── .env                    # email credentials (never commit this)
```

## Ledger format

The Excel file needs these columns (extra columns are ignored):

| Date | Type | Description | Category | Amount | Comments |
|---|---|---|---|---|---|
| 2026-11-01 | Income | Fund Transfer | Fund Transfer | 50000 | Received |
| 2026-11-01 | Expense | Credit Card Due | Credit Card Dues | 24053 | Paid |
| 2026-11-05 | Expense | Home Loan | Home Loan | 32233 | |

- `Comments = Received` counts as income.
- `Comments = Paid` counts as expense.
- Anything else (blank) is treated as **pending** and is not included in the balance.
- Files must be named `ledger_YYYY-MM.xlsx` so the newest month is picked automatically.

## Setup

**Requirements:** Python 3.9 or newer.

```bash
git clone https://github.com/vinodvv/expense-reporter.git
cd expense-reporter

python -m venv .venv
.venv\Scripts\activate            # Windows
# source .venv/bin/activate       # Mac/Linux

pip install -r requirements.txt
```

### Email credentials

The tool sends mail through Gmail SMTP using an **App Password** (your normal password will not work).

1. Turn on 2-Step Verification in your Google Account.
2. Create an App Password at `myaccount.google.com/apppasswords`.
3. Create a `.env` file in the project root:

```
SENDER_EMAIL=your_address@gmail.com
SENDER_PASSWORD=your16characterapppassword
```

### Settings

Edit `config.py`:

```python
OPENING_BALANCE = 0                                   # starting bank balance
CURRENCY = "&#8377;"                                  # currency symbol (HTML entity)
RECIPIENT = "you@example.com, other@example.com"      # comma-separated
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
```

## Usage

```bash
python main.py --no-email            # build and save the report only
python main.py                       # build, save and email the report (today's date)
python main.py --date 2026-11-04     # run as if today were 4 Nov 2026
```

Each run saves `reports/report_YYYY-MM-DD.html`.

## Run daily on Windows

1. Edit the path in `run_report.bat` to match your project folder:

   ```bat
   @echo off
   cd /d E:\Development\expense_reporter
   ".venv\Scripts\python.exe" main.py >> reports\run_log.txt 2>&1
   ```

2. Create the scheduled task (runs daily at 8:00 AM):

   ```bat
   schtasks /create /tn "ExpenseReporter" /tr "E:\Development\expense_reporter\run_report.bat" /sc daily /st 08:00
   ```

3. In Task Scheduler, tick **Run task as soon as possible after a scheduled start is missed** so a report is still sent if the PC was off.

Check `reports/run_log.txt` if an email does not arrive.

## Troubleshooting

| Problem | Cause / fix |
|---|---|
| `FileNotFoundError` for the ledger | No `ledger_*.xlsx` in `Data/`, or the name does not match the pattern |
| `PermissionError` reading the file | The workbook is open in Excel; save and close it |
| `SMTPAuthenticationError (535)` | Wrong App Password; generate a new one |
| `SENDER_EMAIL / SENDER_PASSWORD missing` | `.env` is missing or not in the project root |
| `₹` shows as `â¹` | Make sure the HTML has `<meta charset="utf-8">` |
| Email in Spam | Mark it as "Not spam" the first time |

## Privacy

This tool handles personal financial data. Do not commit your `.env` file, ledger files or generated reports. The included `.gitignore` excludes them.

## Known limitations

- Only reads the current month's file, so "Next Expenses Due" can be empty at month end even if next month's file has entries.
- Gmail SMTP is configured by default; other providers need different SMTP settings.

## License

Released under the [MIT License](LICENSE).