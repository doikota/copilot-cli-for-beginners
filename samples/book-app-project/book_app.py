import sys
from books import Book, BookCollection, get_book_statistics


# Global collection instance
collection = BookCollection()


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


def handle_list() -> None:
    books = collection.list_books()
    show_books(books)


def handle_add() -> None:
    print("\nAdd a New Book\n")

    title = input("Title: ").strip()
    author = input("Author: ").strip()
    year_str = input("Year: ").strip()

    try:
        year = int(year_str) if year_str else 0
        collection.add_book(title, author, year)
        print("\nBook added successfully.\n")
    except ValueError as e:
        print(f"\nError: {e}\n")


def handle_remove() -> None:
    print("\nRemove a Book\n")

    title = input("Enter the title of the book to remove: ").strip()
    collection.remove_book(title)

    print("\nBook removed if it existed.\n")


def handle_find() -> None:
    print("\nFind Books by Author\n")

    author = input("Author name: ").strip()
    books = collection.find_by_author(author)

    show_books(books)


def handle_stat() -> None:
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


def handle_review() -> None:
    print("\nRate and Review a Book\n")

    title = input("Book title: ").strip()
    book = collection.find_book_by_title(title)
    if book is None:
        print("\nBook not found.\n")
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
        collection.set_rating_and_review(title, rating, review)
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


def main() -> None:
    if len(sys.argv) < 2:
        show_help()
        return

    command = sys.argv[1].lower()

    if command == "list":
        handle_list()
    elif command == "add":
        handle_add()
    elif command == "remove":
        handle_remove()
    elif command == "find":
        handle_find()
    elif command == "stat":
        handle_stat()
    elif command == "review":
        handle_review()
    elif command == "help":
        show_help()
    else:
        print("Unknown command.\n")
        show_help()


if __name__ == "__main__":
    main()
