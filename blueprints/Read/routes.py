from flask import render_template, url_for, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from dikureads.models import load_user, User, Book, Author
from dikureads.queries import get_book, get_authors_from_isbn, get_top_rated_books


Read = Blueprint('Read', __name__)


@Read.route("/")
def home():
    top_rated_books = get_top_rated_books()
    top_rated_books = [Book(book) for book in top_rated_books]
    return render_template('pages/home.html', top_rated_books=top_rated_books)

@Read.route("/read/<book_id>")
def read(book_id):
    book = get_book(book_id)
    book = Book(book)
    authors = get_authors_from_isbn(book_id)
    authors = [Author(author) for author in authors]
    return render_template('pages/book_view.html', book_id=book_id, book=book, authors=authors)