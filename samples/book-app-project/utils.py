from books import Book


def print_menu() -> None:
    print("\n📚 Book Collection App")
    print("1. Add a book")
    print("2. List books")
    print("3. Mark book as read")
    print("4. Remove a book")
    print("5. Exit")


def get_user_choice() -> str:
    while True:
        choice = input("Choose an option (1-5): ").strip()
        try:
            numeric_choice = int(choice)
        except ValueError:
            print("Invalid choice. Please choose an option from 1 to 5.")
            continue

        if 1 <= numeric_choice <= 5:
            return str(numeric_choice)

        print("Invalid choice. Please choose an option from 1 to 5.")


def get_book_details() -> tuple[str, str, int]:
    title = input("Enter book title: ").strip()
    author = input("Enter author: ").strip()

    year_input = input("Enter publication year: ").strip()
    try:
        year = int(year_input)
    except ValueError as error:
        raise ValueError("Publication year must be an integer.") from error

    return title, author, year


def print_books(books: list[Book]) -> None:
    if not books:
        print("No books in your collection.")
        return

    print("\nYour Books:")
    for index, book in enumerate(books, start=1):
        status = "✅ Read" if book.read else "📖 Unread"
        print(f"{index}. {book.title} by {book.author} ({book.year}) - {status}")
