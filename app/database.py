import pandas as pd

# utf-8 fix some insonsistencies while parsing the data
df = pd.read_csv("./data/book_database.csv", encoding="utf-8")

def get_books_by_author(author: str) -> pd.DataFrame:
    filtered_df = df[df["author"].str.contains(author, case=False, na=False)]
    return filtered_df

def get_books() -> pd.DataFrame:
    return df