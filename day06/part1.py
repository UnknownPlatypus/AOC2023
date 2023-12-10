from __future__ import annotations

import argparse
import math
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def compute(s: str) -> int:
    print("\n")
    fin = 1
    lines = s.splitlines()
    times = [int(v) for v in lines[0].split(": ")[1].split()]
    distances = [int(v) for v in lines[1].split(": ")[1].split()]

    for time, dst in zip(times, distances):
        tot = 0
        for i in range(0, time):
            if (time - i) * i > dst:
                tot += 1
        print(tot)
        fin *= tot
    return fin


def compute_with_math(s: str) -> int:
    print("\n")
    fin = 1
    lines = s.splitlines()
    times = [int(v) for v in lines[0].split(": ")[1].split()]
    distances = [int(v) for v in lines[1].split(": ")[1].split()]

    for time, dst in zip(times, distances):
        R1 = math.floor((time + math.sqrt(time * time - 4 * dst) / 2))
        R2 = math.ceil((time - math.sqrt(time * time - 4 * dst) / 2))
        fin *= R1 - R2 + 1
    return fin


INPUT_S = """\
Time:      7  15   30
Distance:  9  40  200
"""
EXPECTED = 288


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
        # print(compute(f.read()))  # brute force
        # f.seek(0)
        print(compute_with_math(f.read()))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
