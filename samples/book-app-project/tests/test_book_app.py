import os
import sys
from contextlib import redirect_stdout
from io import StringIO

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import book_app
from books import Book


def test_stat_command_displays_collection_statistics(monkeypatch) -> None:
    books = [
        Book("Book B", "Author B", 1950),
        Book("Book A", "Author A", 1900, read=True),
        Book("Book C", "Author C", 2000, read=True),
    ]
    monkeypatch.setattr(book_app.collection, "list_books", lambda: books)
    monkeypatch.setattr(sys, "argv", ["book_app.py", "stat"])
    output = StringIO()

    with redirect_stdout(output):
        book_app.main()

    assert "Total books: 3" in output.getvalue()
    assert "Read: 2" in output.getvalue()
    assert "Unread: 1" in output.getvalue()
    assert "Oldest book: Book A by Author A (1900)" in output.getvalue()
    assert "Newest book: Book C by Author C (2000)" in output.getvalue()


def test_stat_command_displays_empty_collection(monkeypatch) -> None:
    monkeypatch.setattr(book_app.collection, "list_books", lambda: [])
    monkeypatch.setattr(sys, "argv", ["book_app.py", "stat"])
    output = StringIO()

    with redirect_stdout(output):
        book_app.main()

    assert "Total books: 0" in output.getvalue()
    assert "Read: 0" in output.getvalue()
    assert "Unread: 0" in output.getvalue()
    assert "Oldest book: None" in output.getvalue()
    assert "Newest book: None" in output.getvalue()


def test_help_lists_stat_command(monkeypatch) -> None:
    monkeypatch.setattr(sys, "argv", ["book_app.py", "help"])
    output = StringIO()

    with redirect_stdout(output):
        book_app.main()

    assert "stat     - Show collection statistics" in output.getvalue()
