import os
import sys
from contextlib import redirect_stdout
from io import StringIO

import pytest

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


def test_review_command_updates_rating_and_review(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    book = Book("Dune", "Frank Herbert", 1965, rating=3, review="Old review")
    saved_values = []
    monkeypatch.setattr(
        book_app.collection, "find_book_by_title", lambda title: book
    )
    monkeypatch.setattr(
        book_app.collection,
        "set_rating_and_review",
        lambda title, rating, review: saved_values.append((rating, review)) or True,
    )
    answers = iter(["Dune", "5", "A memorable adventure."])
    monkeypatch.setattr("builtins.input", lambda prompt: next(answers))
    output = StringIO()

    with redirect_stdout(output):
        book_app.handle_review()

    assert saved_values == [(5, "A memorable adventure.")]
    assert "Rating and review saved." in output.getvalue()


def test_review_command_keeps_existing_values_when_prompts_are_blank(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    book = Book("Dune", "Frank Herbert", 1965, rating=3, review="Existing review")
    saved_values = []
    monkeypatch.setattr(
        book_app.collection, "find_book_by_title", lambda title: book
    )
    monkeypatch.setattr(
        book_app.collection,
        "set_rating_and_review",
        lambda title, rating, review: saved_values.append((rating, review)) or True,
    )
    answers = iter(["Dune", "", ""])
    monkeypatch.setattr("builtins.input", lambda prompt: next(answers))

    book_app.handle_review()

    assert saved_values == [(3, "Existing review")]


def test_review_command_clears_rating_and_review(monkeypatch: pytest.MonkeyPatch) -> None:
    book = Book("Dune", "Frank Herbert", 1965, rating=3, review="Existing review")
    saved_values = []
    monkeypatch.setattr(
        book_app.collection, "find_book_by_title", lambda title: book
    )
    monkeypatch.setattr(
        book_app.collection,
        "set_rating_and_review",
        lambda title, rating, review: saved_values.append((rating, review)) or True,
    )
    answers = iter(["Dune", "0", "!clear"])
    monkeypatch.setattr("builtins.input", lambda prompt: next(answers))

    book_app.handle_review()

    assert saved_values == [(None, None)]


def test_review_command_reports_unknown_book(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(book_app.collection, "find_book_by_title", lambda title: None)
    monkeypatch.setattr("builtins.input", lambda prompt: "Unknown")
    output = StringIO()

    with redirect_stdout(output):
        book_app.handle_review()

    assert "Book not found." in output.getvalue()


def test_show_books_displays_rating_and_review() -> None:
    output = StringIO()

    with redirect_stdout(output):
        book_app.show_books(
            [Book("Dune", "Frank Herbert", 1965, rating=5, review="Excellent")]
        )

    assert "Rating: 5/5" in output.getvalue()
    assert "Review: Excellent" in output.getvalue()
