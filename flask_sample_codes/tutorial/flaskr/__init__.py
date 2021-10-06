from os import path, makedirs

from flask import Flask

from .db import init_app
from .auth import auth_bp
from .blog import blog_bp


# Files which should not be commited to version control can be located in the
# instance folder.
# In order to inform flask that the configuration files are relative to the
# instance folder, instance_relative_config argument can be used when
# initiating the flask app.
def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY='TH1515453CR3TK3Y',
                            DATABASE=path.join(app.instance_path,
                                               'flaskr.sqlite3'))

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        makedirs(app.instance_path)
    except OSError:
        pass

    init_app(app)
    # In order to plug a blueprint into a flask app, register_blueprint method
    # can be used.
    app.register_blueprint(auth_bp)
    app.register_blueprint(blog_bp)

    @app.route('/hello/')
    def hello():
        return 'Hello, world!'

    return app
