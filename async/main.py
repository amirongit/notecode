# Evenet loops
# Programmin constructs or design patterns which dispatch events or messages in a program. they work by making a request
# to an event provider which usually blocks the request untill an event has arrvied and then call the relevant event
# handler. In other words, they have the ability to put tasks in a queue & put them on the call stack when it's empty.
# Event loops take unit of works (also called coroutine or a task) containing requests, event providers & event handlers
# & process them step by step concurrently.

# Coroutines
# It is possible to implement coroutines using generators (althogh coroutines have their own syntax).
# The yield keyword is now an expression instead of an statement. It has been modified to accept values from the outside
# of the generator using send() method.
# The send method also returns the next value yielded by the generator; making yield a bidirectional communication
# channel between the generator and the caller. It also raises an StopIteration exception if the generator doesn't yield
# anything. Passing a generator to next function is equivalent to calling send(None) on it.
# A method called throw can be called on a generator to raise a given exception in the suspension point of the
# generator. The genrator has the ability to catch the exception and yield a value in response, or throw an exception
# (including the given exception) with or without a value. Also returning a value directly will result an StopIteration
# exception with a value.
# The close method can be called on generators to raise a GeneratorExit exception in the suspension point of the
# generator. If the generator raises StopIteration or GeneratorException, the close method returns to it's caller & if
# it raises any other exceptions, the exception will be propagated. The close method does nothing if the generator has
# already exited.
# Priming a generator means to pass it to the next function once in order to reach the first suspension point and get
# the yielded value. Then it is possible to send a value to the generator.
