from forms import MyForm
from flask import Flask, render_template, request, redirect
from typing import List, Dict
from models import get_all_books, Book, get_author_books, get_book_by_id_from_db

app = Flask(__name__)

BOOKS = [
    {'id': 0, 'title': 'A byte of Python', 'author': 'Swaroop C. H.'},
    {'id': 1, 'title': 'Moby-Dick; or, The Whale', 'author': 'Herman Melville'},
    {'id': 2, 'title': 'Mar and Peace', 'author': 'Lev Tolstoy'},
]


def _get_html_table_for_books(books: List[Dict]) -> str:
    table = """
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Title</th>
                    <th>Author</th>
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
def show_all_books() -> str:
    return render_template('pred_index.html', books=get_all_books())


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        form = MyForm()
        if form.validate_on_submit():
            title = request.form['title']
            author = request.form['author']
            new_book = Book(title=title, author=author)
            new_book.save()
            return redirect('/books')
        else:
            return f'Ошибка в заполнении формы, убедитесь, что заполнили все поля'
    else:
        return render_template('add_book.html')


@app.route('/books/<string:author_name>')
def get_authors_books(author_name):
    author_books = get_author_books(author_name)
    return render_template('author_books.html', author=author_name, books=author_books)


@app.route('/books/<int:id>')
def get_book_by_id(id):
    id_books = get_book_by_id_from_db(id)
    return render_template('book_by_id.html', id=id, books=id_books)


if __name__ == '__main__':
    app.config["WTF_CSRF_ENABLED"] = False
    app.run(debug=True)
