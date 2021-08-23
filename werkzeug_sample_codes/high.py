from html import escape
from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple

# Request and Response object are high-level APIs to use werkzeug.

# Request.application decorator is used to mark a function as a responder which
# accepts a Request object as it's last argument.


@Request.application
def hello_world(request):
    result = ['<title>Greeter</title>\n']
    if request.method == 'POST':
        result.append(f'<h1>hello {escape(request.form["name"])}!</h1>\n')
    result.append('<form action="" method="post">\n'
                  '    <p>Name: <input type="text" name="name" size="20">\n'
                  '    <input type="submit" value="Greet me">\n'
                  '</form>')
    return Response(''.join(result), mimetype='text/html')


if __name__ == '__main__':
    run_simple('127.0.0.1', 5000, hello_world,
               use_reloader=True, use_debugger=True)
