from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
DB_NAME = "database.db"
basedir = os.path.abspath(os.path.dirname(__file__))


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
        basedir, DB_NAME
    )

    db.init_app(app)
    migrate.init_app(app, db)

    from .views import dashboard_bp, expenses_bp, incomes_bp, savings_bp, tags_bp
    from .auth import auth

    app.register_blueprint(dashboard_bp, url_prefix="/")
    app.register_blueprint(expenses_bp, url_prefix="/")
    app.register_blueprint(incomes_bp, url_prefix="/")
    app.register_blueprint(savings_bp, url_prefix="/")
    app.register_blueprint(tags_bp, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from .models import User, Expense, Etag, Income, Itag, Saving, Note

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app
