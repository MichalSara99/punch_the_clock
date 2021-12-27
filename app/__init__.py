from flask import Flask,render_template
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from config import config


bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    # extensions inits:
    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)


    ## All the routes go in here

    from .main import main as main_bp
    app.register_blueprint(main_bp)

    from .auth import auth as auth_bp
    app.register_blueprint(auth_bp)
    return app



