from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_misaka import Misaka
from config import Config

bootstrap = Bootstrap()
login = LoginManager()
db = SQLAlchemy()
migrate = Migrate()
md = Misaka()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    bootstrap.init_app(app)
    login.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    md.init_app(app)
    
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    return app

from app import models