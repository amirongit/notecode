def encode(s: str) -> tuple[str, int]:
    if s == '':
        return ('', 0)

    ring = s
    shifts: list[str] = list()
    for turn in range(len(s)):
        shifts.append(ring)
        ring = ring[-1] + ring[:-1]
    shifts.sort()
    return (''.join(s[-1] for s in shifts), shifts.index(s))


def decode(s: str, n: int) -> str:
    if s == '':
        return ''

    fs = sorted(s)
    ft = {c: 0 for c in fs}
    st = {c: 0 for c in s}
    fcol: list[tuple[str, int]] = list()
    lcol: list[tuple[str, int]] = list()
    for c in fs:
        ft[c] += 1
        fcol.append((c, ft[c]))
    for c in s:
        st[c] += 1
        lcol.append((c, st[c]))
    original: list[str] = list()
    pointer = fcol[n]
    for _ in range(len(s)):
        original.append(pointer[0])
        pointer = fcol[lcol.index(pointer)]
    return ''.join(original)
