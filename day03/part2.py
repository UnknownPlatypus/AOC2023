from __future__ import annotations

import argparse
import math
import os.path
import re
from collections import defaultdict
from pprint import pprint

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")

digit_regex = re.compile(r"\d*")


def compute(s: str) -> int:
    print()
    symbols = {}
    for y, line in enumerate(s.splitlines()):
        for x, c in enumerate(line):
            if c == "*":
                symbols[(x, y)] = c

    match = defaultdict(set)
    for y, line in enumerate(s.splitlines()):
        for x, c in enumerate(line):
            if c.isdigit():
                for point_x, point_y in support.adjacent_8(x, y):
                    if (point_x, point_y) in symbols:
                        next_digits = digit_regex.search(line[x + 1 :])[0]
                        previous_digits = digit_regex.search(line[:x:][::-1])[0]
                        nb = int(f"{previous_digits[::-1]}{c}{next_digits}")
                        start_of_nb_coord = (x - len(previous_digits), y)
                        match[(point_x, point_y)].add((start_of_nb_coord, nb))
    return sum(
        math.prod(val[1] for val in vals) for vals in match.values() if len(vals) == 2
    )


INPUT_S = """\
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
"""
EXPECTED = 467835


@pytest.mark.parametrize(
    ("input_s", "expected"),
    ((INPUT_S, EXPECTED),),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("data_file", nargs="?", default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
