from html import escape
from werkzeug.formparser import parse_form_data
from werkzeug.serving import run_simple


def hello_world(environ, start_response):
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

# TODO: find out what is wsgi.input


if __name__ == '__main__':
    run_simple('127.0.0.1', 5000, hello_world,
               use_reloader=True, use_debugger=True)
