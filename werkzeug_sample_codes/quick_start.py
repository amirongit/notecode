from werkzeug.test import create_environ
from werkzeug.wrappers import Request

# The environ dictionary contains all the information which is transmited by
# the request.
# It is passed to the WSGI application.
# Environ dictionary doesn't provide anyway to access the form data.
# Data in environ dictionary is encoded.
sample_environ = create_environ(method='POST')

# The Request object wraps the environ and provides a read-only access to the
# data.
# Data in Request object is decoded where it makes sense.
# Also form data is parsed and put in Request object.
sample_request = Request(sample_environ)
