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

    tails = [(0, 0)] * 10
    tVisited.append(tails[-1])

    lines = s.splitlines()
    for line in lines:
        d, cS = line.split() # direction and count(string)
        c = int(cS)

        for _ in range(c):
            h = tails[0]
            if d == 'U':
                h = (h[0]-1, h[1])
            if d == 'D':
                h = (h[0]+1, h[1])
            if d == 'L':
                h = (h[0], h[1]-1)
            if d == 'R':
                h = (h[0], h[1]+1)
            tails[0] = h

            for i in range(1, len(tails)):
                prev = tails[i-1] 
                cur = tails[i]
                #isAdjecent = True if t in support.adjacent_8_including(prev[0], prev[1]) else False
                if cur not in support.adjacent_8_including(prev[0], prev[1]):
                    diffX = prev[0]-cur[0]
                    diffY = prev[1]-cur[1]
                    if (abs(diffX) > 1):
                        if (diffX < 0):
                            diffX += 1
                        else:
                            diffX -= 1
                    if (abs(diffY) > 1):
                        if (diffY < 0):
                            diffY += 1
                        else:
                            diffY -= 1
                    tails[i] = (cur[0]+diffX, cur[1]+diffY)
                    #print(f'Difference is x {x}, y {y}')
                    if tails[-1] not in tVisited:
                        tVisited.append(tails[-1])
            
            #print(f'H is at {h}')
            #print(f'Tail is at {tails}')
        print(f'Current potition is {tails[-1]}, line is {line}')
        print(f'Tail is at {tails}')
    #print(f'Visited {tVisited}')
    return len(tVisited)


INPUT_S = '''\
R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20
'''
EXPECTED = 36


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
