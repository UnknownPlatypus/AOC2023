from __future__ import annotations

import argparse
import os.path
import re

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")

str_to_int = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}

_nb_pattern = re.compile("|".join(str_to_int))


def compute(s: str) -> int:
    tot = 0

    for line in s.splitlines():
        digits = []
        for i in range(len(line)):
            char = line[i]
            if char.isdigit():
                digits.append(int(char))
            elif digit_match := _nb_pattern.match(line[i: i+5]):
                digits.append(str_to_int[digit_match[0]])
        tot += digits[0] * 10 + digits[-1]

    return tot


INPUT_S = """\
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
"""
EXPECTED = 281


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
