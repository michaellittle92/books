from typing import Optional
from fastapi import Body, FastAPI
from pydantic import BaseModel, Field

app = FastAPI()



class Book:
    id: int
    title: str
    author: str
    description:str
    rating: int

    #python constructor

    def __init__(self, id, title, author, description, rating):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating 

class BookRequest(BaseModel):
    id: Optional[int] = Field(description="ID is not required on create", default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description:str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=-1, lt=6)

    model_config = {
        "json_schema_extra":{
            "example":{
                "title": "New book title",
                "author": "Example Author",
                "description": "New Book Description", 
                "rating": 5
            }
        }
    }



BOOKS = [
    Book(1, 'Computer Science Pro', 'Author One', 'A very nice book', 5),
    Book(2, 'Be Fast with FastAPI', 'Author One', 'A great book', 5),
    Book(3, 'Master Endpoints', 'Author One', 'A good book', 5),
    Book(4, 'HP1', 'Author Two', 'Book Description', 2),
    Book(5, 'HP2', 'Author Three', 'Book Description', 3),
    Book(6, 'HP3', 'Author Four', 'Book Description', 1)
]

@app.get("/books")
async def read_all_books():
    return BOOKS

@app.get("/books/{book_title}")
async def read_book(book_title: str):
    for book in BOOKS:
        if book.get('title').casefold() == book_title.casefold():
            return book

@app.get("/books/")
async def read_category_by_query(category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('category').casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return

@app.get("/books/by-author/{author}")
async def read_books_by_author(author: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('author').casefold() == author.casefold():
            books_to_return.append(book)
    return books_to_return

@app.get("/books/{book_author}/")
async def read_author_category_by_query(book_author: str, category:str):
    books_to_return = []
    for book in BOOKS:
        if book.get('author').casefold() == book_author.casefold() and \
        book.get('category').casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return

@app.post("/books/create_book")
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))

def find_book_id(book: Book):
    if len(BOOKS) > 0:
        book.id = BOOKS[-1].id + 1
    else:
        book.id = 1
    return book

@app.put("/books/update_book")
async def update_book(updated_book=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == updated_book.get('title').casefold():
            BOOKS[i] = updated_book

@app.delete("/books/delete_book/{book_title}")
async def delete_book(book_title: str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == book_title.casefold():
            BOOKS.pop(i)
            break

