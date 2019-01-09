from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_misaka import Misaka
from flask_moment import Moment
from config import Config

bootstrap = Bootstrap()
login = LoginManager()
db = SQLAlchemy()
migrate = Migrate()
md = Misaka(fenced_code=True, hard_wrap=True, smartypants=True)
moment=Moment()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    bootstrap.init_app(app)
    login.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    md.init_app(app)
    moment.init_app(app)
    
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    return app

from app import models