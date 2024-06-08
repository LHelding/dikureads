from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField, FloatField
from wtforms.validators import DataRequired, Length, ValidationError, NumberRange

from dikureads.queries import get_user_by_user_name, get_book_shelfs
from dikureads.models import Book_shelf
from dikureads.utils.choices import ModelChoices2, UserTypeChoices
import re

class UserLoginForm(FlaskForm):
    user_name = StringField('Username',
                            validators=[DataRequired(), Length(min=2, max=50)],
                            render_kw=dict(placeholder='Username'))
    password = PasswordField('Password',
                             validators=[DataRequired()],
                             render_kw=dict(placeholder='Password'))
    submit = SubmitField('Login')

    def validate_password(self, field):
        user = get_user_by_user_name(self.user_name.data)
        if user is None:
            raise ValidationError(f'User name "{self.user_name.data}" does not exist.')
        if user.password != self.password.data:
            raise ValidationError(f'User name or password are incorrect.')

class UserSignupForm(FlaskForm):
    full_name = StringField('Full name',
                            validators=[DataRequired(), Length(min=2, max=50)],
                            render_kw=dict(placeholder='Full name'))
    user_name = StringField('Email',
                            validators=[DataRequired(), Length(min=2, max=50)],
                            render_kw=dict(placeholder='Username'))
    password = PasswordField('Password',
                             validators=[DataRequired()],
                             render_kw=dict(placeholder='Password'))
    password_repeat = PasswordField('Repeat Password',
                                    validators=[DataRequired()],
                                    render_kw=dict(placeholder='Password'))

    submit = SubmitField('Sign up')

    def validate_user_name(self, field):
        user = get_user_by_user_name(self.user_name.data)
        if user:
            raise ValidationError(f'User name "{self.user_name.data}" already in use.')

        val = re.search(r'[a-z]{3}[0-9]{3}(?=@alumni.ku.dk)', self.user_name.data)
        if not val:
            raise ValidationError(f'Venligst brug dit KU email som brugernavn')

    def validate_password_repeat(self, field):
        if not self.password.data == self.password_repeat.data:
            raise ValidationError(f'Provided passwords do not match.')

class ReviewForm(FlaskForm):
    rating = IntegerField ('Rating',
                            validators=[DataRequired(), NumberRange(min=1, max=5)],
                            render_kw=dict(placeholder='select number between 1 and 5'))
    review_text = StringField('Review text',
                            validators=[DataRequired(), Length(min=2, max=1500)],
                            render_kw=dict(placeholder='Review text'))
    submit = SubmitField('Post review')

class BookshelfForm(FlaskForm):
    shelf_name = StringField('Shelf name',
                             validators=[DataRequired(), Length(min=2, max=50)],
                             render_kw=dict(placeholder='Shelf name'))
    submit = SubmitField('Create shelf')

class BookshelfForm(FlaskForm):    
    bookshelf = SelectField('Bogreol',
                           choices=[])

    submit = SubmitField('submit')