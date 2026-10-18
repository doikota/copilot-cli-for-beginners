import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import books
from books import Book, get_book_statistics


def test_data_file_path_is_relative_to_books_module(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)

    assert books.DATA_FILE == Path(books.__file__).resolve().parent / "data.json"


def test_get_book_statistics() -> None:
    oldest_book = Book("Book A", "Author A", 1900, read=True)
    middle_book = Book("Book B", "Author B", 1950)
    newest_book = Book("Book C", "Author C", 2000, read=True)

    result = get_book_statistics([middle_book, oldest_book, newest_book])

    assert result == {
        "total": 3,
        "read": 2,
        "unread": 1,
        "oldest_book": oldest_book,
        "newest_book": newest_book,
    }


def test_get_book_statistics_empty_list() -> None:
    result = get_book_statistics([])

    assert result == {
        "total": 0,
        "read": 0,
        "unread": 0,
        "oldest_book": None,
        "newest_book": None,
    }
