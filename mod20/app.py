import datetime

from flask import Flask, jsonify, abort, request
from bd import session, Book, Receivingbook

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
    debtors = session.query(Receivingbook).filter(
        Receivingbook.date_of_return == None,
        Receivingbook.date_of_issue <= threshold_date
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

    new_receiving = Receivingbook(
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

    receiving = session.query(Receivingbook).filter_by(
        book_id=book_id,
        student_id=student_id,
        date_of_return=None
    ).first()

    if not receiving:
        abort(400, description="No matching record found")

    receiving.date_of_return = datetime.datetime.utcnow()
    session.commit()
    return jsonify({'message': 'Book returned successfully'}), 200


if __name__ == '__main__':
    app.run(debug=True)

