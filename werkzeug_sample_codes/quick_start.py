from werkzeug.test import create_environ
from werkzeug.wrappers import Request
print('environ')
environ = create_environ('/foo', 'http://localhost:8080/')
print(environ['PATH_INFO'])
print(environ['SCRIPT_NAME'])
print(environ['SERVER_NAME'])

print('request')
req = Request(environ)
print(req.path)
print(req.script_root)
print(req.host)
print(req.url)
print(req.method)
