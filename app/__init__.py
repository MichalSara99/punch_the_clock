from flask import Flask,request
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_babel import Babel
from config import config,Config


bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
babel = Babel()
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
    babel.init_app(app)
    login_manager.init_app(app)


    ## All the routes go in here

    from .main import main as main_bp
    app.register_blueprint(main_bp)

    from .auth import auth as auth_bp
    app.register_blueprint(auth_bp)
    return app

@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(list(Config.LANGUAGES))

def translate_month(month_str):
    if get_locale() == 'cs':
        if month_str == 'January':
            return 'Leden'
        elif month_str == 'February':
            return 'Únor'
        elif month_str == 'March':
            return 'Březen'
        elif month_str == 'April':
            return 'Duben'
        elif month_str == 'May':
            return 'Květen'
        elif month_str == 'June':
            return 'Červen'
        elif month_str == 'July':
            return 'Červenec'
        elif month_str == 'August':
            return 'Srpen'
        elif month_str == 'September':
            return 'Září'
        elif month_str == 'October':
            return 'Říjen'
        elif month_str == 'November':
            return 'Listopad'
        elif month_str == 'December':
            return 'Prosinec'
    return

def translate_weekday(weekday_str):
    if get_locale() == 'cs':
        if weekday_str == 'Monday':
            return 'Pondělí'
        elif weekday_str == 'Tuesday':
            return 'Úterý'
        elif weekday_str == 'Wednesday':
            return 'Středa'
        elif weekday_str == 'Thursday':
            return 'Čtvrtek'
        elif weekday_str == 'Friday':
            return 'Pátek'
    return

