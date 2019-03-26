from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, \
    TextAreaField, FileField
from wtforms.validators import DataRequired
import os


class LoginForm(FlaskForm):
    username = StringField('Login', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign in')


class RegForm(FlaskForm):
    username = StringField('Login', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign up')


class EditForm(FlaskForm):
    username = StringField('New Name', validators=[DataRequired()])
    submit = SubmitField('Change name')


class CreateForm(FlaskForm):
    title = StringField('New Community Name', validators=[DataRequired()])
    bio = TextAreaField('Bio', validators=[DataRequired()])
    submit = SubmitField('Create')


class EditComForm(FlaskForm):
    title = StringField('New Community Name')
    bio = TextAreaField('New Bio')
    submit = SubmitField('Change Community')


class AddNewsForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    hashtag = StringField('Hashtag')
    content = TextAreaField('Content', validators=[DataRequired()])
    image = FileField('Image')
    submit = SubmitField('Post')


class EditNewsForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    hashtag = StringField('Hashtag', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Change')
