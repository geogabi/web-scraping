from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_migrate import Migrate

db = SQLAlchemy()
db_name = 'database.db'
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_name}'
    app.config['SECRET_KEY'] = 'secret'
    db.init_app(app)
    migrate.init_app(app, db)

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


# command
"""
    flask --app main.py db init ----> migrate
"""
