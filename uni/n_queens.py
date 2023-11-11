from typing import TypeAlias


Board: TypeAlias = list[int]


def solve(board: Board, side: int = 4, column: int = 1) -> Board:
    pass


def is_safe(board: Board, column: int, row: int) -> bool:


    if row in board or column < len(board):
        return False

    for b_column, b_row in enumerate(board):
        if (row - column == b_row - b_column) or (row + column == b_row + b_column):
            return False

    return True


def draw_board(board: Board) -> str:

    size = max(board) + 1
    cells = [['-' for _ in range(size)] for _ in range(size)]

    for column, row in enumerate(board):
        cells[row][column] = 'Q'

    return '\n'.join([' '.join(c) for c in cells])

