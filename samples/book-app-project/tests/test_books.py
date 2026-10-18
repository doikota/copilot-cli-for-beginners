import sys
import os
from pathlib import Path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import books
from books import BookCollection


@pytest.fixture(autouse=True)
def use_temp_data_file(tmp_path, monkeypatch):
    """Use a temporary data file for each test."""
    temp_file = tmp_path / "data.json"
    temp_file.write_text("[]")
    monkeypatch.setattr(books, "DATA_FILE", str(temp_file))


def test_add_book():
    collection = BookCollection()
    initial_count = len(collection.books)
    collection.add_book("1984", "George Orwell", 1949)
    assert len(collection.books) == initial_count + 1
    book = collection.find_book_by_title("1984")
    assert book is not None
    assert book.author == "George Orwell"
    assert book.year == 1949
    assert book.read is False


def test_list_books_returns_independent_copies() -> None:
    collection = BookCollection()
    collection.add_book("1984", "George Orwell", 1949)

    listed_books = collection.list_books()
    listed_books[0].title = "Changed title"
    listed_books[0].read = True
    listed_books.append(books.Book("Dune", "Frank Herbert", 1965))

    stored_book = collection.find_book_by_title("1984")
    assert stored_book is not None
    assert stored_book.title == "1984"
    assert stored_book.read is False
    assert len(collection.list_books()) == 1


def test_save_and_load_japanese_book_names() -> None:
    collection = BookCollection()
    collection.add_book("吾輩は猫である", "夏目漱石", 1905)

    saved_json = Path(books.DATA_FILE).read_text(encoding="utf-8")
    assert "吾輩は猫である" in saved_json
    assert "夏目漱石" in saved_json
    assert "\\u" not in saved_json

    reloaded_collection = BookCollection()
    book = reloaded_collection.find_book_by_title("吾輩は猫である")
    assert book is not None
    assert book.author == "夏目漱石"


@pytest.mark.parametrize(
    "invalid_data",
    [
        '{"title": "not a list"}',
        '[null]',
        '[{"title": "Missing year", "author": "Author"}]',
        '[{"title": "Bad year", "author": "Author", "year": true}]',
        '[{"title": "Bad status", "author": "Author", "year": 2000, "read": "yes"}]',
        '[{"title": "Bad rating", "author": "Author", "year": 2000, "rating": 6}]',
        '[{"title": "Bad review", "author": "Author", "year": 2000, "review": 5}]',
    ],
)
def test_load_invalid_book_data_raises_and_preserves_file(
    invalid_data: str,
) -> None:
    Path(books.DATA_FILE).write_text(invalid_data, encoding="utf-8")

    with pytest.raises(ValueError, match="Cannot load books from data.json"):
        BookCollection()

    assert Path(books.DATA_FILE).read_text(encoding="utf-8") == invalid_data


def test_legacy_book_data_loads_without_rating_or_review() -> None:
    Path(books.DATA_FILE).write_text(
        '[{"title": "1984", "author": "George Orwell", "year": 1949}]',
        encoding="utf-8",
    )

    collection = BookCollection()
    book = collection.find_book_by_title("1984")

    assert book is not None
    assert book.rating is None
    assert book.review is None
    assert book.id


def test_set_rating_and_review_persists_values() -> None:
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)

    book = collection.find_book_by_title("Dune")
    assert book is not None
    assert collection.set_rating_and_review("Dune", 5, "A memorable adventure.")

    saved_collection = BookCollection()
    book = saved_collection.find_book_by_title("Dune")
    assert book is not None
    assert book.rating == 5
    assert book.review == "A memorable adventure."
    original_book = collection.find_book_by_title("Dune")
    assert original_book is not None
    assert book.id == original_book.id


@pytest.mark.parametrize("rating", [0, 6, -1, 1.5, True, "3"])
def test_set_rating_and_review_rejects_invalid_ratings(rating: object) -> None:
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)

    with pytest.raises(ValueError, match="Rating must be an integer"):
        collection.set_rating_and_review("Dune", rating, None)  # type: ignore[arg-type]


def test_set_rating_and_review_rejects_non_string_review() -> None:
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)

    with pytest.raises(ValueError, match="Review must be a string"):
        collection.set_rating_and_review("Dune", None, 123)  # type: ignore[arg-type]


def test_set_rating_and_review_returns_false_for_unknown_title() -> None:
    collection = BookCollection()

    assert not collection.set_rating_and_review("Unknown", 4, "Review")


def test_set_rating_and_review_by_id_returns_false_for_unknown_id() -> None:
    collection = BookCollection()

    assert not collection.set_rating_and_review_by_id(
        "unknown-id", 4, "Review"
    )


def test_set_rating_and_review_updates_the_selected_duplicate_title() -> None:
    collection = BookCollection()
    first_book = collection.add_book("Dune", "Frank Herbert", 1965)
    second_book = collection.add_book("Dune", "Another Author", 2020)

    assert collection.set_rating_and_review_by_id(
        second_book.id, 5, "Selected review."
    )

    assert first_book.review is None
    assert second_book.review == "Selected review."


def test_mark_book_as_read():
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)
    result = collection.mark_as_read("Dune")
    assert result is True
    book = collection.find_book_by_title("Dune")
    assert book.read is True

def test_mark_book_as_read_invalid():
    collection = BookCollection()
    result = collection.mark_as_read("Nonexistent Book")
    assert result is False

def test_remove_book():
    collection = BookCollection()
    collection.add_book("The Hobbit", "J.R.R. Tolkien", 1937)
    result = collection.remove_book("The Hobbit")
    assert result is True
    book = collection.find_book_by_title("The Hobbit")
    assert book is None

def test_remove_book_invalid():
    collection = BookCollection()
    result = collection.remove_book("Nonexistent Book")
    assert result is False
