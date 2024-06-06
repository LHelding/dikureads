from flask import render_template, url_for, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from dikureads.models import load_user, User, Book, Author, Book_shelf
from dikureads.queries import get_book, get_authors_from_isbn, get_top_rated_books, get_book_shelfs, create_shelf_in_db, get_book_shelf, delete_shelf, get_books_in_shelf, remove_book_from_shelf_db, get_reviews_from_isbn, add_review
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

@Read.route("/shelf/create", methods=['GET', 'POST'])
def create_shelf():
    form = BookshelfForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            create_shelf_in_db(current_user.id, form.shelf_name.data)
            return redirect(url_for('Read.shelf'))
    return render_template('pages/create_bookshelf.html', form=form)

@Read.route("/shelf/delete/<shelf_id>")
def delete_bookshelf(shelf_id):
    selected_shelf = get_book_shelf(shelf_id)
    selected_shelf = Book(selected_shelf)
    if selected_shelf['shelf_owner'] == current_user.id:
        delete_shelf(shelf_id)
    return redirect(url_for('Read.shelf'))

@Read.route("/shelf/<shelf_id>")
def view_shelf(shelf_id):
    shelf = get_book_shelf(shelf_id)
    # Kunne tjekke om den faktisk gav et resultat   
    books = get_books_in_shelf(shelf_id)
    books = [Book(book) for book in books]
    if shelf['shelf_owner'] != current_user.id:
        return redirect(url_for('Read.shelf'))
    return render_template('pages/view_bookshelf.html', shelf=shelf, books=books)

@Read.route("/shelf/remove/<shelf_id>/<book_id>")
def remove_book_from_shelf(shelf_id, book_id):
    #shelf = get_book_shelf(shelf_id)
    ## should be fixed
    # if shelf['shelf_owner'] != current_user.id:
    #     return redirect(url_for('Read.shelf'))
    remove_book_from_shelf_db(shelf_id, book_id)
    return redirect(url_for('Read.view_shelf', shelf_id=shelf_id))
    