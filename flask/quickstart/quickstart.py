from markupsafe import escape

from flask import (Flask, url_for, request, render_template, redirect,
                   make_response, abort, session, flash)
from werkzeug.utils import secure_filename

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
@minimal_application.route('/template/')
def template():
    return render_template('index.html', title='Quickstart')


# some objects in flask are global objects which can be used inside a view
# function and still be unique for each thread handling a request; this happens
# using contexts; in fact, these objects are proxies to local variables of some
# special contexts and won't work as excepted outside of these contexts.
# request and session objects need to be used inside a request context to work
# properly.
# g and current_app objects need to be used inside an application context to
# work properly.


# By default, a view function only responses to GET requests.
# In order to specify allowed HTTP methods for requests to be handled, their
# names can be passed as a list to methods argument of the route method.
# Form data which is sent by a POST or PUT request can be accessed through form
# attribute of the request object.
# Parameters which are submitted in the url, can be accessed through args
# attribute of the request object.
# Uploaded files can be accessed through file attribute of the request object.
# Retrieved file object from file attribute of the request object acts like a
# normal python file object, but it also has a save method.
# Name of the files should never be trusted, if it is needed to use the
# original name of the uploaded file, it should be secured.
# werkzeug.utils.secure_filename function can be used in order to secure the
# name of a file.
# In order to redirect a client to another view function, redirect function
# can be used.
@minimal_application.route('/form/')
def form():
    post_input = request.args.get('post_input')
    get_input = request.args.get('get_input')
    post_upload = request.args.get('post_upload')
    return render_template('form.html', title='Make Get/Post Request',
                           get_input=get_input, post_input=post_input,
                           post_upload=post_upload)


@minimal_application.route('/formdata/', methods=['GET', 'POST'])
def formdata():
    if request.method == 'GET':
        return redirect(
                url_for('form', get_input=request.args.get('get_input')))
    if request.method == 'POST':
        if request.files.get('post_upload'):
            return redirect(url_for('form',
                                    post_input=request.form.get('post_input'),
                                    post_upload=secure_filename(
                                        request.files.get(
                                            'post_upload').filename)))
        return redirect(url_for('form',
                                post_input=request.form.get(
                                    'post_input')))


# Cookies which is transmited by the client can be accessed through cookie
# attribute of the request object.
# In order to set a cookie, a Response object should be created using
# make_response function which returns a Response object which should be
# returned by the view function, and then set_cookie method can be called on
# the returning response object.
# In ordert to remove a cookie, set_cookie method can be called on the
# returning response object, with 0 passed to "max_age" keyword argument.
@minimal_application.route('/cookie_set/', methods=['GET', 'POST'])
def cookie_set():
    if request.method == 'POST':
        resp = make_response(redirect(url_for('cookie_set')))
        resp.set_cookie('cookie', request.form.get('cookie'))
        return resp
    return render_template('cookie_set.html')


@minimal_application.route('/cookie_unset/')
def cookie_unset():
    resp = make_response(redirect(url_for('cookie_set')))
    resp.set_cookie('cookie', '', max_age=0)
    return resp


# In order to abort a request early with an error code, abort function can be
# used.
# If abort function gets executed inside a view function, the rest of the code
# of the view function won't be executed.
@minimal_application.route('/get_not_found/')
def get_not_found():
    abort(404)


# In order to customize a default error page, error_handler decorator can be
# used.
@minimal_application.errorhandler(404)
def page_not_found(error):
    return render_template('not_found.html'), 404


# Flask automatically converts the return value of a view function to a
# response object.
# Flask's logic in converting return values to response objects are as follow:
# Response object -> returned directly from the view
# str -> Response object with a body containing str data
# dict -> Response object produced using jsonify
# tuple -> valid formats : (response, status), (response, headers)
# (response, status, headers)
# none of the above -> assuming it's a valid WSGI application, it is returned
# directly


# The session object is used to store information specific to a user from one
# request to the next; it is implemented on top of cookies, and signed using
# the secret key.
# FLASK SESSION IS NOT SECURE.
minimal_application.secret_key = 'TH1515453CR3TK3Y'


@minimal_application.route('/session_set/', methods=['GET', 'POST'])
def session_set():
    if request.method == 'POST':
        session['session'] = request.form.get('session')
        return redirect(url_for('session_set'))
    return render_template('session_set.html')


@minimal_application.route('/session_unset/')
def session_unset():
    session.pop('session')
    return redirect(url_for('session_set'))


# In order to flash a message and access it in the (only) next request, flash
# function can be used.
# In order to access the flashed messages, get_flashed_messages function can be
# used both in templates and code.
@minimal_application.route('/msg_flash/', methods=['GET', 'POST'])
def msg_flash():
    if request.method == 'POST':
        flash(request.form.get('msg'))
        return redirect(url_for('msg_flash'))
    return render_template('msg_flash.html')
