import json
from dataclasses import dataclass, asdict, field, replace
from datetime import date
from pathlib import Path
from typing import List, Optional
from uuid import uuid4

DATA_FILE = Path(__file__).resolve().parent / "data.json"


def _validate_publication_year(year: object) -> int:
    """出版年が1年から現在年までの整数であることを検証します。"""
    current_year = date.today().year
    if (
        not isinstance(year, int)
        or isinstance(year, bool)
        or not 1 <= year <= current_year
    ):
        raise ValueError(
            f"Publication year must be an integer from 1 to {current_year}."
        )
    return year


@dataclass
class Book:
    """書籍コレクション内の1冊を表します。

    属性:
        title: 書籍のタイトル。
        author: 著者名。
        year: 出版年。
        read: 読了済みかどうか。
        rating: 1から5までの任意の評価。
        review: 任意のレビュー文。
        id: 一意の識別子。省略時には自動生成されます。

    使用例:
        >>> book = Book("Dune", "Frank Herbert", 1965)
        >>> book.read
        False
    """

    title: str
    author: str
    year: int
    read: bool = False
    rating: Optional[int] = None
    review: Optional[str] = None
    id: str = field(default_factory=lambda: str(uuid4()))

    def __post_init__(self) -> None:
        _validate_publication_year(self.year)


def get_book_statistics(books: List[Book]) -> dict[str, int | Book | None]:
    """コレクションの冊数を集計し、最も古い本と新しい本を特定します。

    引数:
        books (List[Book]): 集計する書籍のリスト。

    戻り値:
        dict[str, int | Book | None]: ``total``、``read``、``unread``の各件数と、
        ``oldest_book``、``newest_book``の各書籍を含む辞書です。``books``が空の場合、
        書籍の値は``None``になります。

    発生する例外:
        AttributeError: 要素が``Book``に必要な``read``属性や``year``属性を持たない場合。

    使用例:
        >>> book = Book("Dune", "Frank Herbert", 1965, read=True)
        >>> get_book_statistics([book])["read"]
        1
    """
    read_count = sum(book.read for book in books)
    return {
        "total": len(books),
        "read": read_count,
        "unread": len(books) - read_count,
        "oldest_book": min(books, key=lambda book: book.year, default=None),
        "newest_book": max(books, key=lambda book: book.year, default=None),
    }


def _book_from_data(data: object, index: int) -> Book:
    """JSONからデコードした値を検証し、``Book``に変換します。

    引数:
        data (object): 書籍のフィールドを含む想定の、デコード済みJSON値。
        index (int): 元のコレクション内における0始まりの位置。

    戻り値:
        Book: 検証済みの書籍。IDが省略されている場合は自動生成されます。

    発生する例外:
        ValueError: 値がオブジェクトでない場合、必須フィールドがない場合、
            想定外のフィールドがある場合、またはフィールドの型や値が無効な場合。

    使用例:
        >>> _book_from_data({"title": "Dune", "author": "Frank Herbert",
        ...                  "year": 1965}, 0).title
        'Dune'
    """
    if not isinstance(data, dict):
        raise ValueError(f"Book at index {index} must be an object.")

    required_fields = {"title", "author", "year"}
    missing_fields = required_fields - data.keys()
    if missing_fields:
        raise ValueError(
            f"Book at index {index} is missing: {', '.join(sorted(missing_fields))}."
        )

    unexpected_fields = data.keys() - required_fields - {
        "read",
        "rating",
        "review",
        "id",
    }
    if unexpected_fields:
        raise ValueError(
            f"Book at index {index} has unexpected fields: "
            f"{', '.join(sorted(unexpected_fields))}."
        )

    title = data["title"]
    author = data["author"]
    year = data["year"]
    read = data.get("read", False)
    rating = data.get("rating")
    review = data.get("review")
    book_id = data.get("id")
    if not isinstance(title, str):
        raise ValueError(f"Book at index {index} has a non-string title.")
    if not isinstance(author, str):
        raise ValueError(f"Book at index {index} has a non-string author.")
    try:
        _validate_publication_year(year)
    except ValueError as error:
        raise ValueError(
            f"Book at index {index} has an invalid year: {error}"
        ) from error
    if not isinstance(read, bool):
        raise ValueError(f"Book at index {index} has a non-boolean read status.")
    if rating is not None and (
        not isinstance(rating, int) or isinstance(rating, bool) or not 1 <= rating <= 5
    ):
        raise ValueError(f"Book at index {index} has a rating outside 1 to 5.")
    if review is not None and not isinstance(review, str):
        raise ValueError(f"Book at index {index} has a non-string review.")
    if "id" in data and (
        not isinstance(book_id, str) or not book_id.strip()
    ):
        raise ValueError(f"Book at index {index} has an invalid id.")

    return Book(
        title=title,
        author=author,
        year=year,
        read=read,
        rating=rating,
        review=review,
        id=book_id if isinstance(book_id, str) else str(uuid4()),
    )


