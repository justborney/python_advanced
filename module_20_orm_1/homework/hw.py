from datetime import datetime, timedelta

from sqlalchemy import Column, Integer, Date, Text, Float, Boolean, DateTime, create_engine
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy.orm import declarative_base, sessionmaker
from flask import Flask, jsonify, request
from typing import Dict, Any, Optional, Tuple

app = Flask(__name__)

engine = create_engine('sqlite:///hw.db')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    count = Column(Integer, default=1)
    release_date = Column(Date, nullable=False)
    author_id = Column(Integer, nullable=False)

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in
                self.__table__.columns}


class Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    surname = Column(Text, nullable=False)


class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    surname = Column(Text, nullable=False)
    phone = Column(Text, nullable=False)
    email = Column(Text, nullable=False)
    average_score = Column(Float, nullable=False)
    scholarship = Column(Boolean, nullable=False)

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in
                self.__table__.columns}

    @classmethod
    def get_students_with_scholarship(cls) -> Tuple[Any, int]:
        """Get all students with a scholarship"""
        try:
            return session.query(Student).filter(Student.scholarship == True), 200
        except NoResultFound:
            return 'No students with a scholarship', 400

    @classmethod
    def get_students_with_specific_score(cls, score: float) -> Tuple[Any, int]:
        """Get all students with specific score or more"""
        try:
            return session.query(Student).filter(Student.average_score >= score), 200
        except NoResultFound:
            return f'No student with score {score} or more', 400


class ReceivingBook(Base):
    __tablename__ = 'receiving_books'

    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, nullable=False)
    student_id = Column(Integer, nullable=False)
    date_of_issue = Column(DateTime, nullable=False)
    date_of_return = Column(DateTime)

    @hybrid_property
    def days_with_a_book(self):
        """Days while student keeps holding a book"""
        if self.date_of_return:
            return self.date_of_return - self.date_of_issue
        return datetime.now() - self.date_of_issue

    @hybrid_method
    def is_debtor(self, compare_date):
        """Counting days while student keeps holding a book"""
        return self.date_of_issue < compare_date


@app.before_request
def before_request_func() -> None:
    Base.metadata.create_all(engine)


@app.route('/books')
def books() -> Tuple:
    if request.method == 'GET':
        data = request.json
        book_title = data['book_title']
        if not book_title:
            """Getting all books in the library"""
            all_books = session.query(Book).all()
            books_list = []
            for book in all_books:
                json_book = book.to_json()
                books_list.append(json_book)
            return jsonify(books_list=books_list), 200

        """Getting a books with the specific string in the title"""
        all_books = session.query(Book).filter(Book.name.like(f'%{book_title}%'))
        books_list = []
        for book in all_books:
            json_book = book.to_json()
            books_list.append(json_book)
        return jsonify(books_list=books_list), 200

    elif request.method == 'POST':
        """Return a book with the specific book_id from a student with the specific student_id to the library"""
        book_id = request.form.get('book_id', type=int)
        student_id = request.form.get('student_id', type=int)
        record = session.query(ReceivingBook).filter(ReceivingBook.book_id == book_id,
                                                     ReceivingBook.student_id == student_id).one_or_none()
        if record is None:
            return f'No record with book_id {book_id} and student_id {student_id}', 400
        record.date_of_return = datetime.now()
        session.add(record)
        session.commit()
        return f'A book with id {book_id} was returned by a student with id {student_id} on {datetime.now().date()}', 201


@app.route('/receiving')
def receiving() -> Optional[Tuple]:
    if request.method == 'GET':
        """Getting all students that keep holding a book for 14 days or more"""
        deadline = datetime.now() - timedelta(days=14)
        students = session.query(Student).filter(ReceivingBook.is_debtor(deadline))
        if students is None:
            return 'No debtors', 201
        students_list = []
        for student in students:
            json_student = student.to_json()
            students_list.append(json_student)
        return jsonify(students_list=students_list), 200

    elif request.method == 'POST':
        """Issue a book with the specific book_id to a student with the specific student_id"""
        book_id = request.form.get('book_id', type=int)
        student_id = request.form.get('student_id', type=int)
        record = ReceivingBook(book_id=book_id,
                               student_id=student_id,
                               date_of_issue=datetime.now())
        session.add(record)
        session.commit()
        return f'A book with id {book_id} was issued to a student with id {student_id} on {datetime.now().date()}', 201


if __name__ == '__main__':
    app.run()
