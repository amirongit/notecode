from typing import Union, List

from dataclasses import dataclass, field
from datetime import datetime
from random import choice

from blacksheep import Application, Request, json

app = Application()


@app.route('/route')
def route(): return f'Hello, world! - {datetime.utcnow().isoformat()}'


@app.router.get('/router')
def router(): return 'THIS IS A GET REQUEST!'


@app.router.get('/params/{name}')
def accept_param(name): return f'Hello, {name}!'


@app.router.get('/plustwo/{number}')
def plustwo(number: int): return number + 2


@app.router.get('/multiply')
def multiply(f: int, s: int = 2): return f * s


@app.router.get('/sum')
def sum_(num: List[float]): return sum(num)


@app.router.get('/getreq')
def getreq(req: Request): return str(req.url) + ' ' + str(req.query)


@dataclass
class FooModel:
    bar: int = field(default_factory=lambda: choice((1, 0)))
    baz: int = field(default_factory=lambda: choice((1, 0)))


@app.router.get('/getresources')
def getresources(): return json([FooModel(), FooModel()])


@app.router.get('/getresourcesasync')
async def getresourcesasync(): return json([FooModel(), FooModel()])


