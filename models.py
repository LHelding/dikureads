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