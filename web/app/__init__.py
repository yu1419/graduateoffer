from flask import Flask
from flask_login import LoginManager
import os
from flask_bootstrap import Bootstrap
from flaskext.markdown import Markdown
import markdown
from flask import Markup
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail


login_manager = LoginManager()
mail = Mail()
bootstrap = Bootstrap()
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    Markdown(app)

    app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['gmail_username'] = os.environ.get('gmail_username')
    app.config['gmail_psw'] = os.environ.get('gmail_psw')
    mysql_host = os.environ.get('aws_mysql_host')
    mysql_password = os.environ.get('aws_mysql_password')
    app.config['SECRET_KEY'] = 'hard to guess string'


    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://master:" + mysql_password + "@" + mysql_host + "offer_2?charset=utf8"
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)


    app.jinja_env.globals['markdown'] = markdown
    app.jinja_env.globals['Markup'] = Markup

    bootstrap.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    """from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    from .member import member as member_blueprint
    app.register_blueprint(member_blueprint, url_prefix='/member')"""
    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
