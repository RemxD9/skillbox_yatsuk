import csv
from datetime import datetime
from io import StringIO

from flask import Flask, jsonify, abort, request, render_template_string
from sqlalchemy import func, desc
from sqlalchemy.orm import joinedload
from bd import session, Book,  Student, ReceivingBook


app = Flask(__name__)


@app.route('/books', methods=['GET'])
def get_all_books():
    books = session.query(Book).all()
    return jsonify([{
        'id': book.id,
        'name': book.name,
        'count': book.count,
        'release_date': book.release_date,
        'author_id': book.author_id
    } for book in books])


@app.route('/debtors', methods=['GET'])
def get_debtors():
    threshold_date = datetime.datetime.utcnow() - datetime.timedelta(days=14)
    debtors = session.query(ReceivingBook).filter(
        ReceivingBook.date_of_return == None,
        ReceivingBook.date_of_issue <= threshold_date
    ).all()
    return jsonify([{
        'id': debtor.id,
        'book_id': debtor.book_id,
        'student_id': debtor.student_id,
        'date_of_issue': debtor.date_of_issue.isoformat(),
        'count_date_with_book': debtor.count_date_with_book
    } for debtor in debtors])


@app.route('/issue_book', methods=['POST'])
def issue_book():
    data = request.get_json()
    book_id = data.get('book_id')
    student_id = data.get('student_id')

    if not book_id or not student_id:
        abort(400, description="book_id and student_id are required")

    new_receiving = ReceivingBook(
        book_id=book_id,
        student_id=student_id
    )
    session.add(new_receiving)
    session.commit()
    return jsonify({'message': 'Book issued successfully'}), 201


@app.route('/return_book', methods=['POST'])
def return_book():
    data = request.get_json()
    book_id = data.get('book_id')
    student_id = data.get('student_id')

    receiving = session.query(ReceivingBook).filter_by(
        book_id=book_id,
        student_id=student_id,
        date_of_return=None
    ).first()

    if not receiving:
        abort(400, description="No matching record found")

    receiving.date_of_return = datetime.datetime.utcnow()
    session.commit()
    return jsonify({'message': 'Book returned successfully'}), 200


@app.route('/books_by_author/<int:author_id>', methods=['GET'])
def get_books_by_author(author_id):
    books = session.query(Book).filter(Book.author_id == author_id).all()
    return jsonify([{
        'id': book.id,
        'name': book.name,
        'count': book.count,
        'release_date': book.release_date.isoformat(),
        'author_id': book.author_id
    } for book in books])


@app.route('/unread_books_by_author/<int:student_id>', methods=['GET'])
def get_unread_books_by_author(student_id):
    student = session.query(Student).options(joinedload(Student.receiving_books)).filter(Student.id == student_id).one()
    read_books_ids = [rb.book_id for rb in student.receiving_books]
    read_authors_ids = {rb.book.author_id for rb in student.receiving_books}
    unread_books = session.query(Book).filter(Book.author_id.in_(read_authors_ids),
                                              Book.id.notin_(read_books_ids)).all()
    return jsonify([{
        'id': book.id,
        'name': book.name,
        'count': book.count,
        'release_date': book.release_date.isoformat(),
        'author_id': book.author_id
    } for book in unread_books])


@app.route('/average_books_this_month', methods=['GET'])
def get_average_books_this_month():
    start_of_month = datetime(datetime.utcnow().year, datetime.utcnow().month, 1)
    end_of_month = datetime(datetime.utcnow().year, datetime.utcnow().month + 1,
                            1) if datetime.utcnow().month < 12 else datetime(datetime.utcnow().year + 1, 1, 1)
    total_books_issued = session.query(ReceivingBook).filter(ReceivingBook.date_of_issue >= start_of_month,
                                                             ReceivingBook.date_of_issue < end_of_month).count()
    total_students = session.query(Student).count()
    average_books = total_books_issued / total_students if total_students > 0 else 0
    return jsonify({'average_books': average_books})


@app.route('/popular_book_above_score', methods=['GET'])
def get_popular_book_above_score():
    score_threshold = 4.0
    popular_books = session.query(ReceivingBook.book_id, func.count(ReceivingBook.book_id).label('count')).join(
        Student).filter(Student.average_score > score_threshold).group_by(ReceivingBook.book_id).order_by(
        desc('count')).first()
    book = session.query(Book).get(popular_books.book_id)
    return jsonify({
        'id': book.id,
        'name': book.name,
        'count': book.count,
        'release_date': book.release_date.isoformat(),
        'author_id': book.author_id
    })


@app.route('/top_10_reading_students', methods=['GET'])
def get_top_10_reading_students():
    start_of_year = datetime(datetime.utcnow().year, 1, 1)
    top_students = session.query(Student.id, Student.name, Student.surname,
                                 func.count(ReceivingBook.id).label('count')).join(ReceivingBook).filter(
        ReceivingBook.date_of_issue >= start_of_year).group_by(Student.id).order_by(desc('count')).limit(10).all()
    return jsonify([{
        'id': student.id,
        'name': student.name,
        'surname': student.surname,
        'books_count': student.count
    } for student in top_students])


@app.route('/upload_students')
def upload_students_form():
    form_html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Upload Students</title>
    </head>
    <body>
        <h1>Upload Students</h1>
        <form action="/csvreader" method="get">
            <button type="submit">Go to CSV Reader</button>
        </form>
    </body>
    </html>
    """
    return render_template_string(form_html)


@app.route('/csvreader', methods=['GET', 'POST'])
def csv_reader():
    if request.method == 'POST':
        if 'file' not in request.files:
            abort(400, description="No file part")

        file = request.files['file']
        if file.filename == '':
            abort(400, description="No selected file")

        if file:
            stream = StringIO(file.stream.read().decode("UTF8"), newline=None)
            csv_input = csv.DictReader(stream, delimiter=';')
            students = []
            for row in csv_input:
                students.append({
                    'name': row['name'],
                    'surname': row['surname'],
                    'phone': row['phone'],
                    'email': row['email'],
                    'average_score': float(row['average_score']),
                    'scholarship': row['scholarship'].lower() == 'true'
                })
            session.bulk_insert_mappings(Student, students)
            session.commit()
            return jsonify(message="Students uploaded successfully")

    form_html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>CSV Reader</title>
    </head>
    <body>
        <h1>Upload Students CSV</h1>
        <form method="post" action="/csvreader" enctype="multipart/form-data">
            <input type="file" name="file" accept=".csv">
            <button type="submit">Upload</button>
        </form>
    </body>
    </html>
    """
    return render_template_string(form_html)


if __name__ == '__main__':
    app.run(debug=True)

