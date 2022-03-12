from typing import Tuple, Dict, Optional

from apispec.ext.marshmallow import MarshmallowPlugin
from flask import Flask, request
from flask_restful import Api, Resource
from marshmallow import ValidationError
from flasgger import APISpec, Swagger
from apispec_webframeworks.flask import FlaskPlugin

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
spec = APISpec(
    title='Books and authors',
    version='1.0.0',
    openapi_version='2.0',
    plugins=[
        FlaskPlugin(),
        MarshmallowPlugin(),
    ],
)

template = spec.to_flasgger(
    app,
    definitions=[BookSchema, AuthorSchema]
)

swagger = Swagger(app, template=template)


class BookList(Resource):
    def get(self, book_id=None) -> Optional[Tuple[str, int]]:
        """
        Endpoint for obtaining the list of the books and for getting a book by id

        :param book_id:
        :return: Optional[Books data]
        ---
         tags:
          - books
         parameters:
           - in: path
             name: book_id
             schema:
               type: integer
             description: The looking book`s id
         responses:
           200:
             description: All books data
             schema:
               type: array
               items:
                 $ref: '#/definitions/Book'
           201:
             description: Book data
             schema:
                 $ref: '#/definitions/Book'
           400:
             description: No book with entered id
        """
        schema = BookSchema()
        if book_id:
            book = get_book_by_id(book_id)
            if book:
                return schema.dump(book), 201
            return f'No book with id {book_id}', 400
        return schema.dump(get_all_books(), many=True), 200

    def post(self) -> Tuple[Dict, int]:
        """
        This is an endpoint for book creation
        If book`s author not being in library - new author will be creating

        :return: New book
        ---
         tags:
         - books
         parameters:
          - in: body
            name: new book params
            author: new book author
            schema:
              $ref: '#/definitions/Book'
         responses:
          201:
            description: The book has been created
            schema:
              $ref: '#/definitions/Book'
          400:
            description: Wrong book params
        """
        data = request.json
        schema = BookSchema()
        try:
            book = schema.load(data)
        except ValidationError as exc:
            return exc.messages, 400
        book = add_book(book)
        return schema.dump(book), 201

    def put(self, book_id: int) -> Tuple[Dict, int]:
        """
        This is an endpoint for book`s params changing

        :param book_id:
        :return: The book with a new params
        ---
        tags:
         - books
        parameters:
          - in: path
            name: book_id
            schema:
              type: integer
            description: The book`s id
          - in: body
            name: book`s new title
            author: book`s new author
            schema:
              $ref: '#/definitions/Book'
        responses:
          201:
            description: Book`s params has been changed
            schema:
                $ref: '#/definitions/Book'
          400:
            description: No book with entered id or wrong book params
        """
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
        """
        This is an endpoint for a book deleting

        :param book_id:
        :return: result str
        ---
        tags:
         - books
        parameters:
          - in: path
            name: book_id
            schema:
              type: integer
            description: The book`s id
        responses:
          200:
            description: Book with entered id was deleted
          400:
            description: No book with entered id
        """
        if get_book_by_id(book_id):
            delete_book_by_id(book_id)
            return f'Book with id {book_id} was deleted', 200
        else:
            return f'No book with id {book_id}', 400


class AuthorList(Resource):
    def get(self, author_id=None) -> Optional[Tuple[str, int]]:
        """
        Endpoint for obtaining the list of the authors and for getting all author books

        :param author_id:
        :return: Optional[All authors data or all author`s books]
        ---
         tags:
          - authors
         parameters:
           - in: path
             name: author_id
             schema:
               type: integer
             description: The looking author`s id
         responses:
           200:
             description: All authors data
             schema:
               type: array
               items:
                 $ref: '#/definitions/Author'
           201:
             description: All author`s books data
             schema:
                 $ref: '#/definitions/Book'
           400:
             description: No author with entered id
        """
        book_schema = BookSchema()
        author_schema = AuthorSchema()
        if author_id:
            author = get_author_by_id(author_id)
            if author:
                all_books = get_all_author_books(author_id)
                if len(all_books) == 0:
                    return f'No any books of author with id {author_id}', 200
                return book_schema.dump(all_books, many=True), 201
            return f'No author with id {author_id}', 400
        return author_schema.dump(get_all_authors(), many=True), 200

    def post(self) -> Tuple[Dict, int]:
        """
        This is an endpoint for author creation

        :return: New author
        ---
         tags:
         - authors
         parameters:
          - in: body
            name: new author name
            schema:
              $ref: '#/definitions/Author'
         responses:
          201:
            description: The author has been created
            schema:
              $ref: '#/definitions/Author'
        """
        data = request.json
        schema = AuthorSchema()
        try:
            author = schema.load(data)
        except ValidationError as exc:
            return exc.messages, 400
        author = add_author(author)
        return schema.dump(author), 201

    def put(self, author_id: int) -> Optional[Tuple]:
        """
        This is an endpoint for author`s name changing

        :param author_id:
        :return: The author with a new name
        ---
        tags:
         - authors
        parameters:
          - in: path
            name: author_id
            schema:
              type: integer
            description: The author`s id
          - in: body
            name: new author name
            schema:
              $ref: '#/definitions/Author'
        responses:
          201:
            description: Author`s name has been changed
            schema:
                $ref: '#/definitions/Author'
          400:
            description: No author with entered id or wrong author name
        """
        data = request.json
        schema = AuthorSchema()
        try:
            author = schema.load(data)
        except ValidationError as exc:
            return exc.messages, 400
        if get_author_by_id(author_id):
            author.id = author_id
            update_author_by_id(author)
            return schema.dump(author), 201
        return f'No author with id {author_id}', 400

    def delete(self, author_id: int) -> Tuple[str, int]:
        """
        This is an endpoint for an author and all his books deleting

        :param author_id:
        :return: result str
        ---
        tags:
         - authors
        parameters:
          - in: path
            name: author_id
            schema:
              type: integer
            description: The author`s id
        responses:
          200:
            description: Author with entered id and all his books were deleted
          400:
            description: No author with entered id
        """
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
