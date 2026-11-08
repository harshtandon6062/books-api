class BookNotFound(Exception):
    def __init__(self, book_id: int):
        super().__init__(f"Book {book_id} not found")


class DuplicateBook(Exception):
    def __init__(self, title: str, author: str):
        super().__init__(f"'{title}' by {author} already exists")
