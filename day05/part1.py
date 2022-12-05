from __future__ import annotations
from __future__ import absolute_import

import argparse
import os
import sys
import string
import math

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from support import support

import pytest

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> str:
    s = s.replace("move ", "").replace("from ", "").replace("to ", "")

    stacksStr, actions = s.split('\n\n')
    stacks = [ [] for i in range(10) ] #assume 9 stacks

    for stackStr in stacksStr.splitlines():
        for i,s in enumerate(stackStr):
            if str.isalpha(s):
                stackIndex = math.ceil(i/4)
                stacks[stackIndex].insert(0, s)

    for a in actions.splitlines():
        c,f,t = [int(x) for x in a.split()]
        for m in range(c):
            stacks[t].append(stacks[f].pop())

    result = ''
    for i in range(len(stacks)):
        if len(stacks[i]) > 0:
            result += stacks[i].pop()

    return result

INPUT_S = '''\
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
'''
EXPECTED = 'CMZ'


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
