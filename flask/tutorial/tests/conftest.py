import os
import tempfile

import pytest

from flaskr import create_app
from flaskr.db import get_db, init_db


with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf-8')


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()
    # In order to prepare flask for testing, TESTING flag can be set to true
    # in settings.
    app = create_app({'TESTING': True, 'DATABASE': db_path})

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    # A test client can be used to request the application without running a
    # server by using test_client method.
    return app.test_client()


@pytest.fixture
def runner(app):
    # A test runner can be used to run registered commands with an application
    # without using a shell by using test_cli_runner.
    return app.test_cli_runner()


class AuthActions():
    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test'):
        return self._client.post('/auth/login/',
                                 data={'username': username,
                                       'password': password})

    def logout(self):
        return self._client.get('/auth/logout/')


@pytest.fixture
def auth(client):
    return AuthActions(client)
