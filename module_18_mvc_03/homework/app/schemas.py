from typing import Dict

from flasgger import Schema, fields, ValidationError
from marshmallow import Schema, fields, validates, ValidationError, post_load

from models import get_book_by_title, Book, get_author_by_name, Author


class BookSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    author = fields.Str(required=True)

    @validates('title')
    def validate_title(self, title: str) -> None:
        if get_book_by_title(title) is not None:
            raise ValidationError(
                'Book with title "{title}" already exists, '
                'please use a different title.'.format(title=title)
            )

    @post_load
    def create_book(self, data: Dict, **kwargs) -> Book:
        return Book(**data)


class AuthorSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)

    @validates('name')
    def validate_name(self, name: str) -> None:
        if get_author_by_name(name) is not None:
            raise ValidationError(
                'Author with name "{name}" already exists, '
                'please use a different name.'.format(name=name)
            )

    @post_load
    def create_author(self, data: Dict, **kwargs) -> Author:
        return Author(**data)
