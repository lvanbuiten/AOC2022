from __future__ import annotations
from __future__ import absolute_import

import argparse
import os
import sys
import string

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from support import support

import pytest

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    count=0
    lines = s.splitlines()
    for line in lines:
        elf1,elf2 = line.split(',')
        b1,e1 = [int(i) for i in elf1.split('-')]
        b2,e2 = [int(i) for i in elf2.split('-')]

        p1 = set([i for i in range(b1, e1+1)])
        p2 = set([i for i in range(b2, e2+1)])

        if len(p1 - p2) < len(p1) or len(p2 - p1) < len(p2):
            #print(f"Found line {line}, {p1}, {p2}")
            count += 1

    return count


INPUT_S = '''\
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
'''
EXPECTED = 4


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
