from datetime import datetime, timedelta
from sqlalchemy import create_engine, Column, Integer, String, Date, DateTime, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.hybrid import hybrid_property

engine = create_engine('sqlite:///library.db')
Base = declarative_base()


class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    count = Column(Integer, default=1)
    release_date = Column(Date, nullable=False)
    author_id = Column(Integer, nullable=False)


class Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)


class Students(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False)
    average_score = Column(Float, nullable=False)
    scholarship = Column(Boolean, nullable=False)

    @classmethod
    def get_students_with_scholarship(cls, session):
        return session.query(cls).filter(cls.scholarship == True).all()

    @classmethod
    def get_students_with_average_score_above(cls, session, score):
        return session.query(cls).filter(cls.average_score > score).all()


class Receivingbook(Base):
    __tablename__ = 'receiving_books'

    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, nullable=False)
    student_id = Column(Integer, nullable=False)
    date_of_issue = Column(DateTime, default=datetime.utcnow())
    date_of_return = Column(DateTime)

    @hybrid_property
    def count_date_with_book(self):
        if self.date_of_return:
            return (self.date_of_return - self.date_of_issue).days
        return (datetime.utcnow() - self.date_of_issue).days


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Добавление тестовых данных
author1 = Author(name='Leo', surname='Tolstoy')
author2 = Author(name='Fyodor', surname='Dostoevsky')
session.add_all([author1, author2])
session.commit()

book1 = Book(name='War and Peace', count=3, release_date=datetime(1869, 1, 1), author_id=author1.id)
book2 = Book(name='Crime and Punishment', count=2, release_date=datetime(1866, 1, 1), author_id=author2.id)
session.add_all([book1, book2])
session.commit()

student1 = Students(name='Ivan', surname='Ivanov', phone='1234567890', email='ivanov@example.com', average_score=4.5,
                    scholarship=True)
student2 = Students(name='Petr', surname='Petrov', phone='0987654321', email='petrov@example.com', average_score=3.8,
                    scholarship=False)
session.add_all([student1, student2])
session.commit()

receiving_book1 = Receivingbook(book_id=book1.id, student_id=student1.id,
                                date_of_issue=datetime.utcnow() - timedelta(days=10))
receiving_book2 = Receivingbook(book_id=book2.id, student_id=student2.id,
                                date_of_issue=datetime.utcnow() - timedelta(days=20))
session.add_all([receiving_book1, receiving_book2])
session.commit()
