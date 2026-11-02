import pandas as pd

REQUIRED_COLUMNS = ["Date", "Type", "Description", "Category", "Amount", "Comments"]


def read_transactions(path):
    """Read CSV / Excel and return a clean DataFrame."""
    df = pd.read_excel(path)

    # Remove stray spaces from column names
    df.columns = df.columns.str.strip()

    # Check all required columns exist
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns in file: {missing}")

    # Keep only the columns we need
    df = df[REQUIRED_COLUMNS].copy()

    # Clean the data:
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
    df["Type"] = df["Type"].astype("object").fillna("").astype(str).str.strip().str.title()
    df["Comments"] = df["Comments"].astype("object").fillna("").astype(str).str.strip().str.title()

    # Drop rows with a bad date or amount
    df = df.dropna(subset=["Date", "Amount"])

    # Oldest first (needed for the running balance later)
    df = df.sort_values("Date").reset_index(drop=True)

    return df
