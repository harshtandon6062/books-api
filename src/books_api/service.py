from books_api.models import Book, BookCreate, BookUpdate
from books_api.repository import BookRepository
from books_api.exceptions import BookNotFound, DuplicateBook


class BookService:
    def __init__(self, repo: BookRepository):
        self.repo = repo

    def get_book(self, book_id: int) -> Book:
        book = self.repo.get(book_id)
        if book is None:
            raise BookNotFound(book_id)
        return book

    def list_books(self, offset: int, limit: int) -> list[Book]:
        return self.repo.list_all(offset, limit)

    def create_book(self, data: BookCreate) -> Book:
        self._ensure_unique(data.title, data.author)
        book = Book(**data.model_dump())
        self.repo.add(book)
        self.repo.commit()
        self.repo.refresh(book)
        return book

    def update_book(self, book_id: int, data: BookUpdate) -> Book:
        book = self.get_book(book_id)
        changes = data.model_dump(exclude_none=True)
        self._ensure_unique(
            changes.get("title", book.title),
            changes.get("author", book.author),
            ignore_id=book.id,
        )
        for field, value in changes.items():
            setattr(book, field, value)
        self.repo.add(book)
        self.repo.commit()
        self.repo.refresh(book)
        return book

    def delete_book(self, book_id: int) -> None:
        book = self.get_book(book_id)
        self.repo.delete(book)
        self.repo.commit()

    def _ensure_unique(self, title: str, author: str, ignore_id: int | None = None):
        existing = self.repo.find_by_title_author(title, author)
        if existing and existing.id != ignore_id:
            raise DuplicateBook(title, author)
