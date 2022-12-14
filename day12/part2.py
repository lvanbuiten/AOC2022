from __future__ import annotations
from __future__ import absolute_import

import argparse
import os
import sys
import string
import collections
import heapq

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from support import support

import pytest

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    coords = {}
    S = E = None
    for x, line in enumerate(s.splitlines()):
        for y, char in enumerate(line):
            coords[(x, y)] = char
            if char == 'S':
                S = (x, y)
            if char == 'E':
                E = (x, y)

    maxX, maxY = max(coords)

    s_queue = [S]
    s_seen = set()
    startpos = [S]
    while s_queue:
        c = s_queue.pop(0)
        for nb in support.adjacent_4_in_range(*c, maxX, maxY):
            if nb in s_seen:
                continue
            currentElevation = 0 if c == S else string.ascii_letters.index(coords.get(c))
            nextElevation = string.ascii_letters.index(coords.get(nb))
            if currentElevation == nextElevation == 0:
                s_queue.append(nb)
                startpos.append(nb)
                s_seen.add(nb)
                pass
    
    levels = []
    while startpos:
        pos = startpos.pop(0)
        seen = set(pos)
        queue = [(0, pos)]
        level = 0

        while queue:
            level, c = heapq.heappop(queue)
            if c == E:
                levels.append(level)
                queue = []
                break

            for nb in support.adjacent_4_in_range(*c, maxX, maxY):
                if nb in seen:
                    continue
                currentElevation = 0 if c == S else string.ascii_letters.index(coords.get(c))
                nextElevation = 25 if E == nb else string.ascii_letters.index(coords.get(nb))
                if nextElevation <= currentElevation+1:
                    seen.add(nb)
                    heapq.heappush(queue, (level+1, nb))

    return min(levels)


INPUT_S = '''\
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
'''
EXPECTED = 29


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
