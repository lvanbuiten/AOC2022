from __future__ import annotations
from __future__ import absolute_import

import argparse
import math
import os
import sys
import string

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from support import support

import pytest

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

def compute(s: str) -> int:
    tVisited = []

    h = (0, 0)
    t = (0, 0)
    tVisited.append(t)

    lines = s.splitlines()
    for line in lines:
        d, cS = line.split() # direction and count(string)
        c = int(cS)

        for _ in range(c):
            if d == 'U':
                h = (h[0]-1, h[1])
            if d == 'D':
                h = (h[0]+1, h[1])
            if d == 'L':
                h = (h[0], h[1]-1)
            if d == 'R':
                h = (h[0], h[1]+1)

            isAdjecent = True if t in support.adjacent_8_including(h[0], h[1]) else False
            if not isAdjecent:
                diffX = h[0]-t[0]
                diffY = h[1]-t[1]
                if (abs(diffX) > 1):
                    if (diffX < 0):
                        diffX += 1
                    else:
                        diffX -= 1
                else:
                    if (diffY < 0):
                        diffY += 1
                    else:
                        diffY -= 1
                t = (t[0]+diffX, t[1]+diffY)
                if t not in tVisited:
                    tVisited.append(t)
    return len(tVisited)


INPUT_S = '''\
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
'''
EXPECTED = 13


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
