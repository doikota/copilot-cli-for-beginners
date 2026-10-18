# Book Collection App

*(This README is intentionally rough so you can improve it with GitHub Copilot CLI)*

A Python app for managing books you have or want to read.
It can add, remove, and list books, mark them as read, and save a rating and review.

---

## Current Features

* Reads books from a JSON file (our database)
* Stores an optional 1-to-5 rating and one review for each book
* Use the `review` command to add or update a rating and review
* Input checking is weak in some areas
* Some tests exist but probably not enough

---

## Files

* `book_app.py` - Main CLI entry point
* `utils_app.py` - Interactive app using the helpers in `utils.py`
* `books.py` - BookCollection class with data logic
* `utils.py` - Helper functions for UI and input
* `data.json` - Sample book data
* `tests/test_books.py` - Starter pytest tests

---

## Running the App

Install the project and its dependencies:

```bash
python -m pip install -e .
```

```bash
python book_app.py list
python book_app.py add
python book_app.py find
python book_app.py remove
python book_app.py review
python book_app.py help
```

To run the menu-based app that uses `utils.py`:

```bash
python utils_app.py
```

When reviewing a book, use the up and down arrow keys to highlight a book, then
press Enter to select it. Enter a rating from 1 to 5. Leave a prompt blank to
keep its current value; enter `0` to clear the rating or `!clear` to clear the
review.

## Running Tests

```bash
python -m pytest tests/
```

---

## Notes

* Not production-ready (obviously)
* Some code could be improved
* Could add more commands later
