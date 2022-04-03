import csv
import re
from datetime import datetime, timedelta

from sqlalchemy import Column, Integer, Date, Text, Float, Boolean, DateTime, create_engine, ForeignKey, event, func, \
    distinct
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, backref
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
    author_id = Column(Integer, ForeignKey('authors.id'), nullable=False)

    author = relationship("Author", backref=backref("books",
                                                    cascade="all, "
                                                            "delete-orphan",
                                                    lazy='joined'))
    students = association_proxy('book', 'ReceivingBook')

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

    books = association_proxy('student', 'ReceivingBook')

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

    student = association_proxy("books", "Student")
    book = association_proxy("students", "Book")

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
        try:
            data = request.json
            if 'book_title' in data:
                """Getting a books with the specific string in the title"""
                book_title = data['book_title']
                all_books = session.query(Book).filter(Book.name.like(f'%{book_title}%')).all()
                books_list = []
                for book in all_books:
                    json_book = book.to_json()
                    books_list.append(json_book)
                return jsonify(books_list=books_list), 200

            elif 'author_id' in data:
                """Getting all books written by the specific author that are available now"""
                author_id = data['author_id']
                available_books = session.query(Book). \
                    filter(Book.author_id == author_id,
                           Book.id == ReceivingBook.book_id,
                           ReceivingBook.date_of_return == None).all()
                books_list = []
                for book in available_books:
                    json_book = book.to_json()
                    books_list.append(json_book)
                return jsonify(available_books_list=books_list), 200

            elif 'student_id' in data:
                """Getting another book written by the author that was reading by the specific student"""
                student_id = data['student_id']
                authors_id = session.query(ReceivingBook.book_id).distinct(). \
                    filter(ReceivingBook.book_id == Book.id,
                           ReceivingBook.student_id == student_id).subquery()
                books_by_authors = session.query(Book.id).filter(Book.author_id in authors_id).all()
                books_list = []
                for book in books_by_authors:
                    json_book = book.to_json()
                    books_list.append(json_book)
                return jsonify(recomended_books_list=books_list), 200

        except TypeError:
            """Getting all books in the library"""
            all_books = session.query(Book).all()
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


@app.route('/books/month', methods=['GET'])
def book_of_the_month() -> Tuple:
    """Getting an average count of the books that was taken at this month"""
    current_year = datetime.now().year
    current_month = datetime.now().month
    current_month_start = datetime(current_year, current_month, 1, 0, 0, 0, 0)
    taken_books_count = session.query(func.count(ReceivingBook.id)). \
        filter(ReceivingBook.date_of_issue >= current_month_start).scalar()
    students_count = session.query(func.count(Student.id)).scalar()
    avg_book_month_count = round(taken_books_count / students_count, 3)
    return f'The average count of the books taken by the students at this month is {avg_book_month_count}', 200


@app.route('/books/popular', methods=['GET'])
def the_most_popular_book() -> Tuple:
    """Getting the count of the books that was taken at this month"""
    book_id = session.query(func.count(ReceivingBook.id)). \
        filter(ReceivingBook.student_id == Student.id,
               Student.average_score >= 4.0). \
        group_by(ReceivingBook.book_id). \
        order_by(func.count(ReceivingBook.id).desc()). \
        limit(1).all()
    book = session.query(Book). \
        filter(Book.id == book_id[0][0]).all()
    json_book = book.to_json()
    return jsonify(the_most_popular_book=json_book), 200


@app.route('/receiving')
def receiving() -> Optional[Tuple]:
    if request.method == 'GET':
        """Getting all students that keep holding a book for 14 days or more"""
        deadline = datetime.now() - timedelta(days=14)
        students = session.query(Student).filter(ReceivingBook.is_debtor(deadline)).all()
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


@app.route('/students')
def students() -> Optional:
    if request.method == 'GET':
        """Getting top 10 readers of the year"""
        current_year = datetime.now().year
        current_year_start = datetime(current_year, 1, 1, 0, 0, 0, 0)
        students = session.query(Student). \
            filter(ReceivingBook.student_id == Student.id,
                   ReceivingBook.date_of_issue >= current_year_start). \
            group_by(ReceivingBook.student_id). \
            order_by(func.count(ReceivingBook.id).desc()). \
            limit(10).all()
        students_list = []
        for student in students:
            json_student = student.to_json()
            students_list.append(json_student)
        return jsonify(top_10_readers_of_the_year=students_list), 200

    elif request.method == 'POST':
        """Adding students from the file 'students_file'"""
        if request.method == 'POST':
            stud_file = request.files.get('students_file')
            if stud_file:
                try:
                    stud_file.save('stud.csv')
                    stud_list = []
                    with open('stud.csv', 'r', newline='') as csvfile:
                        reader = csv.DictReader(csvfile, delimiter=';')
                        for student in reader:
                            if student['scholarship'].lower() == 'true':
                                student['scholarship'] = True
                            elif student['scholarship'].lower() == 'false':
                                student['scholarship'] = False
                            stud_list.append(student)
                    session.bulk_insert_mappings(Student, stud_list)
                    try:
                        session.commit()
                    except Exception:
                        return 'Error processing a phone number', 400
                except Exception:
                    return 'Error processing the file "students_file"', 400
                return 'Students from the file "students_file" was added', 200
            return 'No file "students_file" was found', 400


def check_phone_number(check_session: Session) -> None:
    phone_format = r'\+7\(\d{3}\)\-\d{3}\-\d{2}\-\d{2}'
    check_students = check_session.query(Student)
    students_list = []
    for student in check_students:
        json_student = student.to_json()
        students_list.append(json_student)
        student_phone = json_student['phone']
        if not re.fullmatch(phone_format, student_phone):
            session.rollback()
            break


event.listen(session, "before_commit", check_phone_number)

if __name__ == '__main__':
    app.run(debug=True)
