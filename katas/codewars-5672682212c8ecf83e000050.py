def dbl_linear(n: int) -> int:
    yfunc = lambda x: 2 * x + 1
    zfunc = lambda x: 3 * x + 1

    seq = [1]

    for i in range(n * 5):
        seq.append(yfunc(seq[i]))
        seq.append(zfunc(seq[i]))

    return sorted(set(seq))[n]
