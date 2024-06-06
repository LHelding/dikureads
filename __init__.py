import os
from flask import Flask
from dotenv import load_dotenv
from flask_login import LoginManager
from psycopg2.extras import RealDictCursor
import psycopg2

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

conn = psycopg2.connect(
    host="localhost",
    database=os.getenv('DB_NAME'),
    user=os.getenv('DB_USERNAME'),
    password=os.getenv('DB_PASSWORD')
)

db_cursor = conn.cursor(cursor_factory=RealDictCursor)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from dikureads.blueprints.Login.routes import Login
from dikureads.blueprints.Read.routes import Read
from dikureads.blueprints.BookView.routes import BookView

app.register_blueprint(Login)
app.register_blueprint(Read)
app.register_blueprint(BookView)