import config
from reader import read_transactions

df = read_transactions(config.DATA_FILE)
print(df.head(10))
print()
print("Rows:", len(df))
print("Comment values found:", df["Comments"].unique())
