import argparse
import pandas as pd

import config
from reader import read_transactions
from calculator import calculate_summary
from report import build_report
from emailer import send_email


def main():
    parser = argparse.ArgumentParser(description="Income & Expense report emailer")
    parser.add_argument("--date", help="Report date, YYYY-MM-DD (default: today)")
    parser.add_argument("--no-email", action="store_true", help="Save report only, do not send.")
    args = parser.parse_args()

    report_date = pd.Timestamp(args.date or pd.Timestamp.today()).normalize()

    # 1. Read
    df = read_transactions(config.DATA_FILE)

    # 2. Calculate
    summary = calculate_summary(df, config.OPENING_BALANCE, report_date)

    # 3. Build and save a copy of the report
    html = build_report(summary)
    config.REPORTS_DIR.mkdir(exist_ok=True)
    out = config.REPORTS_DIR / f"report_{report_date:%Y-%m-%d}.html"
    out.write_text(html, encoding="utf-8")
    print("Report saved:", out)

    # 4. Send
    if args.no_email:
        print("Email skipped (--no-email)")
    else:
        subject = f"Income & Expense Report - {report_date:%d-%b-%Y}"
        send_email(subject, html, config.RECIPIENT)


if __name__ == "__main__":
    main()
