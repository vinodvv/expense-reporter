def calculate_summary(df, opening_balance=0):
    """
    Income = rows where Comments == "Received"
    Expenses = rows where Comments == "Paid"
    Pending = rows with any other (blank) Comments
    Balance = opening balance + running total of (income - expense)
    """
    df = df.copy()
    amount = df["Amount"].abs()

    df["Income"] = amount.where(df["Comments"] == "Received", 0)
    df["Expense"] = amount.where(df["Comments"] == "Paid", 0)

    # Daily totals and running balance
    daily = df.groupby("Date")[["Income", "Expense"]].sum().reset_index()
    daily["Net"] = daily["Income"] - daily["Expense"]
    daily["Balance"] = opening_balance + daily["Net"].cumsum()

    # Pending items (not yet paid / received)
    pending = df[~df["Comments"].isin(["Paid", "Received"])]
    pending_income = pending.loc[pending["Type"] == "Income", "Amount"].abs().sum()
    pending_expense = pending.loc[pending["Type"] == "Expense", "Amount"].abs().sum()

    total_income = df["Income"].sum()
    total_expense = df["Expense"].sum()

    return {
        "opening_balance": opening_balance,
        "total_income": total_income,
        "total_expense": total_expense,
        "closing_balance": opening_balance + total_income - total_expense,
        "daily": daily,
        "pending": pending[["Date", "Type", "Description", "Amount"]],
        "pending_income": pending_income,
        "pending_expense": pending_expense
    }

