import os
import sys
from contextlib import redirect_stdout
from datetime import date
from io import StringIO
from pathlib import Path

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import books
import utils_app


def test_main_runs_book_collection_workflow(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(books, "DATA_FILE", tmp_path / "data.json")
    answers = iter(
        [
            "1",
            "Dune",
            "Frank Herbert",
            "1965",
            "2",
            "3",
            "Dune",
            "2",
            "4",
            "Dune",
            "2",
            "5",
        ]
    )
    monkeypatch.setattr("builtins.input", lambda _prompt: next(answers))
    output = StringIO()

    with redirect_stdout(output):
        utils_app.main()

    displayed = output.getvalue()
    assert "Book added successfully." in displayed
    assert "Dune by Frank Herbert (1965) - 📖 Unread" in displayed
    assert "Dune by Frank Herbert (1965) - ✅ Read" in displayed
    assert "Book marked as read." in displayed
    assert "Book removed." in displayed
    assert "No books in your collection." in displayed
    assert "Goodbye!" in displayed


def test_main_handles_invalid_choice_and_empty_book_details(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(books, "DATA_FILE", tmp_path / "data.json")
    answers = iter(["invalid", "1", "", "Frank Herbert", "1965", "5"])
    monkeypatch.setattr("builtins.input", lambda _prompt: next(answers))
    output = StringIO()

    with redirect_stdout(output):
        utils_app.main()

    displayed = output.getvalue()
    assert "Invalid choice. Please choose an option from 1 to 5." in displayed
    assert "Title and author are required." in displayed
    assert not (tmp_path / "data.json").exists()


@pytest.mark.parametrize(
    "year_input",
    ["not-a-year", "0", "-1", str(date.today().year + 1)],
)
def test_main_rejects_invalid_publication_year(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    year_input: str,
) -> None:
    monkeypatch.setattr(books, "DATA_FILE", tmp_path / "data.json")
    answers = iter(["1", "Dune", "Frank Herbert", year_input, "5"])
    monkeypatch.setattr("builtins.input", lambda _prompt: next(answers))
    output = StringIO()

    with redirect_stdout(output):
        utils_app.main()

    displayed = output.getvalue()
    assert "Invalid book details:" in displayed
    assert "Book added successfully." not in displayed
    assert not (tmp_path / "data.json").exists()


def test_main_reprompts_for_empty_and_nonnumeric_choices(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(books, "DATA_FILE", tmp_path / "data.json")
    answers = iter(["", "not-a-number", "5"])
    monkeypatch.setattr("builtins.input", lambda _prompt: next(answers))
    output = StringIO()

    with redirect_stdout(output):
        utils_app.main()

    displayed = output.getvalue()
    assert displayed.count(
        "Invalid choice. Please choose an option from 1 to 5."
    ) == 2
    assert "Goodbye!" in displayed
