from dikureads import db_cursor, conn
from dikureads.models import User

def get_user_by_user_name(user_name):
    sql = """
    SELECT * FROM users
    WHERE user_name = %s
    """
    db_cursor.execute(sql, (user_name,))
    user = User(db_cursor.fetchone()) if db_cursor.rowcount > 0 else None
    return user

def get_book(isbn):
    sql = """
    SELECT * FROM books
    WHERE isbn = %s
    """
    db_cursor.execute(sql, (isbn,))
    book = db_cursor.fetchone()
    return book

def search_books(search_term):
    sql = """
    SELECT * FROM books
    WHERE title LIKE %s
    ORDER BY title ASC
    LIMIT 2000
    """
    db_cursor.execute(sql, ('%' + search_term + '%',))
    books = db_cursor.fetchall()
    return books

def get_books():
    sql = """
    SELECT * FROM books
    ORDER BY title ASC
    LIMIT 2000
    """
    db_cursor.execute(sql)
    books = db_cursor.fetchall()
    return books

def insert_user(user: User):
    sql = """
    INSERT INTO Users(user_name, full_name, password)
    VALUES (%s, %s, %s)
    """
    db_cursor.execute(sql, (user.user_name, user.full_name, user.password))
    conn.commit()

def get_authors_from_isbn(isbn):
    sql = """
    SELECT author_name
    FROM authors
    JOIN written_by ON authors.author_id = written_by.author
    WHERE written_by.book = %s
    """
    db_cursor.execute(sql, (isbn,))
    authors = db_cursor.fetchall()
    return authors

def get_reviews_from_isbn(isbn):
    sql = """
    SELECT *
    FROM Reviews
    JOIN Users ON Reviews.user_id = Users.pk
    WHERE Reviews.book = %s
    """
    db_cursor.execute(sql, (isbn,))
    reviews = db_cursor.fetchall()
    return reviews

def add_review(review):
    sql = """
    INSERT INTO Reviews (user_id, book, review_text, rating)
    VALUES (%s, %s, %s, %s)
    """
    print(review)
    db_cursor.execute(sql, (review['user_id'], review['book'], review['review_text'], review['rating']))
    conn.commit()

def get_top_rated_books():
    sql = """
    SELECT * FROM books
    ORDER BY avg_rating DESC
    LIMIT 10
    """
    db_cursor.execute(sql)
    books = db_cursor.fetchall()
    return books

def get_book_shelfs(user_id):
    sql = """
    SELECT * FROM Bookshelf
    WHERE shelf_owner = %s
    """
    db_cursor.execute(sql, (user_id,))
    shelfs = db_cursor.fetchall()
    return shelfs
    
def create_shelf(user_id, shelf_name):
    sql = """
    INSERT INTO Bookshelf(shelf_owner, shelf_name)
    VALUES (%s, %s)
    """
    db_cursor.execute(sql, (user_id, shelf_name))
    conn.commit()
    return True