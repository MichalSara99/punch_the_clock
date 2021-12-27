from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,EmailField,BooleanField,ValidationError
from wtforms.validators import DataRequired,Email,Regexp,EqualTo
from ..models import User

field_width = {'style': 'width: 250px'}

class LoginForm(FlaskForm):
    email = StringField("Email:",
                        render_kw=field_width,
                        validators=[DataRequired(),Email()])
    password = PasswordField("Password:",
                             render_kw=field_width,
                             validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField("Log In")

class RegisterForm(FlaskForm):
    email = EmailField("Email:",
                       render_kw=field_width,
                       validators=[DataRequired()])
    username = StringField("Username:",
                           render_kw=field_width,
                           validators=[DataRequired(),
                                       Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,
                                              'Usernames must have only letters, numbers, dots or '
                                                'underscores')])
    password = PasswordField("Password:",
                             render_kw=field_width,
                             validators=[DataRequired(),
                                         EqualTo('password2',
                                                 message='Passwords must match')])
    password2 = PasswordField('Confirm password:',
                              render_kw=field_width,
                              validators=[DataRequired()])
    submit = SubmitField("Register")

    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already exists.')
