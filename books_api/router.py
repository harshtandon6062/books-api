from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from database import get_session
from models import Book, BookCreate, BookUpdate
from repository import BookRepository
from service import BookService

router = APIRouter(prefix="/books", tags=["books"])


def get_repo(session: Session = Depends(get_session)) -> BookRepository:
    return BookRepository(session)


def get_service(repo: BookRepository = Depends(get_repo)) -> BookService:
    return BookService(repo)


@router.post("", response_model=Book, status_code=201)
def create_book(data: BookCreate, service: BookService = Depends(get_service)):
    return service.create_book(data)


@router.get("", response_model=list[Book])
def list_books(
    offset: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    service: BookService = Depends(get_service),
):
    return service.list_books(offset, limit)


@router.get("/{book_id}", response_model=Book)
def get_book(book_id: int, service: BookService = Depends(get_service)):
    return service.get_book(book_id)


@router.patch("/{book_id}", response_model=Book)
def update_book(
    book_id: int,
    data: BookUpdate,
    service: BookService = Depends(get_service),
):
    return service.update_book(book_id, data)


@router.delete("/{book_id}", status_code=204)
def delete_book(book_id: int, service: BookService = Depends(get_service)):
    service.delete_book(book_id)
