from sqlmodel import Session, select
from books_api.models import Book


class BookRepository:
    def __init__(self, session: Session):
        self.session = session

    def get(self, book_id: int) -> Book | None:
        return self.session.get(Book, book_id)

    def list_all(self, offset: int, limit: int) -> list[Book]:
        stmt = select(Book).offset(offset).limit(limit)
        return list(self.session.exec(stmt).all())

    def find_by_title_author(self, title: str, author: str) -> Book | None:
        stmt = select(Book).where(Book.title == title, Book.author == author)
        return self.session.exec(stmt).first()

    def add(self, book: Book) -> None:
        self.session.add(book)

    def delete(self, book: Book) -> None:
        self.session.delete(book)

    def commit(self) -> None:
        self.session.commit()

    def refresh(self, book: Book) -> None:
        self.session.refresh(book)
