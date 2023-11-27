import pytest
from website import create_app, db
from website.models import User, Expense, Etag, Income, Itag, Saving, Note
from werkzeug.security import generate_password_hash
from datetime import date


@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def test_user_creation(app):
    with app.app_context():
        user = User(username='testuser', first_name='Test', password=generate_password_hash('password'))
        db.session.add(user)
        db.session.commit()
        assert user.id is not None
        assert user.username == 'testuser'


def test_expense_creation(app):
    with app.app_context():
        user = User(username='testuser', first_name='Test', password=generate_password_hash('password'))
        db.session.add(user)
        etag = Etag(data='Food', user_id=user.id)
        db.session.add(etag)
        db.session.commit()

        expense = Expense(value=10.0, date=date(2023, 1, 1), tag_id=etag.id, user_id=user.id)
        db.session.add(expense)
        db.session.commit()
        assert expense.id is not None
        assert expense.value == 10.0