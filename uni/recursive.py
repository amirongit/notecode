def factorial(x: int) -> int:
    if x != 0:
        return x * factorial(x - 1)
    return 1


print(f'''
factorial(5): {factorial(5)}
    5 * factorial(4) => 120
        4 * factorial(3) => 24
            3 * factorial(2) => 6
                2 * factorial(1) => 2
                  1 * factorial(0) => 1
''')


def fibonacci(x: int) -> int:
    if x == 0 or x == 1:
        return x
    return fibonacci(x - 1) + fibonacci(x - 2)


print(f'''
fibonacci(5): {fibonacci(5)}
    fibonacci(4) + fibonacci(3) => 5
        (fibonacci(3) + fibonacci(2)) + (fibonacci(2) + fibonacci(1)) => (2 + \
1) + (1 + 1) => 5
        fibonacci(3) => 2
            fibonacci(2) + fibonacci(1) => 2
        fibonacci(2) => 1
            fibonacci(1) + fibonacci(0) => 1
''')
