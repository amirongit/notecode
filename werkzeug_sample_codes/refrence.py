from werkzeug.exceptions import HTTPException
from werkzeug.routing import Map, Rule, NotFound, RequestRedirect
from werkzeug.wrappers import Response, Request

# The Request and Response objects wrap the WSGI environment or the return
# value from a WSGI application so that it is another WSGI application.
# A WSGI application is always passed two arguments including WSGI environment
# and the WSGI start_response function that is used to start response phase.
# The Request object wraps WSGI environment in order to provide easy access to
# it's variables.
# The Response object is a standard WSGI application that you can instantiate.

basic_application = Response('Hello, World!')


def processing_application(environment, start_response):
    request = Request(environment)
    response = Response(f'Hello, {request.args.get("name", "world")}!')
    return response(environment, start_response)


@Request.application
def high_level_application(request):
    return Response(f'Hello, {request.args.get("name", "world")}!')


# A Map object stores a list of Rule objects which represent url rulse.
# Multiple Rule objects can have the same endpoint but should have different
# arguments to allow url construction.
# A Map object can be binded to an environment in order to get a MapAdapter
# object which can be used to match or build domains for the request.
# The match method of MapAdapter object either returns a tuple including
# endpoint and args or raises an exception.
# Url paths are passed to Rule objects during construction and can have
# convertors for url variables.
# If no convertors is used for a url variables, the default convertor (str)
# will be used.
simple_url_map = Map([Rule('/', endpoint='blog/index'),
                      Rule('/<int:year>/,', endpoint='blog/archive'),
                      Rule('/<int:year>/<int:month>/',
                           endpoint='blog/archive'),
                      Rule('/<int:year>/<int:month>/<int:day>/',
                           endpoint='blog/archive'),
                      Rule('/<int:year>/<int:month>/<int:day>/<slug>/',
                           endpoint='blog/show_post'),
                      Rule('/about/', endpoint='blog/about_me'),
                      Rule('/feeds/', endpoint='blog/feeds'),
                      Rule('/feeds/<feedname>.rss/',
                           endpoint='blog/show_feed')])


def simple_application(environment, start_response):
    urls = simple_url_map.bind_to_environ(environment)
    try:
        endpoint, args = urls.match()
    except HTTPException as e:
        return e(environment, start_response)
    start_response('200 OK', [('Content-type', 'text/plain')])
    return [f'Rule points to {endpoint!r} with arguments {args!r}']


# A custom convertor can be created by subclassing BaseConvertor class.
