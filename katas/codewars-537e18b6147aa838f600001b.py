from __future__ import annotations

from math import floor
from typing import NamedTuple, Sequence


def justify(text: str, width: int) -> str:
    if text == '':
        return ''

    if len(text) <= width:
        return text

    return '\n'.join(assemble_lines(get_structure(words := text.split(' '), width), words))


def get_structure(words: Sequence[str], width: int) -> Sequence[LineInfo]:
    words_lengths = [len(w) for w in words]
    out: list[LineInfo] = list()

    llen = 0
    ptr = 0
    strt = 0
    words_num = len(words)
    while ptr < words_num:
        if (wlen := words_lengths[ptr]) + llen > width:
            out.append(LineInfo(strt, ptr, width - (llen - 1)))
            llen = 0
            strt = ptr
        llen += wlen + 1
        ptr += 1

    if (last_end := out[-1][1]) < words_num:
        out.append(LineInfo(last_end, words_num))

    return out


def assemble_lines(lines: Sequence[LineInfo], words: Sequence[str]) -> Sequence[str]:
    out: list[str] = list()
    for ln in lines:
        line_words = words[ln.start_word_index:ln.end_word_index]
        if (num_gaps := (ln.end_word_index - ln.start_word_index) - 1) == 0:
            out.append(line_words[0])
        elif ln.extra_spaces % num_gaps == 0:
            separator = ' ' * ((ln.extra_spaces // num_gaps) + 1)
            out.append(separator.join(line_words))
        else:
            out.append(spread_spaces(line_words, ln))

    return out


def spread_spaces(line_words: Sequence[str], line_info: LineInfo) -> str:
    num_gaps = (line_info.end_word_index - line_info.start_word_index) - 1
    base_gap_length = floor(line_info.extra_spaces / num_gaps) + 1

    pieces: list[str] = list()
    for w in line_words:
        pieces.append(w)
        pieces.append(' ' * base_gap_length)

    pieces.pop()
    gap_index = 1
    plen = len(pieces)
    remainder = (line_info.extra_spaces + num_gaps) - (base_gap_length * num_gaps)
    while remainder > 0:
        pieces[gap_index] += ' '
        remainder -= 1

        if (gap_index := gap_index + 2) > plen:
            gap_index = 1

    return ''.join(pieces)


class LineInfo(NamedTuple):
    start_word_index: int
    end_word_index: int
    extra_spaces: int = 0


if __name__ == '__main__':
    justify('''Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum sagittis dolor mauris, at elementum ligula tempor eget. In quis rhoncus nunc, at aliquet orci. Fusce at dolor sit amet felis suscipit tristique. Nam a imperdiet tellus. Nulla eu vestibulum urna. Vivamus tincidunt suscipit enim, nec ultrices nisi volutpat ac. Maecenas sit amet lacinia arcu, non dictum justo. Donec sed quam vel risus faucibus euismod. Suspendisse rhoncus rhoncus felis at fermentum. Donec lorem magna, ultricies a nunc sit amet, blandit fringilla nunc. In vestibulum velit ac felis rhoncus pellentesque. Mauris at tellus enim. Aliquam eleifend tempus dapibus. Pellentesque commodo, nisi sit amet hendrerit fringilla, ante odio porta lacus, ut elementum justo nulla et dolor.''', 759)
