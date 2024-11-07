def total_inc_dec(x: int) -> int:
    if x in (0, 1, 2):
        return 10 ** x

    return 0


if __name__ == '__main__':
    print(total_inc_dec(0))
