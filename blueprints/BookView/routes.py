from flask import render_template, request, Blueprint
from dikureads.models import Book
from dikureads.queries import  get_books, search_books


BookView = Blueprint('BookView', __name__)


@BookView.route("/")
def home():
    allBooks = get_books()
    allBooks = [Book(book) for book in allBooks]
    return render_template('pages/home.html', allBooks=allBooks)

@BookView.route("/search", methods=['GET'])
def search():
    search_term = request.args.get('query', '')
    books = search_books(search_term)
    books = [Book(book) for book in books]
    return render_template('pages/home.html', allBooks=books)