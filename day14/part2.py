from __future__ import annotations
from __future__ import absolute_import

import argparse
import copy
import os
import sys
import string
import collections
import math

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from support import support

import pytest

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

def compute(s: str) -> int:
    start = (500, 0)
    coords = {}
    for line in s.splitlines():
        values = line.split(' -> ')
        for i in range(len(values)-1):
            c = tuple([int(x) for x in values[i].split(',')])
            n = tuple([int(x) for x in values[i+1].split(',')])
            diffX, diffY = abs(n[0]-c[0]), abs(n[1]-c[1])
            m = min([c,n])

            for x in range(diffX+1):
                coords[(m[0]+x, m[1])] = '#'
            for y in range(diffY+1):
                coords[(m[0], m[1]+y)] = '#'
    
    #print(support.format_coords_hash_values(coords))

    startX = min(x for x, _ in coords)
    endX = max(x for x, _ in coords)
    startY = min(y for _, y in coords)
    endY = max(y for _, y in coords) + 2

    unitCount = 0
    while True:
        c = copy.copy(start)
        canMove = True
        while canMove:
            #check below
            if c[1]+1 < endY and coords.get((c[0], c[1]+1), '.') == '.':
                c = (c[0], c[1]+1)
            #check below left
            elif c[1]+1 < endY and coords.get((c[0]-1, c[1]+1), '.') == '.':
                c = (c[0]-1, c[1]+1)
            #check below left
            elif c[1]+1 < endY and coords.get((c[0]+1, c[1]+1), '.') == '.':
                c = (c[0]+1, c[1]+1)
            else:
                unitCount += 1
                coords[c] = 'O'
                if c == start:
                    break
                canMove = False
                #print(support.format_coords_hash_values(coords))
        if canMove:
            # end everything
            #print(f'Breaking')
            break

    #print(support.format_coords_hash_values(coords))
    return unitCount


INPUT_S = '''\
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
'''
EXPECTED = 93


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
