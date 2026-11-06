import pandas as pd


def calculate_summary(df, opening_balance=0, report_date=None):
    """
    Income = rows where Comments == "Received"
    Expenses = rows where Comments == "Paid"
    Pending = rows with any other (blank) Comments
    Balance = opening balance + running total of (income - expense)
    Next day = Expense rows dated report_date + 1 day
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
    # pending_income = pending.loc[pending["Type"] == "Income", "Amount"].abs().sum()
    # pending_expense = pending.loc[pending["Type"] == "Expense", "Amount"].abs().sum()
    is_income = pending["Type"] == "Income"
    is_expense = pending["Type"] == "Expense"

    pending_income = pending.loc[is_income, "Amount"].abs().sum()
    pending_expense = pending.loc[is_expense, "Amount"].abs().sum()

    # Next day's expenses
    report_date = pd.Timestamp(report_date or pd.Timestamp.today()).normalize()
    next_day = report_date + pd.Timedelta(days=1)
    next_df = df[(df["Date"].dt.normalize() == next_day) & (df["Type"] == "Expense")]
    next_df = next_df[["Description", "Category", "Amount", "Comments"]]

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
        "pending_income_count": int(is_income.sum()),
        "pending_expense": pending_expense,
        "pending_expense_count": int(is_expense.sum()),
        "next_day": next_day,
        "next_day_expenses": next_df,
        "next_day_total": next_df["Amount"].abs().sum(),
    }

