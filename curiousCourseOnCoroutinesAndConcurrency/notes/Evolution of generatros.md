# Evolution of generators

## yield & send

`yield` is now an expression instead of an statement. It has been modified to
accept values from outside of the generator using `send()`. `send` also returns
the next value yielded by the generator, making it a bidirectional communication
channel between the generator & the caller; so passing a generator to `next`
would be the equivalent of calling `send(None)` on it. It also raises
`StopIteration` exception if the generator doesn't yield anything.

## throw

`throw` can be called on a generator to raise a given exception in the
suspension point of the generator. The genrator has the ability to catch the
exception & yield a value in response, or throw an exception (including the
given one) with or without a value. Also returning a value directly will result
in an `StopIteration` exception with the returned value from the generator.

## close

`close` can be called on generators to raise `GeneratorExit` exception
in the suspension point of the generator. If the generator raises
`StopIteration` or `GeneratorException`, the close method returns to it's caller
but other exceptions will be propagated. The close method does nothing if the
generator has alreadyexited.

## Priming

Priming a generator means to pass it `next` once in order for it to reach the
first suspension point; after that, it is possible to send values to it.

## yield from

`yield from` allows using nested generators & extends the communication channel
from the caller to the inner most generator being yielded from. So the caller
can call `throw`, `send` or `close` on the inner generator from outside.
