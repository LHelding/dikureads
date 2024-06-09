from flask import render_template, url_for, redirect, request, Blueprint
from flask_login import current_user, login_required
from dikureads.models import Book, Author, Book_shelf

from dikureads.queries import get_book, get_authors_from_isbn,  get_book_shelfs, create_shelf_in_db, get_book_shelf, delete_shelf, get_books_in_shelf, remove_book_from_shelf_db, get_reviews_from_isbn, add_review, add_book_to_shelf_db
from dikureads.forms import BookshelfForm, ReviewForm, OtherBookshelfForm
from dikureads.utils.choices import ModelChoices


Read = Blueprint('Read', __name__)

@Read.route("/read/<book_id>", methods=['GET', 'POST'])
def read(book_id):
    book = get_book(book_id)
    book = Book(book)
    authors = get_authors_from_isbn(book_id)
    authors = [Author(author) for author in authors]
    reviews = get_reviews_from_isbn(book_id)
    if current_user.is_authenticated:
        shelves = [Book_shelf(shelf) for shelf in get_book_shelfs(current_user.id)]
        choices = ModelChoices(shelves)
        form = OtherBookshelfForm()
        form.bookshelf.choices = choices.choices()
        if request.method == 'POST':
            if form.validate_on_submit():
                add_book_to_shelf_db(form.bookshelf.data, book_id)
                return redirect(url_for('Read.read', book_id=book_id))
        return render_template('pages/book_view.html', book_id=book_id, book=book, authors=authors, reviews = reviews, form=form)
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
    remove_book_from_shelf_db(shelf_id, book_id)
    return redirect(url_for('Read.view_shelf', shelf_id=shelf_id))

@Read.route("/shelf/add/<book_id>", methods=['POST'])
@login_required
def add_book_to_shelf(book_id):
    shelf_id = request.form.get('shelf_id')
    if shelf_id and current_user.is_authenticated:
        add_book_to_shelf_db(shelf_id, book_id)
    return redirect(url_for('Read.read', book_id=book_id))