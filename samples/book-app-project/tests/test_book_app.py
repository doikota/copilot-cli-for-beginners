import os
import sys
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

import questionary
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import book_app
import books
from books import Book, BookCollection


@pytest.fixture
def collection(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> BookCollection:
    monkeypatch.setattr(books, "DATA_FILE", tmp_path / "data.json")
    return BookCollection()


def test_stat_command_displays_collection_statistics(
    monkeypatch: pytest.MonkeyPatch, collection: BookCollection
) -> None:
    books = [
        Book("Book B", "Author B", 1950),
        Book("Book A", "Author A", 1900, read=True),
        Book("Book C", "Author C", 2000, read=True),
    ]
    monkeypatch.setattr(collection, "list_books", lambda: books)
    monkeypatch.setattr(book_app, "BookCollection", lambda: collection)
    monkeypatch.setattr(sys, "argv", ["book_app.py", "stat"])
    output = StringIO()

    with redirect_stdout(output):
        book_app.main()

    assert "Total books: 3" in output.getvalue()
    assert "Read: 2" in output.getvalue()
    assert "Unread: 1" in output.getvalue()
    assert "Oldest book: Book A by Author A (1900)" in output.getvalue()
    assert "Newest book: Book C by Author C (2000)" in output.getvalue()


def test_stat_command_displays_empty_collection(
    monkeypatch: pytest.MonkeyPatch, collection: BookCollection
) -> None:
    monkeypatch.setattr(collection, "list_books", lambda: [])
    monkeypatch.setattr(book_app, "BookCollection", lambda: collection)
    monkeypatch.setattr(sys, "argv", ["book_app.py", "stat"])
    output = StringIO()

    with redirect_stdout(output):
        book_app.main()

    assert "Total books: 0" in output.getvalue()
    assert "Read: 0" in output.getvalue()
    assert "Unread: 0" in output.getvalue()
    assert "Oldest book: None" in output.getvalue()
    assert "Newest book: None" in output.getvalue()


def test_help_lists_stat_command(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(sys, "argv", ["book_app.py", "help"])
    output = StringIO()

    with redirect_stdout(output):
        book_app.main()

    assert "stat     - Show collection statistics" in output.getvalue()


def test_help_does_not_load_book_collection(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr(books, "DATA_FILE", tmp_path / "invalid.json")
    books.DATA_FILE.write_text("{invalid", encoding="utf-8")
    monkeypatch.setattr(sys, "argv", ["book_app.py", "help"])

    def fail_to_load() -> BookCollection:
        raise AssertionError("Collection should not load")

    monkeypatch.setattr(book_app, "BookCollection", fail_to_load)

    assert book_app.main() == 0
    assert "Commands:" in capsys.readouterr().out


def test_main_reports_invalid_data_and_returns_error(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr(books, "DATA_FILE", tmp_path / "invalid.json")
    books.DATA_FILE.write_text("{invalid", encoding="utf-8")
    monkeypatch.setattr(sys, "argv", ["book_app.py", "list"])

    assert book_app.main() == 1
    assert "Could not load book collection" in capsys.readouterr().err


@pytest.mark.parametrize(
    "error", [OSError("permission denied"), ValueError("invalid data")]
)
def test_main_reports_collection_initialization_errors(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    error: OSError | ValueError,
) -> None:
    def fail_to_load() -> BookCollection:
        raise error

    monkeypatch.setattr(book_app, "BookCollection", fail_to_load)
    monkeypatch.setattr(sys, "argv", ["book_app.py", "list"])

    assert book_app.main() == 1
    assert str(error) in capsys.readouterr().err


def test_review_command_updates_rating_and_review(
    monkeypatch: pytest.MonkeyPatch, collection: BookCollection
) -> None:
    book = Book("Dune", "Frank Herbert", 1965, rating=3, review="Old review")
    saved_values = []
    monkeypatch.setattr(collection, "list_books", lambda: [book])
    monkeypatch.setattr(
        collection,
        "set_rating_and_review_by_id",
        lambda book_id, rating, review: saved_values.append(
            (book_id, rating, review)
        )
        or True,
    )
    monkeypatch.setattr(
        book_app.questionary,
        "select",
        lambda *args, **kwargs: type("Prompt", (), {"ask": lambda self: book.id})(),
    )
    answers = iter(["5", "A memorable adventure."])
    monkeypatch.setattr("builtins.input", lambda prompt: next(answers))
    output = StringIO()

    with redirect_stdout(output):
        book_app.handle_review(collection)

    assert saved_values == [(book.id, 5, "A memorable adventure.")]
    assert "Rating and review saved." in output.getvalue()


def test_review_command_keeps_existing_values_when_prompts_are_blank(
    monkeypatch: pytest.MonkeyPatch, collection: BookCollection
) -> None:
    book = Book("Dune", "Frank Herbert", 1965, rating=3, review="Existing review")
    saved_values = []
    monkeypatch.setattr(collection, "list_books", lambda: [book])
    monkeypatch.setattr(
        collection,
        "set_rating_and_review_by_id",
        lambda book_id, rating, review: saved_values.append(
            (book_id, rating, review)
        )
        or True,
    )
    monkeypatch.setattr(
        book_app.questionary,
        "select",
        lambda *args, **kwargs: type("Prompt", (), {"ask": lambda self: book.id})(),
    )
    answers = iter(["", ""])
    monkeypatch.setattr("builtins.input", lambda prompt: next(answers))

    book_app.handle_review(collection)

    assert saved_values == [(book.id, 3, "Existing review")]


def test_review_command_clears_rating_and_review(
    monkeypatch: pytest.MonkeyPatch, collection: BookCollection
) -> None:
    book = Book("Dune", "Frank Herbert", 1965, rating=3, review="Existing review")
    saved_values = []
    monkeypatch.setattr(collection, "list_books", lambda: [book])
    monkeypatch.setattr(
        collection,
        "set_rating_and_review_by_id",
        lambda book_id, rating, review: saved_values.append(
            (book_id, rating, review)
        )
        or True,
    )
    monkeypatch.setattr(
        book_app.questionary,
        "select",
        lambda *args, **kwargs: type("Prompt", (), {"ask": lambda self: book.id})(),
    )
    answers = iter(["0", "!clear"])
    monkeypatch.setattr("builtins.input", lambda prompt: next(answers))

    book_app.handle_review(collection)

    assert saved_values == [(book.id, None, None)]


def test_review_command_cancels_when_selection_is_cancelled(
    monkeypatch: pytest.MonkeyPatch, collection: BookCollection
) -> None:
    monkeypatch.setattr(
        collection, "list_books", lambda: [Book("Dune", "Frank Herbert", 1965)]
    )
    monkeypatch.setattr(
        book_app.questionary,
        "select",
        lambda *args, **kwargs: type("Prompt", (), {"ask": lambda self: None})(),
    )
    output = StringIO()

    with redirect_stdout(output):
        book_app.handle_review(collection)

    assert "Review cancelled." in output.getvalue()


def test_review_command_handles_empty_collection(
    monkeypatch: pytest.MonkeyPatch, collection: BookCollection
) -> None:
    monkeypatch.setattr(collection, "list_books", lambda: [])
    output = StringIO()

    with redirect_stdout(output):
        book_app.handle_review(collection)

    assert "Add a book before writing a review." in output.getvalue()


def test_review_command_configures_highlighted_arrow_key_choices(
    monkeypatch: pytest.MonkeyPatch, collection: BookCollection
) -> None:
    books = [
        Book("Dune", "Frank Herbert", 1965),
        Book("Dune", "Another Author", 2020),
    ]
    selected_book = books[1]
    saved_ids: list[str] = []
    captured: dict[str, object] = {}
    monkeypatch.setattr(collection, "list_books", lambda: books)

    class Prompt:
        def ask(self) -> str:
            return selected_book.id

    def select_book(
        message: str, choices: list[questionary.Choice], **kwargs: object
    ) -> Prompt:
        captured["message"] = message
        captured["choices"] = choices
        captured["style"] = kwargs["style"]
        captured["use_arrow_keys"] = kwargs["use_arrow_keys"]
        return Prompt()

    monkeypatch.setattr(book_app.questionary, "select", select_book)
    monkeypatch.setattr(
        collection,
        "set_rating_and_review_by_id",
        lambda book_id, rating, review: saved_ids.append(book_id) or True,
    )
    monkeypatch.setattr("builtins.input", lambda prompt: "")

    book_app.handle_review(collection)

    choices = captured["choices"]
    assert isinstance(choices, list)
    assert [(choice.title, choice.value) for choice in choices] == [
        ("Dune — Frank Herbert (1965)", books[0].id),
        ("Dune — Another Author (2020)", books[1].id),
    ]
    assert captured["style"].style_rules == [("highlighted", "reverse")]
    assert captured["use_arrow_keys"] is True
    assert saved_ids == [selected_book.id]


def test_show_books_displays_rating_and_review() -> None:
    output = StringIO()

    with redirect_stdout(output):
        book_app.show_books(
            [Book("Dune", "Frank Herbert", 1965, rating=5, review="Excellent")]
        )

    assert "Rating: 5/5" in output.getvalue()
    assert "Review: Excellent" in output.getvalue()
