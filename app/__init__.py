import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os
from flask import Flask, url_for
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_misaka import Misaka
from flask_moment import Moment
from flask_mail import Mail
from config import Config

bootstrap = Bootstrap()
login = LoginManager()
db = SQLAlchemy()
migrate = Migrate()
md = Misaka(fenced_code=True, hard_wrap=True)
moment=Moment()
mail = Mail()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    bootstrap.init_app(app)
    login.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    md.init_app(app)
    moment.init_app(app)
    mail.init_app(app)
    
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    from app.profile import bp as profile_bp
    app.register_blueprint(profile_bp)
    
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp, url_prefix='/errors')
    
    from app.admin import bp as admin_bp
    app.register_blueprint(admin_bp)
    
    if not app.debug and not app.testing:
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] and app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['ADMINS'], subject='Stublog Failure',
                credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)
        
        if app.config['LOG_TO_STDOUT']:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            app.logger.addHandler(stream_handler)
        else:        
            if not os.path.exists('logs'):
                    os.mkdir('logs')
            file_handler = RotatingFileHandler('logs/stublog.log', maxBytes=10240, backupCount=10)
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Stublog startup')
    return app
       
from app import models