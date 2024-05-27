from sqlalchemy import create_engine, Column, Integer, String, Date, DateTime, Boolean, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, joinedload, subqueryload, selectinload
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.associationproxy import association_proxy
from datetime import datetime, timedelta

Base = declarative_base()
engine = create_engine('sqlite:///library.db')
Session = sessionmaker(bind=engine)
session = Session()


class Author(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    books = relationship("Book", back_populates="author", cascade="all, delete-orphan")


class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    count = Column(Integer, default=1)
    release_date = Column(Date, nullable=False)
    author_id = Column(Integer, ForeignKey('authors.id'), nullable=False)
    author = relationship("Author", back_populates="books")
    receiving_books = relationship("ReceivingBook", back_populates="book", cascade="all, delete-orphan")


class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False)
    average_score = Column(Float, nullable=False)
    scholarship = Column(Boolean, nullable=False)
    receiving_books = relationship("ReceivingBook", back_populates="student", cascade="all, delete-orphan")
    books = association_proxy('receiving_books', 'book')

    @classmethod
    def get_students_with_scholarship(cls, session):
        return session.query(cls).filter(cls.scholarship == True).all()

    @classmethod
    def get_students_with_average_score_above(cls, session, score):
        return session.query(cls).filter(cls.average_score > score).all()


class ReceivingBook(Base):
    __tablename__ = 'receiving_books'
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    date_of_issue = Column(DateTime, nullable=False, default=datetime.utcnow)
    date_of_return = Column(DateTime)
    book = relationship("Book", back_populates="receiving_books")
    student = relationship("Student", back_populates="receiving_books")

    @hybrid_property
    def count_date_with_book(self):
        if self.date_of_return:
            return (self.date_of_return - self.date_of_issue).days
        else:
            return (datetime.utcnow() - self.date_of_issue).days


Base.metadata.create_all(engine)


def add_test_data():
    author1 = Author(name="Leo", surname="Tolstoy")
    author2 = Author(name="Fyodor", surname="Dostoevsky")
    author3 = Author(name="Jane", surname="Austen")

    book1 = Book(name="War and Peace", count=3, release_date=datetime(1869, 1, 1), author=author1)
    book2 = Book(name="Anna Karenina", count=2, release_date=datetime(1877, 1, 1), author=author1)
    book3 = Book(name="Crime and Punishment", count=4, release_date=datetime(1866, 1, 1), author=author2)
    book4 = Book(name="Pride and Prejudice", count=5, release_date=datetime(1813, 1, 1), author=author3)

    student1 = Student(name="John", surname="Doe", phone="123456789", email="john@example.com", average_score=4.5, scholarship=True)
    student2 = Student(name="Jane", surname="Smith", phone="987654321", email="jane@example.com", average_score=3.8, scholarship=False)
    student3 = Student(name="Alice", surname="Johnson", phone="555555555", email="alice@example.com", average_score=4.2, scholarship=True)

    session.add_all([author1, author2, author3, book1, book2, book3, book4, student1, student2, student3])
    session.commit()

    receiving1 = ReceivingBook(book_id=1, student_id=1, date_of_issue=datetime.utcnow() - timedelta(days=10))
    receiving2 = ReceivingBook(book_id=3, student_id=1, date_of_issue=datetime.utcnow() - timedelta(days=5))
    receiving3 = ReceivingBook(book_id=2, student_id=2, date_of_issue=datetime.utcnow() - timedelta(days=20))
    receiving4 = ReceivingBook(book_id=4, student_id=3, date_of_issue=datetime.utcnow() - timedelta(days=30), date_of_return=datetime.utcnow() - timedelta(days=5))

    session.add_all([receiving1, receiving2, receiving3, receiving4])
    session.commit()


add_test_data()
