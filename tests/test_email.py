import config
from reader import read_transactions
from calculator import calculate_summary
from report import build_report
from emailer import send_email

df = read_transactions(config.DATA_FILE)
summary = calculate_summary(df, config.OPENING_BALANCE)
html = build_report(summary)

send_email("Test - Income & Expense Report", html, config.RECIPIENT)
