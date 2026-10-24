import sys

import questionary

from books import Book, BookCollection, get_book_statistics


def show_books(books: list[Book]) -> None:
    """Display books in a user-friendly format."""
    if not books:
        print("No books found.")
        return

    print("\nYour Book Collection:\n")

    for index, book in enumerate(books, start=1):
        status = "✓" if book.read else " "
        print(f"{index}. [{status}] {book.title} by {book.author} ({book.year})")
        rating = f"{book.rating}/5" if book.rating is not None else "Not rated"
        review = book.review if book.review else "No review"
        print(f"   Rating: {rating}")
        print(f"   Review: {review}")

    print()


def handle_list(collection: BookCollection) -> None:
    books = collection.list_books()
    show_books(books)


def handle_add(collection: BookCollection) -> None:
    print("\nAdd a New Book\n")

    title = input("Title: ").strip()
    author = input("Author: ").strip()
    year_str = input("Year: ").strip()

    try:
        year = int(year_str)
    except ValueError:
        print("\nError: Publication year must be an integer.\n")
        return

    try:
        collection.add_book(title, author, year)
        print("\nBook added successfully.\n")
    except ValueError as error:
        print(f"\nError: {error}\n")


def handle_remove(collection: BookCollection) -> None:
    print("\nRemove a Book\n")

    title = input("Enter the title of the book to remove: ").strip()
    collection.remove_book(title)

    print("\nBook removed if it existed.\n")


def handle_find(collection: BookCollection) -> None:
    print("\nFind Books by Author\n")

    author = input("Author name: ").strip()
    books = collection.find_by_author(author)

    show_books(books)


def handle_stat(collection: BookCollection) -> None:
    statistics = get_book_statistics(collection.list_books())
    print("\nBook Collection Statistics\n")
    print(f"Total books: {statistics['total']}")
    print(f"Read: {statistics['read']}")
    print(f"Unread: {statistics['unread']}")

    for label, key in (("Oldest", "oldest_book"), ("Newest", "newest_book")):
        book = statistics[key]
        if book is None:
            print(f"{label} book: None")
        else:
            print(f"{label} book: {book.title} by {book.author} ({book.year})")

    print()


def handle_review(collection: BookCollection) -> None:
    print("\nRate and Review a Book\n")

    books = collection.list_books()
    if not books:
        print("\nNo books found. Add a book before writing a review.\n")
        return

    book_by_id = {book.id: book for book in books}
    selected_id: str | None = questionary.select(
        "Select a book to review:",
        choices=[
            questionary.Choice(
                f"{book.title} — {book.author} ({book.year})",
                value=book.id,
            )
            for book in books
        ],
        style=questionary.Style([("highlighted", "reverse")]),
        use_arrow_keys=True,
    ).ask()
    if selected_id is None:
        print("\nReview cancelled.\n")
        return

    book = book_by_id.get(selected_id)
    if book is None:
        print("\nSelected book could not be found. Please try again.\n")
        return

    rating_input = input(
        "Rating (1-5, blank to keep, 0 to clear): "
    ).strip()
    if rating_input == "":
        rating = book.rating
    elif rating_input == "0":
        rating = None
    else:
        try:
            rating = int(rating_input)
        except ValueError:
            print("\nError: rating must be an integer from 1 to 5.\n")
            return

    review_input = input("Review (blank to keep, !clear to clear): ").strip()
    if review_input == "":
        review = book.review
    elif review_input == "!clear":
        review = None
    else:
        review = review_input

    try:
        collection.set_rating_and_review_by_id(book.id, rating, review)
        print("\nRating and review saved.\n")
    except ValueError as error:
        print(f"\nError: {error}\n")


def show_help() -> None:
    print("""
Book Collection Helper

Commands:
  list     - Show all books
  add      - Add a new book
  remove   - Remove a book by title
  find     - Find books by author
  stat     - Show collection statistics
  review   - Add or update a book rating and review
  help     - Show this help message
""")


def main() -> int:
    if len(sys.argv) < 2:
        show_help()
        return 0

    command = sys.argv[1].lower()

    if command == "help":
        show_help()
        return 0

    handlers = {
        "list": handle_list,
        "add": handle_add,
        "remove": handle_remove,
        "find": handle_find,
        "stat": handle_stat,
        "review": handle_review,
    }
    handler = handlers.get(command)
    if handler is None:
        print("Unknown command.\n")
        show_help()
        return 0

    try:
        collection = BookCollection()
    except (OSError, ValueError) as error:
        print(f"Error: Could not load book collection: {error}", file=sys.stderr)
        return 1

    handler(collection)
    return 0


if __name__ == "__main__":
    sys.exit(main())
