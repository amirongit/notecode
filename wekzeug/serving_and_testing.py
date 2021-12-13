from io import BytesIO

from werkzeug.test import Client
from werkzeug.testapp import test_app

# werkzeug provides a Client class to simulate requests to a WSGI application,
# which has methods to make different types of requests and manage cookies.
sample_client = Client(test_app)

# the client request methods return TestResponse objects which provide extra
# attributes and methods on top of Response objects which are useful for
# testing purposes.
response = sample_client.get('/')
print(response.status_code)
print(response.get_data(as_text=True))

# In order to construct the body of client's request, a dictionary can be
# passed to the request method as data parameter.
# Content type header will be set automatically.
response = sample_client.post(data={
        'name': 'test',
        'file': (BytesIO('file contents'.encode('utf-8')), "test.txt")
    })

# To use something as raw request body, it can be passed to data parameter
# directly.
response = sample_client.post(
        data='a: value\nb: 1\n', content_type='application/yaml'
    )


# A dictionary can be passed to json parameter when working with a json API,
# it will be passed to json.dumps and the also the content type will be set
# to "application/json" automatically.
response = sample_client.post('/api', json={'a': 'value', 'b': 1})

# The easiest way to serve a WSGI application for development purposes is to
# use werkzeug.serving.run_simple function.
