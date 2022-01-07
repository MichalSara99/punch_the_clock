from flask_wtf import FlaskForm
from flask_babel import lazy_gettext as _l
from wtforms import StringField,SubmitField,PasswordField,EmailField,BooleanField,ValidationError
from wtforms.validators import DataRequired,Email,Regexp,EqualTo
from ..models import User

field_width = {'style': 'width: 250px'}

class LoginForm(FlaskForm):
    email = StringField(_l("Email:"),
                        render_kw=field_width,
                        validators=[DataRequired(),Email()])
    password = PasswordField(_l("Password:"),
                             render_kw=field_width,
                             validators=[DataRequired()])
    remember_me = BooleanField(_l('Keep me logged in'))
    submit = SubmitField(_l("Log In"))

class RegisterForm(FlaskForm):
    email = EmailField(_l("Email:"),
                       render_kw=field_width,
                       validators=[DataRequired()])
    username = StringField(_l("Username:"),
                           render_kw=field_width,
                           validators=[DataRequired(),
                                       Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,
                                              _l('Usernames must have only letters, numbers, dots or '
                                                'underscores'))])
    password = PasswordField(_l("Password:"),
                             render_kw=field_width,
                             validators=[DataRequired(),
                                         EqualTo('password2',
                                                 message='Passwords must match')])
    password2 = PasswordField(_l('Confirm password:'),
                              render_kw=field_width,
                              validators=[DataRequired()])
    submit = SubmitField(_l("Register"))

    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already exists.')
