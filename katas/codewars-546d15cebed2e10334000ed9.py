def solve_runes(runes: str) -> int:

    from re import search, findall, match
    from string import digits

    opr = runes[(fe := search(r'^-?[\d,?]+', runes).end()):fe + 1] # type: ignore
    first = runes[:fe]
    second = runes[fe + 1:(se := runes.index('='))]
    result = runes[se + 1:]
    candidates = sorted(set(digits).difference(findall(r'\d', runes)))

    try:
        rm_zero = r'^-?(\?).+'
        if match(rm_zero, first) or match(rm_zero, second) or match(rm_zero, result):
            candidates.remove('0')
    except ValueError:
        pass

    for c in candidates:
        at_first = first.replace('?', c)
        at_second = second.replace('?', c)
        at_result = result.replace('?', c)

        if eval(f'{at_first}{opr}{at_second}') == int(at_result):
            return int(c)

    return -1
