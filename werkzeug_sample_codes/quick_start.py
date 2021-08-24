from io import StringIO

from werkzeug.test import create_environ
from werkzeug.wrappers import Request, Response

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
