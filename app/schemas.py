from pydantic import BaseModel
from datetime import date
from typing import Optional

# Only the attributes listed will be returned as response (no need to filter)
class Book(BaseModel):
    book_name: str
    author: str
    total_pages: int
    start_date: date
    end_date: Optional[date] = None  # in case a book is still being read
    language: str
    category: str
    country_origin: str
    status: str
    score: Optional[float] = None  # dropped or unfinished books have no score

# Schema for the reading speed metric
class AuthorStats(BaseModel):
    author_name: str
    avg_reading_speed_days: float
    unit: str = "days_per_book"
    book_count: int

# Schema for global stats
class GlobalStats(BaseModel):
    book_count: int
    completed_book_count: int
    avg_reading_speed_days: float
    avg_pages_per_day: float