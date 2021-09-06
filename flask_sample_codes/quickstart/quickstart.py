from markupsafe import escape

from flask import Flask, url_for, request, render_template

# An instance of Flask class will play the role of a WSGI application.
# The first parameter of the constructor method of Flask class is the name of
# the module which contains the application and used to look for resources.
minimal_application = Flask(__name__)


# Using the route decorator, the given url is bound to the function. so
# The default content type used by a view function is HTML.
@minimal_application.route('/')
def index():
    return '<h1>This is the index page!</h1>'


# When returning html directly, any user provided input should be escaped in
# order be secure from code injection.
# Variable sections can be added to a url by putting variable names inside <>
# In the given url to flask.
# The view function receives the variable rules as keyword arguments.
# A convertor can be used to specify the type of variable rules existing in
# the url.
# The default convertor used for url variables is string.
@minimal_application.route('/greet/<string:name>/')
def greet(name):
    return f'<h1>Hello, {escape(name)}!</h1>'


# If a url has a trailing slash, accessing the url without a trailing slash
# causes flask to redirect the user to the original url.
# If a url doesn't have a trailing slash, accessing the url with a trailing
# slash results in a 404 erro.


# In order to retriev the url of a veiw function, url_for function can be
# used.
# url_for function accepts the name of a view function as it's first argument
# and accepts any number of keyword arguments to be used as variable rules.
# If a given keyword argument to url_for function doesn't exist in the url of
# the given view function, it will be appended to the returning url as query
# arguments.
# test_request_context is a method of Flask object which tells it to act like
# it is handling a request.
with minimal_application.test_request_context():
    print(url_for('index'))
    print(url_for('greet', name='AmirHossein',
                  sample_unknown_key='sample value'))


# By default, a view function only responses to GET requests.
# In order to specify allowed HTTP methods for requests to be handled, their
# names can be passed as a list to methods argument of the route method.
@minimal_application.route('/postget/', methods=['POST', 'GET'])
def postget():
    return f'<h1>{request.method}</h1>'


# Flask can serve static files using url_for function.
# In order to get static files, the name 'static' should be passed as the
# argument to url_for function along with a keyword argument called filename
# which takes the name or relative path of the static file needed from the
# static directory which should exist next to the module passed to flask as
# import name.
with minimal_application.test_request_context():
    print(url_for('static', filename='styles/main.css'))


# To render a template, render_template function can be used.
# render_template function takes the name of the template and the values
# which should be passed to the template as keyword arguments.
# The template whose name is passed to render_template function should exist
# in the templates directory next to the module passed to flask as import
# name.
# When using flask, config, request, session and g objects can be accessed
# Inside jinja templates, as well as url_for and get_flashed_messages
# functions.
# Templates can inherit from each other.
# In order to use a filter inside a jinja template, the name of the filter
# should come after a pipe symbol which should come after a variable name.
# Jinja2 engine automatically escapes all variables for possible html, for
# trusted sources, safe filter can be used to skip escaping for it.
@minimal_application.route('/gettemplate/<string:title>')
def template(title):
    return render_template('index.html', title=title)
