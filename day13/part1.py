from __future__ import annotations
from __future__ import absolute_import

import argparse
import ast
import itertools
import os
import sys
import string
import collections
import math

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from support import support

import pytest

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

def compare(left: any, right: any) -> int:
    if isinstance(left, int) and not isinstance(right, int):
        left = [left]
    if not isinstance(left, int) and isinstance(right, int):
        right = [right]

    if isinstance(left, int) and isinstance(right, int):
        return right - left
    elif isinstance(left, list) and isinstance(right, list):
        for l, r in itertools.zip_longest(left, right):
            if l is None:
                return 1
            if r is None:
                return -1

            compared = compare(l, r)
            if compared != 0:
                return compared
        else:
            return 0 # sub list only had similar int's
    else:
        raise AssertionError('Whut is this?')
            
def compute(s: str) -> int:
    pairs = s.split('\n\n')
    indices = []

    for pI,p in enumerate(pairs, start=1):
        leftS, rightS = p.splitlines()
        left = ast.literal_eval(leftS)
        right = ast.literal_eval(rightS)

        if compare(left, right) > 0:
            indices.append(pI)

    print(f'Indices is {indices}')
    return sum(indices)


INPUT_S = '''\
[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]
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
