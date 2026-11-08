from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from database import create_tables
from exceptions import BookNotFound, DuplicateBook
from router import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield


app = FastAPI(lifespan=lifespan)


@app.exception_handler(BookNotFound)
async def handle_not_found(request: Request, exc: BookNotFound):
    return JSONResponse(status_code=404, content={"detail": str(exc)})


@app.exception_handler(DuplicateBook)
async def handle_duplicate(request: Request, exc: DuplicateBook):
    return JSONResponse(status_code=409, content={"detail": str(exc)})


app.include_router(router)
