"""Interactive book collection app that uses the helpers in utils.py."""

from books import BookCollection
from utils import get_book_details, get_user_choice, print_books, print_menu


def add_book(collection: BookCollection) -> None:
    try:
        title, author, year = get_book_details()
        if not title or not author:
            print("Title and author are required.")
            return

        collection.add_book(title, author, year)
    except ValueError as error:
        print(f"Invalid book details: {error}")
        return

    print("Book added successfully.")


def mark_book_as_read(collection: BookCollection) -> None:
    title = input("Enter the title of the book to mark as read: ").strip()
    if not title:
        print("Book title is required.")
    elif collection.mark_as_read(title):
        print("Book marked as read.")
    else:
        print("Book not found.")


def remove_book(collection: BookCollection) -> None:
    title = input("Enter the title of the book to remove: ").strip()
    if not title:
        print("Book title is required.")
    elif collection.remove_book(title):
        print("Book removed.")
    else:
        print("Book not found.")


def main() -> None:
    collection = BookCollection()

    while True:
        print_menu()
        choice = get_user_choice()

        if choice == "1":
            add_book(collection)
        elif choice == "2":
            print_books(collection.list_books())
        elif choice == "3":
            mark_book_as_read(collection)
        elif choice == "4":
            remove_book(collection)
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please choose an option from 1 to 5.")


if __name__ == "__main__":
    main()
