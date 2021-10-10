from sqlite3 import connect, PARSE_DECLTYPES, Row

from flask import current_app, g
from flask.cli import with_appcontext
from click import command, echo


# The g variable is a special object which is unique for each request which is
# used to store data during the request.
# current_app is a proxy to the flask app which is handling the request when
# accessed.
def get_db():
    if 'db' not in g:
        g.db = connect(current_app.config['DATABASE'],
                       detect_types=PARSE_DECLTYPES)

        g.db.row_factory = Row
    return g.db


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


# In order to open a file relative to the root path, open_resource method can
# be used.
def init_db():
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf-8'))


@command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    echo('Initialized the data base.')


# In order to register a function as a clean up after the response is returned
# by flask, teardown_appcontext method can be used.
# In order to register a command to flask command, add_command method can be
# used.
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
