from typing import Tuple, Dict, Optional

from flask import Flask, request
from flask_restful import Api, Resource
from marshmallow import ValidationError

from models import (
    BOOK_DATA,
    AUTHOR_DATA,
    get_all_books,
    init_db,
    add_book,
    update_book_by_id,
    get_book_by_id,
    delete_book_by_id,
    add_author,
    update_author_by_id,
    get_all_authors,
    get_author_by_id,
    get_all_author_books,
    delete_author_by_id
)
from schemas import BookSchema, AuthorSchema

app = Flask(__name__)
api = Api(app)


class BookList(Resource):
    def get(self, book_id=None) -> Optional[Tuple[str, int]]:
        schema = BookSchema()
        if book_id:
            book = get_book_by_id(book_id)
            if book:
                return schema.dump(book), 200
            return f'No book with id {book_id}', 400
        return schema.dump(get_all_books(), many=True), 200

    def post(self) -> Tuple[Dict, int]:
        data = request.json
        schema = BookSchema()
        try:
            book = schema.load(data)
        except ValidationError as exc:
            return exc.messages, 400
        book = add_book(book)
        return schema.dump(book), 201

    def put(self, book_id: int) -> Tuple[Dict, int]:
        data = request.json
        schema = BookSchema()
        try:
            book = schema.load(data)
        except ValidationError as exc:
            return exc.messages, 400
        book.id = book_id
        update_book_by_id(book)
        return schema.dump(book), 201

    def delete(self, book_id: int) -> Tuple[str, int]:
        if get_book_by_id(book_id):
            delete_book_by_id(book_id)
            return f'Book with id {book_id} was deleted', 200
        else:
            return f'No book with id {book_id}', 400


class AuthorList(Resource):
    def get(self, author_id=None) -> Optional[Tuple[str, int]]:
        schema = BookSchema()
        if author_id:
            author = get_author_by_id(author_id)
            if author:
                all_books = get_all_author_books(author_id)
                if len(all_books) == 0:
                    return f'No any books of author with id {author_id}', 200
                return schema.dump(all_books, many=True), 200
            return f'No author with id {author_id}', 400
        return schema.dump(get_all_authors(), many=True), 200

    def post(self) -> Tuple[Dict, int]:
        data = request.json
        schema = AuthorSchema()
        try:
            author = schema.load(data)
        except ValidationError as exc:
            return exc.messages, 400
        author = add_author(author)
        return schema.dump(author), 201

    def put(self, author_id: int) -> Tuple[Dict, int]:
        data = request.json
        schema = AuthorSchema()
        try:
            author = schema.load(data)
        except ValidationError as exc:
            return exc.messages, 400
        author.id = author_id
        update_author_by_id(author)
        return schema.dump(author), 201

    def delete(self, author_id: int) -> Tuple[str, int]:
        if get_author_by_id(author_id):
            delete_author_by_id(author_id)
            return f'Author with id {author_id} and all his books were deleted', 200
        else:
            return f'No author with id {author_id}', 400


api.add_resource(BookList, '/api/books', '/api/books/<int:book_id>')
api.add_resource(AuthorList, '/api/authors', '/api/authors/<int:author_id>')

if __name__ == '__main__':
    init_db(initial_books=BOOK_DATA, initial_authors=AUTHOR_DATA)
    app.run(debug=True)
