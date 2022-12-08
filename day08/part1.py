from __future__ import annotations
from __future__ import absolute_import

import argparse
import os
import sys
import string
import collections

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from support import support

import pytest

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

coords = collections.defaultdict(lambda: -1)


def compute(s: str) -> int:
    notVisible = 0
    
    lines = s.splitlines()
    for x, line in enumerate(s.splitlines()):
        for y, char in enumerate(line):
            coords[(x, y)] = int(char)

    coordsLength = len(coords)
    maxX = coordsLength/len(lines)
    maxY = coordsLength/len(lines[0])

    for pt, n in coords.items():
        if (pt[0] == pt[1] == 0 or pt[0] == maxX-1 or pt[1] == maxY-1):
            continue
        
        sideNotVisibleCounter = 0
        x = pt[0]
        while x > 0:
            x -= 1
            if n <= coords.get((x, pt[1]), -1):
                sideNotVisibleCounter += 1
                break
        x = pt[0]
        while x < maxX:
            x += 1
            if n <= coords.get((x, pt[1]), -1):
                sideNotVisibleCounter += 1
                break
            
        y = pt[1]
        while y > 0:
            y -= 1
            if n <= coords.get((pt[0], y), -1):
                sideNotVisibleCounter += 1
                break
        y = pt[1]
        while y < maxY:
            y += 1
            if n <= coords.get((pt[0], y), -1):
                sideNotVisibleCounter += 1
                break

        if sideNotVisibleCounter == 4:
            notVisible += 1

    coordsLength = len(coords)
    return coordsLength-notVisible


INPUT_S = '''\
30373
25512
65332
33549
35390
'''
EXPECTED = 21


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
