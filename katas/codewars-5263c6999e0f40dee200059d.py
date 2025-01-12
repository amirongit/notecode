from itertools import product
from typing import cast

PANEL: tuple[tuple[int | None, ...], ...] = (
    (1, 2, 3),
    (4, 5, 6),
    (7, 8, 9),
    (None, 0, None)
)


def get_pins(observed: str) -> list[str]:
    out: list[str] = list()
    for p in product(*tuple(resolve_adj(int(k)) for k in observed)):
        code = ''
        for digit in p:
            code += str(digit)
        out.append(code)
    return out

def resolve_adj(num: int) -> tuple[int, ...]:
    row = PANEL[row_idx := ((num - 1) // 3) if num != 0 else 3]
    col_idx = PANEL[row_idx].index(num)
    (out := list(row if col_idx == 1 else row[1:] if col_idx == 2 else row[:2])).extend(
        [
            PANEL[1][col_idx]
        ] if row_idx == 0 else [
            PANEL[2][col_idx]
        ] if row_idx == 3 else [
            PANEL[row_idx + 1][col_idx],
            PANEL[row_idx - 1][col_idx]
        ]
    )
    return cast(tuple[int, ...], tuple(filter(lambda n: n is not None, out)))
