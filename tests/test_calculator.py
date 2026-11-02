import config
from reader import read_transactions
from calculator import calculate_summary

df = read_transactions(config.DATA_FILE)
s = calculate_summary(df)

print(s["daily"].to_string(index=False))
print()
print("Total Income     :", s["total_income"])
print("Total Expense    :", s["total_expense"])
print("Closing Balance  :", s["closing_balance"])
print()
print("Pending Income   :", s["pending_income"])
print("Pending Expense  :", s["pending_expense"])
print(s["pending"].to_string(index=False))
