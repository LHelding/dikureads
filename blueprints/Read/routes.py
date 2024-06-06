from flask import render_template, url_for, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from dikureads.models import load_user, User, Book, Author
from dikureads.queries import get_book, get_authors_from_isbn, get_top_rated_books, get_book_shelfs, create_shelf, get_reviews_from_isbn, add_review
from dikureads.forms import BookshelfForm, ReviewForm


Read = Blueprint('Read', __name__)


@Read.route("/test")
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
    reviews = get_reviews_from_isbn(book_id)
    return render_template('pages/book_view.html', book_id=book_id, book=book, authors=authors, reviews = reviews)

@Read.route("/read/<book_id>/review", methods=['GET', 'POST'])
def review(book_id):
    book = get_book(book_id)
    book = Book(book)
    form = ReviewForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            review_data = dict(rating=form.rating.data,
                             review_text=form.review_text.data)
            review_data = {
                'user_id': current_user.pk,
                'book': book_id,
                'rating': form.rating.data,
                'review_text': form.review_text.data
            }
            add_review(review_data)
            return redirect(url_for('Read.read', book_id=book_id))
    return render_template('pages/review.html', form= form)

@Read.route("/shelf")
def shelf():
    owner = current_user.id
    shelfs = get_book_shelfs(owner)
    return render_template('pages/book_shelf.html', book_shelfs=shelfs)

@Read.route("/shelf/create")
def create_shelf():
    form = BookshelfForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            create_shelf(current_user.id, form.shelf_name.data)
            return redirect(url_for('Read.shelf'))
    return render_template('pages/create_bookshelf.html', form=form)