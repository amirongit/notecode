def dbl_linear(n: int) -> int:

    seq = [1]

    for i in range(n * 5):
        seq.append(2 * seq[i] + 1)
        seq.append(3 * seq[i] + 1)

    return sorted(set(seq))[n]
