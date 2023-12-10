from __future__ import annotations

import argparse
import math
import os.path

import pytest
from tqdm import tqdm

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def compute(s: str) -> int:
    print("\n")
    lines = s.splitlines()
    race_time = int(lines[0].split(": ")[1].replace(" ", ""))
    race_distance = int(lines[1].split(": ")[1].replace(" ", ""))

    # Let's do the math this time, but brute forcing was working too in ~2s
    #
    # travel_time = race_time - btn_time                             (1)
    # race_distance = travel_time * btn_time                         (2)
    # travel_dst = (race_time - btn-time) * btn_time
    # btn_time^2 - race_time * btn_time + race_distance = 0          (3)

    # Solving this quadratic equations we get 2 roots:
    #   R1 / R2 = race_time +- math.sqrt(race_time * race_time - 4 * race_distance))/2

    R1 = math.floor(
        (race_time + math.sqrt(race_time * race_time - 4 * race_distance) / 2)
    )
    R2 = math.ceil(
        (race_time - math.sqrt(race_time * race_time - 4 * race_distance) / 2)
    )

    return R1 - R2 + 1


INPUT_S = """\
Time:      7  15   30
Distance:  9  40  200
"""
EXPECTED = 71503


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
