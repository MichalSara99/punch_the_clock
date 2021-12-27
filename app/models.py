from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask import current_app
from sqlalchemy import desc,asc
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String,DateTime,ForeignKey,Numeric
from app import db
from . import login_manager
from datetime import datetime,time
from sqlalchemy.pool import QueuePool




class Time_dimension(db.Model):
    __tablename__ = 'time_dimension'
    id = db.Column(db.Integer, primary_key=True)
    db_date = db.Column(db.DateTime, unique=True)
    year = db.Column(db.Integer)
    month = db.Column(db.Integer)
    day = db.Column(db.Integer)
    quarter = db.Column(db.Integer)
    week = db.Column(db.Integer)
    day_name = db.Column(db.String(9))
    month_name = db.Column(db.String(9))
    holiday_flag = db.Column(db.String(1))
    weekend_flag = db.Column(db.String(1))
    event = db.Column(db.String(50))


class User(UserMixin,db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(200),unique = True)
    email = db.Column(db.String(200),unique = True)
    password_hash = db.Column(db.String(200))
    confirmed = db.Column(db.String(1), default='F')

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)

    def generate_confirmation_token(self,expiration = 3600):
        s=Serializer(current_app.config['SECRET_KEY'],expiration)
        return s.dumps({'confirm':self.id}).decode('utf-8')

    def confirm(self,token):
        s=Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('confirm')!=self.id:
            return False
        self.confirmed = 'Y'
        db.session.add(self)
        return True


class Work(db.Model):
    __tablename__ = 'work'
    id = db.Column(db.Integer,primary_key = True)
    user_id = db.Column(db.Integer)
    td_id = db.Column(db.Integer)
    start_time = db.Column(db.DateTime)
    lunch_duration = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    worked_time = db.Column(db.DateTime)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


