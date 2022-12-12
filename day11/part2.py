from __future__ import annotations
from __future__ import absolute_import

import argparse
import os
import sys
import string
from dataclasses import dataclass
from typing import List
import math

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from support import support

import pytest

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


@dataclass
class Monkey:
    #index: int
    items: list[int]
    operation: str
    test: int # divisble by ..
    true: int
    false: int
    inspected: int
    #gcd

def compute(s: str) -> int:
    monkeys: List[Monkey] = []

    monkeyStr = s.split('\n\n')
    for mS in monkeyStr:
        lines = mS.splitlines()
        #index = int(lines[0][-2])
        items = [int(x) for x in lines[1].split(': ')[1].split(', ')]
        operation = lines[2].split('= ')[1]
        test = int(lines[3].split()[-1])
        true = int(lines[4].split()[-1])
        false = int(lines[5].split()[-1])

        monkeys.append(Monkey(items, operation, test, true, false, 0))

    gdc = 1
    for m in monkeys:
        gdc = gdc * m.test


    for _ in range(10000):
        for i, m in enumerate(monkeys):
            count = len(m.items)
            m.inspected += count
            for _ in range(count):
                item = m.items.pop(0)
                itemValue = int(eval(m.operation.replace('old', str(item))) % gdc) #math.gcd(monkeys[m.true].test, monkeys[m.false].test))
                to = m.true if (itemValue % m.test == 0) else m.false
                monkeys[to].items.append(itemValue)

                #print(f'Monkey {i} : Item with worry level {itemValue} is thrown to monkey {to}.')

                #m.inspected += 1
    
    result = math.prod(sorted([x.inspected for x in monkeys], reverse=True)[:2])
    
    print(f'Here monkeys: {monkeys}')
    return result


INPUT_S = '''\
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
'''
EXPECTED = 2713310158


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
