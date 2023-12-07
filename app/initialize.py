from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_migrate import Migrate
from flask_apscheduler import APScheduler
from flask_mail import Mail

db = SQLAlchemy()
db_name = 'database.db'
migrate = Migrate()
scheduler = APScheduler()
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_name}'
    app.config['SECRET_KEY'] = 'secret'

    db.init_app(app)
    scheduler.init_app(app)         # to set a schedule
    migrate.init_app(app, db)       # to make migrations for db

    scheduler.start()

    config_email(app)
    mail.init_app(app)              # to send a mail

    from .views import views
    app.register_blueprint(views, url_prefix='/')

    from .models import Products, Items, Requests
    with app.app_context():
        db.create_all()

    return app


def create_database(app):
    if not path.exists('app/' + db_name):
        db.create_all(app)
        print('Created database')


def config_email(app):
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'your_mail@gmail.com'
    app.config['MAIL_PASSWORD'] = 'your password'
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True




# command
"""
    flask --app main.py db init ----> migrate
"""
