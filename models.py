from flask_login import UserMixin
from dikureads import login_manager, app, db_cursor
from psycopg2 import sql
from typing import Dict

@login_manager.user_loader
def load_user(user_id):
    user_sql = sql.SQL("""
    SELECT * FROM Users
    WHERE pk = %s
    """).format(sql.Identifier('pk'))

    db_cursor.execute(user_sql, (int(user_id),))
    return User(db_cursor.fetchone()) if db_cursor.rowcount > 0 else None


class ModelUserMixin(dict, UserMixin):
    @property
    def id(self):
        return self.pk


class ModelMixin(dict):
    pass


class User(ModelUserMixin):
    def __init__(self, user_data: Dict):
        super(User, self).__init__(user_data)
        self.pk = user_data.get('pk')
        self.full_name = user_data.get('full_name')
        self.user_name = user_data.get('user_name')
        self.password = user_data.get('password')

class Book(ModelMixin):
    def __init__(self, book_data: Dict):
        super(Book, self).__init__(book_data)
        self.isbn = book_data.get('isbn')
        self.title = book_data.get('title')
        self.pages = book_data.get('pages')
        self.avg_rating = book_data.get('avg_rating')
        self.image = book_data.get('image')
        self.format = book_data.get('formart')
        self.descr = book_data.get('descr')

class Author(ModelMixin):
    def __init__(self, author_data: Dict):
        super(Author, self).__init__(author_data)
        self.author_id = author_data.get('author_id')
        self.author_name = author_data.get('author_name')

class Written_by(ModelMixin):
    def __init__(self, written_by_data: Dict):
        super(Written_by, self).__init__(written_by_data)
        self.book = written_by_data.get('book')
        self.author = written_by_data.get('author')

class Book_shelf(ModelMixin):
    def __init__(self, book_shelf_data: Dict):
        super(Book_shelf, self).__init__(book_shelf_data)
        self.shelf_id = book_shelf_data.get('shelf_id')
        self.shelf_owner = book_shelf_data.get('shelf_owner')
        self.shelf_name = book_shelf_data.get('shelf_name')