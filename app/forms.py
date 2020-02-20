from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.db_models import User, Task
from app import imgs


class LoginForm(FlaskForm):
    username = StringField(u'Username', validators=[DataRequired()])
    password = PasswordField(u'Password', validators=[DataRequired()])
    remember_me = BooleanField(u'Remember Me')
    submit = SubmitField(u'Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    first_name = StringField('First name', validators=[DataRequired()])
    last_name = StringField('Last name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_validation = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('The user with this username is already registered!')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email is not None:
            raise ValidationError('The user with this email is already registered!')


class TaskSubmitForm(FlaskForm):
    text = StringField(label='Add task:', id='textarea',
                       validators=[DataRequired()])
    image = FileField(validators=[FileAllowed(imgs, 'You can attach only images!')])
    submit = SubmitField('Add task')

    def validate_task_name(self, text):
        task_name = Task.query.filter_by(name=text).first()
        if task_name == text:
            raise ValidationError('Task names must be unique!')
