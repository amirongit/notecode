from io import StringIO

from werkzeug.test import create_environ
from werkzeug.wrappers import Request

# The environ dictionary contains all the information which is transmited by
# the request.
# It is passed to the WSGI application.
# Environ dictionary has an item with the key 'wsgi.input' which is a BinaryIO
# object to which represents a low level access to the form data.
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

# url arguments and from data from put and post requests can be accessed
# through Request objects.
# Headers, url argumetns and form data can be accessed in a Request object
# by using it's attributes.
data = 'sample_post_key=sample+post+value'
request_with_data = Request.from_values(
        query_string='sample_arguemtn=sample+value',
        content_length=len(data), input_stream=StringIO(data),
        content_type='application/x-www-form-urlencoded',
        method='POST')
print(f'{request_with_data.args},\n'
      f'{request_with_data.form},\n',
      f'{request_with_data.headers}')
