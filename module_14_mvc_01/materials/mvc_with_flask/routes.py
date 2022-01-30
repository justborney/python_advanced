from typing import List, Dict

from flask_wtf import FlaskForm, CSRFProtect
from flask import Flask, render_template, request
from wtforms import TextAreaField

from models import init_db, get_all_books, DATA, add_book_func, searching_books_by_author, books_count

from wtforms.validators import DataRequired

csrf = CSRFProtect()

app = Flask(__name__)
csrf.init_app(app)
app.config['SECRET_KEY'] = 'SECRET_KEY'


class AddingBookForm(FlaskForm):
    title = TextAreaField(validators=[DataRequired()])
    author = TextAreaField(validators=[DataRequired()])


class SearchingBookByAuthor(FlaskForm):
    author = TextAreaField(validators=[DataRequired()])


def _get_html_table_for_books(books: List[Dict]) -> str:
    table = """
<table>
    <thead>
    <tr>
        <th>ID</td>
        <th>Title</td>
        <th>Author</td>
    </tr>
    </thead>
    <tbody>
        {books_rows}
    </tbody>
</table>
"""
    rows = ''
    for book in books:
        rows += '<tr><td>{id}</tb><td>{title}</tb><td>{author}</tb></tr>'.format(
            id=book['id'], title=book['title'], author=book['author'],
        )
    return table.format(books_rows=rows)


@app.route('/books')
def all_books():
    return render_template(
        'index.html',
        books=get_all_books(),
    )


@app.route('/books/form')
def get_books_form():
    return render_template('add_book.html')


@app.route("/books/add", methods=["POST"])
def add_book():
    wt_form = AddingBookForm(request.form)
    if wt_form.validate_on_submit():
        return render_template('adding_book_result.html', result=add_book_func(wt_form))
    return render_template('adding_book_fail.html')


@app.route("/books/search")
def search_books_y_author():
    return render_template('searching_books_by_author.html')


@app.route("/books/search-result", methods=["POST"])
def search_book_by_author_result():
    wt_form = SearchingBookByAuthor(request.form)
    if wt_form.validate_on_submit():
        return render_template('searching_books_by_author_result.html', result=searching_books_by_author(wt_form))
    return render_template('searching_books_by_author_fail.html')


@app.context_processor
def get_books_count():
    books_total_count = books_count()
    return dict(count=books_total_count)


if __name__ == '__main__':
    init_db(DATA)
    app.run(debug=True)
