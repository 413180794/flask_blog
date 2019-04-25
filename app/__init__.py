# __init__.py 控制包导入的行为
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

from config import config

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "auth.login"

def create_app(config_name):
    app = Flask(__name__)

    app.config.from_object(config[config_name])
    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    # 附加路由和自定义的错误页面
    from .main import main as main_blueprint
    from .auth import auth as auth_blueprint
    from .api import api as api_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(api_blueprint,url_prefix="/api")
    return app
