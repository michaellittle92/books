from typing import Optional
from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()



class Book:
    id: int
    title: str
    author: str
    description:str
    rating: int
    publish_date: int

    #python constructor

    def __init__(self, id, title, author, description, rating, publish_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating 
        self.publish_date = publish_date

class BookRequest(BaseModel):
    id: Optional[int] = Field(description="ID is not required on create", default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description:str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=-1, lt=6)
    publish_date: int = Field(gt=1000, lt=2050)

    model_config = {
        "json_schema_extra":{
            "example":{
                "title": "New book title",
                "author": "Example Author",
                "description": "New Book Description", 
                "rating": 5,
                "publish_date": 2000
            }
        }
    }

BOOKS = [
    Book(1, 'Computer Science Pro', 'Author One', 'A very nice book', 5, 1990),
    Book(2, 'Be Fast with FastAPI', 'Author One', 'A great book', 5, 2000),
    Book(3, 'Master Endpoints', 'Author One', 'A good book', 5, 2000),
    Book(4, 'HP1', 'Author Two', 'Book Description', 2, 2000),
    Book(5, 'HP2', 'Author Three', 'Book Description', 3, 2026),
    Book(6, 'HP3', 'Author Four', 'Book Description', 1, 2026)
]

@app.get("/books", status_code= status.HTTP_200_OK)
async def read_all_books():
    return BOOKS

@app.get("/books/{book_id}", status_code= status.HTTP_200_OK)
async def read_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(404, "Book not found")
        
@app.get("/boooks/{publish_date}", status_code= status.HTTP_200_OK)
async def read_book_by_publish_date(publish_date: int = Path(gt=1990, lt=2050)):
    books_to_return = []
    for book in BOOKS:
        if book.publish_date == publish_date:
            books_to_return.append(book)
    return books_to_return
        
@app.get("/books/", status_code= status.HTTP_200_OK)
async def read_book_by_rating(book_rating: int = Query(gt=0, lt=6)):
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)
    return books_to_return


@app.post("/books/create_book", status_code= status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))

def find_book_id(book: Book):
    if len(BOOKS) > 0:
        book.id = BOOKS[-1].id + 1
    else:
        book.id = 1
    return book


@app.put("/books/update_book", status_code= status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            book_changed = True
    if book_changed == False:
       raise HTTPException(404, "Book not found")

@app.delete("/books/{book_id}", status_code= status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_changed = True
            break
    if book_changed == False:
       raise HTTPException(404, "Book not found")