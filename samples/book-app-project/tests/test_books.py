import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import books
from books import Book, BookCollection, get_book_statistics


@pytest.fixture(autouse=True)
def use_temp_data_file(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Use a temporary data file for each test."""
    temp_file = tmp_path / "data.json"
    temp_file.write_text("[]", encoding="utf-8")
    monkeypatch.setattr(books, "DATA_FILE", str(temp_file))


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
        '[{"title": 1, "author": "Author", "year": 2000}]',
        '[{"title": "Book", "author": 1, "year": 2000}]',
        '[{"title": "Book", "author": "Author", "year": 2000, "rating": true}]',
        '[{"title": "Bad review", "author": "Author", "year": 2000, "review": 5}]',
        '[{"title": "Book", "author": "Author", "year": 2000, "id": " "}]',
        '[{"title": "Book", "author": "Author", "year": 2000, "unknown": true}]',
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


def test_load_books_uses_empty_collection_when_data_file_is_missing() -> None:
    Path(books.DATA_FILE).unlink()

    collection = BookCollection()

    assert collection.list_books() == []


def test_load_books_rejects_malformed_json() -> None:
    Path(books.DATA_FILE).write_text("{invalid json", encoding="utf-8")

    with pytest.raises(ValueError, match="Cannot load books from data.json"):
        BookCollection()


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


def test_mark_as_read_matches_title_without_case_sensitivity() -> None:
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)

    assert collection.mark_as_read("dUnE") is True

    reloaded_collection = BookCollection()
    book = reloaded_collection.find_book_by_title("Dune")
    assert book is not None
    assert book.read is True


@pytest.mark.parametrize("author_query", ["frank herbert", "FRANK HERBERT"])
def test_find_by_author_matches_without_case_sensitivity(
    author_query: str,
) -> None:
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)

    result = collection.find_by_author(author_query)

    assert [book.title for book in result] == ["Dune"]


def test_find_by_author_returns_empty_list_for_no_match() -> None:
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)

    assert collection.find_by_author("Ursula Le Guin") == []


def test_find_by_author_returns_empty_list_for_empty_collection() -> None:
    collection = BookCollection()

    assert collection.find_by_author("") == []


def test_remove_book_matches_title_without_case_sensitivity_and_persists() -> None:
    collection = BookCollection()
    collection.add_book("The Hobbit", "J.R.R. Tolkien", 1937)

    assert collection.remove_book("the hobbit") is True

    reloaded_collection = BookCollection()
    assert reloaded_collection.list_books() == []
