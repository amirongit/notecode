from datetime import datetime, timezone
from html import escape
from io import StringIO

from werkzeug.test import create_environ
from werkzeug.wrappers import Request, Response
from werkzeug.formparser import parse_form_data


# Request and Response object are high-level APIs to use werkzeug.
# Request.application decorator is used to mark a function as a responder which
# accepts a Request object as it's last argument.


@Request.application
def high_level_app(request):
    result = ['<title>Greeter</title>\n']
    if request.method == 'POST':
        result.append(f'<h1>hello {escape(request.form["name"])}!</h1>\n')
    result.append('<form action="" method="post">\n'
                  '    <p>Name: <input type="text" name="name" size="20">\n'
                  '    <input type="submit" value="Greet me">\n'
                  '</form>')
    return Response(''.join(result), mimetype='text/html')


def low_level_app(environ, start_response):
    result = ['<title>Greeter</title>\n']
    if environ['REQUEST_METHOD'] == 'POST':
        form = parse_form_data(environ)[1]
        result.append(f'<h1>Hello {escape(form["name"])}!</h1>\n')
    result.append('<form action="" method="post">\n'
                  '    <p>Name: <input type="text" name="name" size="20">'
                  '    <input type="submit" value="Greet me">'
                  '</form>')
    start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])
    return [''.join(result).encode('utf-8')]


# The environ dictionary contains all the information which is transmited by
# the request.
# It is passed to the WSGI application.
# Environ dictionary has an item with the key 'wsgi.input' which is a BinaryIO
# object which represents a low level access to the form data.
# Data in environ dictionary is encoded.
sample_environ = create_environ()
print(f'{sample_environ["PATH_INFO"]},'
      f' {sample_environ["SERVER_NAME"]},'
      f' {sample_environ["REQUEST_METHOD"]},')

# The Request object wraps the environ and provides a read-only access to the
# data.
# Data in Request object is decoded where it makes sense.
# Also form data is parsed and put in Request object.
# Some of information about the request exists in Request object as attributes
# like path, host, url, method and ...
sample_request = Request(sample_environ)
print(f'{sample_request.path},'
      f' {sample_request.server},'
      f' {sample_request.method}')

# Headers, url argumetns and form data from put and post requests can be
# accessed through Request object's attributes.
data = 'sample_post_key=sample+post+value'
request_with_data = Request.from_values(
        query_string='sample_arguemtn=sample+value',
        content_length=len(data), input_stream=StringIO(data),
        content_type='application/x-www-form-urlencoded',
        method='POST')
print(f'{request_with_data.args}\n'
      f'{request_with_data.form}\n'
      f'{request_with_data.headers}')


typical_environ = create_environ()
typical_environ.update(
    HTTP_ACCEPT='text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q='
    '0.8',
    HTTP_ACCEPT_LANGUAGE='de-at,en-us;q=0.8,en;q=0.5',
    HTTP_ACCEPT_ENCODING='gzip,deflate',
    HTTP_ACCEPT_CHARSET='ISO-8859-1,utf-8;q=0.7,*;q=0.7',
    HTTP_IF_MODIFIED_SINCE='Fri, 20 Feb 2009 10:10:25 GMT',
    HTTP_IF_NONE_MATCH='"e51c9-1e5d-46356dc86c640"',
    HTTP_CACHE_CONTROL='max-age=0')
typical_request = Request(typical_environ)

# With some HTTP headers the browser infroms web application what kinds of
# mimtypes, languages, encodings and charsets it can accept in order of the
# quality of handle.
# These headers can be accessed through Request object's attributes.
print(f'{typical_request.accept_mimetypes}\n'
      f'{typical_request.accept_languages}\n'
      f'{typical_request.accept_encodings}\n'
      f'{typical_request.accept_charsets}')

# Response objects are used to send data back to the client.
# Response objects should be called as a WSGI application inside a WSGI
# application and the returned value of that call should be returned.


def sample_application(environ, start_response):
    '''
    So Response objects are a kind of lower level WSGI app, the original one.
    It returns what a WSGI app should return, and then, it's return value
    should be returned by the high level WSGI app.
    '''
    response = Response('sample content')
    return response(environ, start_response)


# Response object are designed to be modified, so their accessors are not
# read only.
sample_response = Response('sample content')
sample_response.headers['content-length'] = len(sample_response.data)

# If status attribute of a Response object gets modified, it' status_code
# attribute will change too, and it's the same in reverse.
sample_response.status_code = 200
print(sample_response.status)
sample_response.status = '404 Not Found'
print(sample_response.status_code)

# Common headers are exposed as attributes in Response objects and there are
# methods to assign a value to some of them.
sample_response.set_etag('sample etag', weak=True)

# Most of the content headers are sets values and are mutables.
sample_response.content_language.add('en-US')

# Content headers can be set bydirectional through attributes and the
# dictionary stored in header attribute.
print(sample_response.headers['Content-language'])
sample_response.headers['Content-language'] = 'fa-IR'
print(sample_response.content_language)


# In order to set cookies on a Response object, set_cookie method can be
# called on it.
sample_response.set_cookie('sample_key', 'sample_value')

# In order to get all of the values for an specific header, getlist method
# can be called on header attribute of a Response object.
sample_response.content_language.add('en-UK')
print(sample_response.headers.getlist('Content-language'))


# A Response object can be made conditional against a request by calling
# make_conditional method on it after setting an etag and date.
sample_response.date = datetime(2009, 2, 20, 17, 42, 51, tzinfo=timezone.utc)
sample_response.make_conditional(sample_request)
