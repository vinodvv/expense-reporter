import config
from reader import read_transactions
from calculator import calculate_summary
from report import build_report

df = read_transactions(config.DATA_FILE)
summary = calculate_summary(df, config.OPENING_BALANCE)
html = build_report(summary)

config.REPORTS_DIR.mkdir(exist_ok=True)
out = config.REPORTS_DIR / "test_report.html"
out.write_text(html, encoding="utf-8")
print("Saved:", out)
