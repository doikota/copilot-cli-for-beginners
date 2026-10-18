import json
from dataclasses import dataclass, asdict, replace
from pathlib import Path
from typing import List, Optional

DATA_FILE = Path(__file__).resolve().parent / "data.json"


@dataclass
class Book:
    title: str
    author: str
    year: int
    read: bool = False


def get_book_statistics(books: List[Book]) -> dict[str, int | Book | None]:
    """Return counts and the oldest and newest books in the collection."""
    read_count = sum(book.read for book in books)
    return {
        "total": len(books),
        "read": read_count,
        "unread": len(books) - read_count,
        "oldest_book": min(books, key=lambda book: book.year, default=None),
        "newest_book": max(books, key=lambda book: book.year, default=None),
    }


def _book_from_data(data: object, index: int) -> Book:
    if not isinstance(data, dict):
        raise ValueError(f"Book at index {index} must be an object.")

    required_fields = {"title", "author", "year"}
    missing_fields = required_fields - data.keys()
    if missing_fields:
        raise ValueError(
            f"Book at index {index} is missing: {', '.join(sorted(missing_fields))}."
        )

    unexpected_fields = data.keys() - required_fields - {"read"}
    if unexpected_fields:
        raise ValueError(
            f"Book at index {index} has unexpected fields: "
            f"{', '.join(sorted(unexpected_fields))}."
        )

    title = data["title"]
    author = data["author"]
    year = data["year"]
    read = data.get("read", False)
    if not isinstance(title, str):
        raise ValueError(f"Book at index {index} has a non-string title.")
    if not isinstance(author, str):
        raise ValueError(f"Book at index {index} has a non-string author.")
    if not isinstance(year, int) or isinstance(year, bool):
        raise ValueError(f"Book at index {index} has a non-integer year.")
    if not isinstance(read, bool):
        raise ValueError(f"Book at index {index} has a non-boolean read status.")

    return Book(title=title, author=author, year=year, read=read)


class BookCollection:
    def __init__(self) -> None:
        self.books: List[Book] = []
        self.load_books()

    def load_books(self) -> None:
        """Load books from the JSON file if it exists."""
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            if not isinstance(data, list):
                raise ValueError("The collection must be a list.")
            self.books = [
                _book_from_data(book_data, index)
                for index, book_data in enumerate(data)
            ]
        except FileNotFoundError:
            self.books = []
        except ValueError as error:
            raise ValueError(f"Cannot load books from data.json: {error}") from error

    def save_books(self) -> None:
        """Save the current book collection to JSON."""
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump([asdict(b) for b in self.books], f, indent=2, ensure_ascii=False)

    def add_book(self, title: str, author: str, year: int) -> Book:
        book = Book(title=title, author=author, year=year)
        self.books.append(book)
        self.save_books()
        return book

    def list_books(self) -> List[Book]:
        return [replace(book) for book in self.books]

    def find_book_by_title(self, title: str) -> Optional[Book]:
        for book in self.books:
            if book.title.lower() == title.lower():
                return book
        return None

    def mark_as_read(self, title: str) -> bool:
        book = self.find_book_by_title(title)
        if book:
            book.read = True
            self.save_books()
            return True
        return False

    def remove_book(self, title: str) -> bool:
        """Remove a book by title."""
        book = self.find_book_by_title(title)
        if book:
            self.books.remove(book)
            self.save_books()
            return True
        return False

    def find_by_author(self, author: str) -> List[Book]:
        """Find all books by a given author."""
        return [b for b in self.books if b.author.lower() == author.lower()]
