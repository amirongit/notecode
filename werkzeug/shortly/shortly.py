import os
import redis
from werkzeug.serving import run_simple
from werkzeug.urls import url_parse
from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule
from werkzeug.exceptions import HTTPException, NotFound
from werkzeug.middleware.shared_data import SharedDataMiddleware
from werkzeug.utils import redirect
from jinja2 import Environment, FileSystemLoader

# An Instance of this class will be a callables which can be used as a WSGI
# application.


class Shortly:
    def __init__(self, config):
        self.redis = redis.Redis(config['redis_host'], config['redis_port'])
        template_path = os.path.join(os.path.dirname(__file__), 'templates')
        self.jinja_env = Environment(loader=FileSystemLoader(template_path),
                                     autoescape=True)
        # Map object is used to store url rules.
        # Rule object is used to represent a url rule.
        self.url_map = Map([Rule('/', endpoint='new_url'),
                            Rule('/<short_id>',
                                 endpoint='follow_short_link'),
                            Rule('/<short_id>+',
                                 endpoint='short_link_details')])

    def render_template(self, template_name, **context):
        t = self.jinja_env.get_template(template_name)
        # A Response object can be created by instantiating Response class.
        return Response(t.render(context), mimetype='text/html')

    def dispath_request(self, request):
        # A MapAdapter is created by binding a Map object with an environ
        # dictionary.
        adapter = self.url_map.bind_to_environ(request.environ)
        try:
            # MapAdapter object is used to match the binded url in order to
            # get find an endpoint for it.
            # Url arguments are passed along with the endpoint.
            endpoint, values = adapter.match()
            return getattr(self, f'on_{endpoint}')(request, **values)
        except HTTPException as e:
            return e

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.dispath_request(request)
        # A Response object can be called to be processed as a WSGI
        # application.
        return response(environ, start_response)

    def __call__(self, environ, start_response):
        # start_response is a callable which is explained here.
        # https://stackoverflow.com/questions/16774952/
        # It is a deprecated function which led us write our applications as
        # generators and is kept for backward compatibality.
        # It is used to begin a HTTP response.
        # The recommended way is to pass it status code and headers of the
        # response before returning it's body from the application.
        # Headers should be passed in the form of a list of tuples which are
        # made of a single key value pair.
        # New frameworks should avoid using start_response.
        return self.wsgi_app(environ, start_response)

    def on_new_url(self, request):
        error = None
        url = str()
        if request.method == 'POST':
            url = request.form['url']
            if not is_valid_url(url):
                error = 'please enter a valid url'
            else:
                short_id = self.insert_url(url)
                return redirect(f'/{short_id}+')
        return self.render_template('new_url.html', error=error, url=url)

    def on_follow_short_link(self, request, short_id):
        link_target = self.redis.get(f'url-target:{short_id}')
        if link_target is None:
            raise NotFound()
        self.redis.incr(f'click_count:{short_id}')
        return redirect(link_target.decode('utf-8'))

    def on_short_link_details(self, request, short_id):
        link_target = self.redis.get(f'url-target:{short_id}')
        if link_target is None:
            raise NotFound()
        click_count = int(self.redis.get(f'click_count:{short_id}') or 0)
        return self.render_template('short_link_details.html',
                                    link_target=link_target,
                                    short_id=short_id,
                                    click_count=click_count)

    def insert_url(self, url):
        short_id = self.redis.get(f'reverse-url:{url}')
        if short_id is not None:
            return short_id
        url_num = self.redis.incr('last-url-id')
        short_id = base36_encode(url_num)
        self.redis.set(f'url-target:{short_id}', url)
        self.redis.set(f'reverse-url:{url}', short_id)
        return short_id


def is_valid_url(url):
    parts = url_parse(url)
    return parts.scheme in ('http', 'https')


def base36_encode(number):
    assert (number > 0), 'positive integer required'
    if number == 0:
        return '0'
    base36 = list()
    while number != 0:
        number, i = divmod(number, 36)
        base36.append('0123456789abcdefghijklmnopqrstuvwxyz'[i])
    return ''.join(reversed(base36))


def create_app(redis_host='localhost', redis_port=6379, with_static=True):
    app = Shortly({'redis_host': redis_host,
                   'redis_port': redis_port})
    if with_static:
        app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
            '/static': os.path.join(os.path.dirname(__file__), 'static')})
    return app


if __name__ == '__main__':
    app = create_app()
    run_simple('127.0.0.1', 5000, app, use_debugger=True, use_reloader=True)
