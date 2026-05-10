from fastapi import FastAPI, HTTPException, Query

from typing import List, Optional

from .analytics import (
    avg_reading_speed_days,
    book_count,
    completed_book_count,
    avg_pages_per_day,
)

from .schemas import Book, AuthorStats, GlobalStats

from .database import get_books_by_author, get_books

from .utils import clean_for_json

# Initialize the app
app = FastAPI()

# FastAPI checks routes top to bottom, so the order is from specific to general


# Get stats by author
@app.get("/books/analytics/{author_name}", response_model=AuthorStats)
async def get_author_stats(author_name: str):
    data = get_books_by_author(author_name)

    # Can't proceed if an author is not found
    if data.empty:
        raise HTTPException(status_code=404, detail="Author not found")

    # Stats for the selected author
    avg_speed = avg_reading_speed_days(data)
    count = book_count(data)

    # Return the data as defined in the schema
    return AuthorStats(
        author_name=author_name, avg_reading_speed_days=avg_speed, book_count=count
    )


# Get overall stats
@app.get("/books/analytics", response_model=GlobalStats)
async def get_global_stats():
    data = get_books()  # returns the whole dataset

    # Compute the stats (can proceed because data is not empty)
    overall_book_count = book_count(data)
    completed_books = completed_book_count(data)
    avg_speed = avg_reading_speed_days(data)
    avg_pages = avg_pages_per_day(data)

    return GlobalStats(
        book_count=overall_book_count,
        completed_book_count=completed_books,
        avg_reading_speed_days=avg_speed,
        avg_pages_per_day=avg_pages,
    )


# Get the entire dataset or apply filters
@app.get("/books", response_model=List[Book])
async def read_books(
    author: Optional[str] = None,
    category: Optional[str] = None,
    status: Optional[str] = None,
    language: Optional[str] = None,
    limit: int = Query(10, gt=0),  # automatic validation with Query
    offset: int = Query(0, ge=0),
):
    data = get_books()  # modified by subsequent filters

    # Filters
    if author:
        data = data[data["author"].str.contains(author, case=False, na=False)]

    if category:
        data = data[data["category"].str.lower() == category.lower()]

    if status:
        data = data[data["status"].str.lower() == status.lower()]

    if language:
        data = data[data["language"].str.lower() == language.lower()]

    # Pagination
    data = data.iloc[offset : offset + limit]

    # Replace NaN for None to avoid schema mismatches
    data = clean_for_json(data)

    return data.to_dict(
        orient="records"
    )  # if data is empty, return it instead of 404 error
