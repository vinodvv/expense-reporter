from reader import read_transactions
from calculator import calculate_summary
from report import build_report
from emailer import send_email
import config


def main():
    df = read_transactions(config.DATA_FILE)
    summary = calculate_summary(df)
    body = build_report(summary)
    send_email("Income & Expense Report", body, config.RECIPIENT)


if __name__ == "__main__":
    main()
