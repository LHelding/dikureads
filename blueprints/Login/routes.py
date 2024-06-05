from flask import render_template, url_for, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user
from dikureads.models import load_user, User

from dikureads.forms import UserLoginForm, UserSignupForm
from dikureads.queries import get_user_by_user_name, insert_user

Login = Blueprint('Login', __name__)


@Login.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('Login.home'))
    form = UserLoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = get_user_by_user_name(form.user_name.data)
            if user and user['password'] == form.password.data:
                login_user(user, remember=True)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('Login.home'))
    return render_template('pages/login.html', form=form)


@Login.route("/signup", methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('Login.home'))
    form = UserSignupForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user_data = dict(full_name=form.full_name.data,
                             user_name=form.user_name.data,
                             password=form.password.data)
            user = User(user_data)
            insert_user(user)
            user = get_user_by_user_name(form.user_name.data)
            if user:
                login_user(user, remember=True)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('Login.home'))
    return render_template('pages/signup.html', form=form)

@Login.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('Login.login'))