class BookCollection:
    """モジュールのJSONデータファイルに保存された書籍を読み込み、管理します。

    使用例:
        >>> collection = BookCollection()
        >>> isinstance(collection.list_books(), list)
        True
    """

    def __init__(self) -> None:
        """コレクションを作成し、``DATA_FILE``から書籍を読み込みます。

        発生する例外:
            OSError: データファイルが存在しない以外の理由で読み込めない場合。
            ValueError: データファイルのJSONまたは書籍データが無効な場合。

        使用例:
            >>> collection = BookCollection()
            >>> len(collection.list_books()) >= 0
            True
        """
        self.books: List[Book] = []
        self.load_books()

    def load_books(self) -> None:
        """メモリ上のコレクションを``DATA_FILE``から読み込んだ書籍に置き換えます。

        データファイルが存在しない場合は、空のコレクションとして扱います。

        発生する例外:
            OSError: ファイルが存在しない以外の理由で読み込めない場合。
            ValueError: JSONの形式が正しくない場合、または書籍データが無効な場合。

        使用例:
            >>> collection = BookCollection()
            >>> collection.load_books()
        """
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            if not isinstance(data, list):
                raise ValueError("The collection must be a list.")
            self.books = [
                _book_from_data(book_data, index)
                for index, book_data in enumerate(data)
            ]
        except FileNotFoundError:
            self.books = []
        except ValueError as error:
            raise ValueError(f"Cannot load books from data.json: {error}") from error

    def save_books(self) -> None:
        """現在のコレクションをJSON形式で``DATA_FILE``に書き込みます。

        発生する例外:
            OSError: ファイルを開けない場合、または書き込めない場合。
            TypeError: コレクション内にJSONへ変換できない値が含まれている場合。

        使用例:
            >>> collection = BookCollection()
            >>> collection.save_books()
        """
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump([asdict(b) for b in self.books], f, indent=2, ensure_ascii=False)

    def add_book(self, title: str, author: str, year: int) -> Book:
        """書籍をコレクションに追加し、変更をファイルに保存します。

        引数:
            title (str): 書籍のタイトル。
            author (str): 著者名。
            year (int): 出版年。

        戻り値:
            Book: 自動生成されたIDを含む、新しく作成された書籍。

        発生する例外:
            ValueError: 出版年が1から現在年までの整数でない場合。
            OSError: 更新したコレクションを保存できない場合。

        使用例:
            >>> collection = BookCollection()
            >>> book = collection.add_book("Dune", "Frank Herbert", 1965)
            >>> book.title
            'Dune'
        """
        book = Book(title=title, author=author, year=year)
        self.books.append(book)
        self.save_books()
        return book

    def list_books(self) -> List[Book]:
        """コレクション内のすべての書籍のコピーを、現在の順序で返します。

        戻り値:
            List[Book]: 保存されている書籍の浅いコピーのリストです。返された書籍を
            変更しても、コレクション内の書籍には影響しません。

        使用例:
            >>> collection = BookCollection()
            >>> books = collection.list_books()
            >>> isinstance(books, list)
            True
        """
        return [replace(book) for book in self.books]

    def find_book_by_title(self, title: str) -> Optional[Book]:
        """大文字と小文字を区別せず、タイトルが完全一致する最初の書籍を検索します。

        引数:
            title (str): 検索するタイトル。

        戻り値:
            Optional[Book]: 一致する書籍。見つからない場合は``None``。

        使用例:
            >>> collection = BookCollection()
            >>> collection.add_book("Dune", "Frank Herbert", 1965)
            >>> collection.find_book_by_title("dune").title
            'Dune'
        """
        for book in self.books:
            if book.title.lower() == title.lower():
                return book
        return None

    def find_book_by_id(self, book_id: str) -> Optional[Book]:
        """一意のIDを使って書籍を検索します。

        引数:
            book_id (str): 検索するID。

        戻り値:
            Optional[Book]: 一致する書籍。見つからない場合は``None``。

        使用例:
            >>> collection = BookCollection()
            >>> book = collection.add_book("Dune", "Frank Herbert", 1965)
            >>> collection.find_book_by_id(book.id).title
            'Dune'
        """
        for book in self.books:
            if book.id == book_id:
                return book
        return None

    def mark_as_read(self, title: str) -> bool:
        """タイトルが完全一致する最初の書籍を、読了済みにします（大文字・小文字は区別しません）。

        引数:
            title (str): 読了済みにする書籍のタイトル。

        戻り値:
            bool: 書籍が見つかり、読了済みにできた場合は``True``、それ以外は``False``。

        発生する例外:
            OSError: 書籍を読了済みにした後、更新したコレクションを保存できない場合。

        使用例:
            >>> collection = BookCollection()
            >>> collection.add_book("Dune", "Frank Herbert", 1965)
            >>> collection.mark_as_read("DUNE")
            True
        """
        book = self.find_book_by_title(title)
        if book:
            book.read = True
            self.save_books()
            return True
        return False

    def _set_rating_and_review(
        self, book: Optional[Book], rating: Optional[int], review: Optional[str]
    ) -> bool:
        """評価とレビューを検証して書籍を更新し、変更をファイルに保存します。

        引数:
            book (Optional[Book]): 更新する書籍。見つからない場合は``None``。
            rating (Optional[int]): 1から5までの評価。``None``の場合、評価を消去します。
            review (Optional[str]): レビュー文。``None``の場合、レビューを消去します。

        戻り値:
            bool: 書籍を更新した場合は``True``、それ以外は``False``。

        発生する例外:
            ValueError: 評価が1から5までの整数でも``None``でもない場合、または
                レビューが文字列でも``None``でもない場合。
            OSError: 更新したコレクションを保存できない場合。

        使用例:
            >>> collection = BookCollection()
            >>> book = collection.add_book("Dune", "Frank Herbert", 1965)
            >>> collection._set_rating_and_review(book, 5, "Excellent")
            True
        """
        if rating is not None and (
            not isinstance(rating, int)
            or isinstance(rating, bool)
            or not 1 <= rating <= 5
        ):
            raise ValueError("Rating must be an integer from 1 to 5 or None.")
        if review is not None and not isinstance(review, str):
            raise ValueError("Review must be a string or None.")

        if book is None:
            return False

        book.rating = rating
        book.review = review
        self.save_books()
        return True

    def set_rating_and_review(
        self, title: str, rating: Optional[int], review: Optional[str]
    ) -> bool:
        """タイトルが完全一致する書籍の評価とレビューを設定します（大文字・小文字は区別しません）。

        引数:
            title (str): 更新する書籍のタイトル。
            rating (Optional[int]): 1から5までの評価。``None``の場合、評価を消去します。
            review (Optional[str]): レビュー文。``None``の場合、レビューを消去します。

        戻り値:
            bool: 一致する書籍を更新した場合は``True``、それ以外は``False``。

        発生する例外:
            ValueError: 評価またはレビューの値が無効な場合。
            OSError: 更新したコレクションを保存できない場合。

        使用例:
            >>> collection = BookCollection()
            >>> collection.add_book("Dune", "Frank Herbert", 1965)
            >>> collection.set_rating_and_review("Dune", 5, "Excellent")
            True
        """
        return self._set_rating_and_review(
            self.find_book_by_title(title), rating, review
        )

    def set_rating_and_review_by_id(
        self, book_id: str, rating: Optional[int], review: Optional[str]
    ) -> bool:
        """一意のIDを指定して、書籍の評価とレビューを設定します。

        引数:
            book_id (str): 更新する書籍のID。
            rating (Optional[int]): 1から5までの評価。``None``の場合、評価を消去します。
            review (Optional[str]): レビュー文。``None``の場合、レビューを消去します。

        戻り値:
            bool: 一致する書籍を更新した場合は``True``、それ以外は``False``。

        発生する例外:
            ValueError: 評価またはレビューの値が無効な場合。
            OSError: 更新したコレクションを保存できない場合。

        使用例:
            >>> collection = BookCollection()
            >>> book = collection.add_book("Dune", "Frank Herbert", 1965)
            >>> collection.set_rating_and_review_by_id(
            ...     book.id, 5, "Excellent"
            ... )
            True
        """
        return self._set_rating_and_review(
            self.find_book_by_id(book_id), rating, review
        )

    def remove_book(self, title: str) -> bool:
        """タイトルが完全一致する最初の書籍を削除します（大文字・小文字は区別しません）。

        引数:
            title (str): 削除する書籍のタイトル。

        戻り値:
            bool: 書籍が見つかり削除できた場合は``True``、それ以外は``False``。

        発生する例外:
            OSError: 書籍を削除した後、更新したコレクションを保存できない場合。

        使用例:
            >>> collection = BookCollection()
            >>> collection.add_book("Dune", "Frank Herbert", 1965)
            >>> collection.remove_book("dune")
            True
        """
        book = self.find_book_by_title(title)
        if book:
            self.books.remove(book)
            self.save_books()
            return True
        return False

    def find_by_author(self, author: str) -> List[Book]:
        """著者名が完全一致する書籍を検索します（大文字・小文字は区別しません）。

        引数:
            author (str): 検索する著者名。

        戻り値:
            List[Book]: 一致する書籍のリスト。一致するものがない場合は空のリストです。

        使用例:
            >>> collection = BookCollection()
            >>> collection.add_book("Dune", "Frank Herbert", 1965)
            >>> [book.title for book in collection.find_by_author("frank herbert")]
            ['Dune']
        """
        return [b for b in self.books if b.author.lower() == author.lower()]
