from __future__ import annotations

import argparse
import itertools
import os.path
from multiprocessing import Pool
from typing import Iterator

import pytest
from tqdm import tqdm

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def _compute(args) -> int:
    print(f"compute for range {args[1]}")
    min_val = float("inf")
    for seed in args[1]:
        for chunk_lookups in args[0]:
            for dest, source, length in chunk_lookups:
                if source <= seed < source + length:
                    seed = (seed - source) + dest
                    break
        min_val = min(min_val, seed)
    return min_val


def create_chunks(seeds: list[int], chunk_size=10_000_000) -> Iterator[range]:
    ranges = itertools.batched(seeds, 2)
    for start, length in ranges:
        nb, remainder = divmod(length, chunk_size)
        for _ in range(nb):
            yield range(start, start + chunk_size)
            start = start + chunk_size
        yield range(start, start + remainder)


def compute(s: str) -> int:
    print("\n")
    chunks = s.split("\n\n")
    seeds = [int(seed) for seed in chunks[0].split(": ")[1].split()]

    lookups = []
    for chunk in chunks[1:]:
        chunk_lookups = []
        for line in chunk.splitlines()[1:]:
            dest, source, length = map(int, line.split())
            chunk_lookups.append((dest, source, length))
        lookups.append(chunk_lookups)

    with Pool() as pool:
        results = tqdm(
            pool.imap_unordered(
                _compute, zip(itertools.repeat(lookups), create_chunks(seeds))
            )
        )
        return min(results)


INPUT_S = """\
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
"""
EXPECTED = 46


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
