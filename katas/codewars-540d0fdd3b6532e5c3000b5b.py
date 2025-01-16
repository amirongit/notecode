from __future__ import annotations

from itertools import groupby
from typing import NamedTuple, cast


def expand(expr: str) -> str:
    '''given expr will alway be in the form of: (ax+b)^n'''
    ax, b, n = decompose(expr)
    if n == 0:
        return '1'
    result: list[Term] = [ax, b]
    for multiplier in range(n - 1):
        new_result: list[Term] = list()
        for multiplicand in result:
            new_result.append(Term(
                b.coefficient * multiplicand.coefficient,
                multiplicand.variable,
                multiplicand.exponent
            ))
            new_result.append(Term(
                multiplicand.coefficient * ax.coefficient,
                ax.variable,
                1 if multiplicand.variable is None else multiplicand.exponent + 1
            ))
        result = new_result
    return to_string(*condense(*result))


def decompose(expr: str) -> tuple[Term, Term, int]:
    inside = (no_pre := expr.removeprefix('('))[:no_pre.index(')')]
    a_end = 0 if inside[0] != '-' else 1
    while inside[a_end].isdigit():
        a_end += 1
    a = 1 if (s := inside[:a_end]) == '' else -1 if s == '-' else int(s)
    x = inside[a_end]
    b = int(inside[a_end + 1:])
    return (Term(a, x), Term(b), int(expr[expr.index('^') + 1:]))


def condense(*terms: Term) -> list[Term]:
    expr_degree = max(t.exponent for t in terms)
    variable = next(iter(filter(lambda t: t.variable is not None, terms))).variable
    out: list[Term] = list()
    for exponent in range(expr_degree, 0, -1):
        coefficient = 0
        for t in filter(lambda t: t.variable is not None and t.exponent == exponent, terms):
            coefficient += t.coefficient
        out.append(Term(coefficient, variable, exponent))
    out.append(Term(sum(t_.coefficient for t_ in filter(lambda t: t.variable is None, terms))))
    return out


def to_string(*terms: Term) -> str:
    out = ''
    for vt in sorted(filter(lambda t: t.variable is not None, terms), key=lambda t: t.exponent, reverse=True):
        out += ('+' if vt.coefficient > 1 else '') + (
            '-' if vt.coefficient == -1 else str(vt.coefficient) if vt.coefficient != 1 else ''
        ) + cast(str, vt.variable) + (('^' + str(vt.exponent)) if vt.exponent > 1 else '')
    final_coefficient = next(iter(filter(lambda t: t.variable is None, terms))).coefficient
    return (out + (('+' + str(final_coefficient)) if final_coefficient > 0 else str(final_coefficient))).removeprefix(
        '+'
    )

class Term(NamedTuple):
    coefficient: int = 1
    variable: str | None = None
    exponent: int = 1
