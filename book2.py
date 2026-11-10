from fastapi import FastAPI, HTTPException, Path, Query
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()


class Book:
    id: int
    name: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self, id, name, author, description, rating, published_date):
        self.id = id
        self.name = name
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


BOOKS = [
    Book(
        1, "Atomic Habits", "James Clear", "A book about building good habits", 5, 2012
    ),
    Book(
        2,
        "The Alchemist",
        "Paulo Coelho",
        "A novel about following your dreams",
        4,
        2014,
    ),
    Book(
        3,
        "Deep Work",
        "Cal Newport",
        "A book about improving focus and productivity",
        5,
        2017,
    ),
    Book(
        4,
        "Rich Dad Poor Dad",
        "Robert Kiyosaki",
        "A book about personal finance",
        4,
        2017,
    ),
    Book(
        5, "Clean Code", "Robert C. Martin", "A book about writing better code", 5, 2016
    ),
]


class BookRequest(BaseModel):
    id: int | None = Field(description="ID is not needed on create", default=None)
    name: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)
    published_date: int = Field(gt=1999, lt=2031)

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "a new book",
                "author": "umais",
                "description": "A new description of book",
                "rating": 5,
                "published_date": 2015,
            }
        }
    }


@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS


@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def read_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book_id == book.id:
            return book
    raise HTTPException(status_code=404, detail="item not found")


@app.get("/books/", status_code=status.HTTP_200_OK)
async def read_book_by_rating(rating: int = Query(gt=0, lt=6)):
    book_to_return = []
    for book in BOOKS:
        if book.rating == rating:
            book_to_return.append(book)
    return book_to_return


@app.get("/books/publish/", status_code=status.HTTP_200_OK)
async def read_book_by_date(date: int = Query(gt=1999, lt=2031)):
    book_to_return = []
    for book in BOOKS:
        if book.published_date == date:
            book_to_return.append(book)
    return book_to_return


def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book


@app.post("/books/create_book", status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    print(type(new_book))
    BOOKS.append(find_book_id(new_book))


@app.put("/books/update_book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            book_changed = True
            BOOKS[i] = book
    if not book_changed:
        raise HTTPException(status_code=404, detail="item not found")


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_changed = True
            break
    if not book_changed:
        raise HTTPException(status_code=404, detail="item not found")
