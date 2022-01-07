from flask import Flask,render_template,url_for,session,redirect,request,flash,Markup
from flask_login import login_user,login_required,logout_user,current_user
from flask_babel import _
from . import auth
from .forms import LoginForm,RegisterForm
from .. import db
from .. models import User,User_settings
from ..email import send_mail


@auth.route('/login',methods = ['GET','POST'])
def login():
    log_form = LoginForm()
    if log_form.validate_on_submit():
        user = User.query.filter_by(email=log_form.email.data).first()
        # fist check if the user is in the database:
        if user is not None and user.verify_password(log_form.password.data):
            login_user(user,log_form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        flash(_('Invalid email or password'))
    return render_template('auth/login.html',
                           log_form=log_form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash(_('You have been logged out.'))
    return redirect(url_for('main.index'))



@auth.route('/register',methods = ['GET','POST'])
def register():
    reg_form = RegisterForm()
    if reg_form.validate_on_submit():
        user = User(email = reg_form.email.data,
                    username = reg_form.username.data,
                    password = reg_form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_mail(user.email,_('Confirm Your Account'),
                  'auth/email/confirm',user = user,token=token)
        flash(_('A confirmation email has been sent to you by email.'))
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html',
                           reg_form = reg_form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed == 'Y':
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        db.session.commit()
        user_settings = User_settings(user_id = current_user.id,
                                      working_time = '08:00:00')
        db.session.add(user_settings)
        db.session.commit()
        flash(_('You have confirmed your account. Thanks!'))
    else:
        flash(_('The confirmation link is invalid or has expired.'))
    return redirect(url_for('main.index'))

@auth.before_app_request
def before_request():
    if current_user.is_authenticated \
        and not (current_user.confirmed == 'Y') \
        and request.blueprint !='auth' \
        and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))

@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed == 'Y':
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')

@auth.route('/confirmed')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_mail(current_user.email,_('Confirm Your Account'),
              'auth/email/confirm',user = current_user,token=token)
    flash(_('A new confirmation email has been sent to your email.'))
    return redirect(url_for('main.index'))
