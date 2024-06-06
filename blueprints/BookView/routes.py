from flask import render_template, url_for, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from dikureads.models import load_user, User, Book, Author
from dikureads.queries import get_book, get_authors_from_isbn, get_books, search_books, get_book_shelfs, create_shelf, get_top_rated_books
from dikureads.forms import BookshelfForm


BookView = Blueprint('BookView', __name__)


@BookView.route("/")
def home():
    allBooks = get_books()
    allBooks = [Book(book) for book in allBooks]
    return render_template('pages/homeREAL.html', allBooks=allBooks)

@BookView.route("/read/<book_id>")
def read(book_id):
    book = get_book(book_id)
    book = Book(book)
    authors = get_authors_from_isbn(book_id)
    authors = [Author(author) for author in authors]
    return render_template('pages/book_view.html', book_id=book_id, book=book, authors=authors)

@BookView.route("/search/<search_term>")
def search(search_term):
    books = search_books(search_term)
    books = [Book(book) for book in books]
    return render_template('pages/homeREAL.html', allBooks=books)