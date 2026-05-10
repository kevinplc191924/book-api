import pandas as pd

# Counts

def book_count(df: pd.DataFrame) -> int:
    return len(df)  # Overall (completed, ongoing, dropped)

def completed_book_count(df: pd.DataFrame) -> int:
    return len(df[df["status"] == "Completed"])  # Only completed books

# Averages

def avg_reading_speed_days(df: pd.DataFrame) -> float:
    # Avoid side effects by copying the df before making modifications
    df = df.copy()

    # Cast dates
    df["start_date"] = pd.to_datetime(df["start_date"])
    df["end_date"] = pd.to_datetime(df["end_date"])

    # Only calculate for completed books (have both start and end dates)
    finished_books = df[df["status"] == "Completed"]

    # Calculate reading days (no risk of getting None)
    reading_durations = (finished_books["end_date"] - finished_books["start_date"]).dt.days

    return round(reading_durations.mean(), 2)

def avg_pages_per_day(df: pd.DataFrame) -> float:
    df = df.copy()

    # Cast dates
    df["start_date"] = pd.to_datetime(df["start_date"])
    df["end_date"] = pd.to_datetime(df["end_date"])

    # Total pages for completed books
    finished_books = df[df["status"] == "Completed"]

    # Calculate total days
    total_pages = finished_books["total_pages"].sum()

    # Calculate reading days
    reading_durations = (finished_books["end_date"] - finished_books["start_date"]).dt.days

    # Total days
    total_days = reading_durations.sum()

    # Zero division error case
    if total_days == 0:
        return 0.0

    return round(total_pages / total_days, 2)