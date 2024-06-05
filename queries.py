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

def get_top_rated_books():
    sql = """
    SELECT * FROM books
    ORDER BY avg_rating DESC
    LIMIT 10
    """
    db_cursor.execute(sql)
    books = db_cursor.fetchall()
    return books