from __future__ import annotations
from __future__ import absolute_import

import argparse
import os
import sys
import string
import copy
from typing import List
from dataclasses import dataclass, field

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from support import support

import pytest

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

MAX = 100000
totalSize = 0

@dataclass
class Node:
    dir: str
    parent: Node
    childNodes: List[Node] = field(default_factory=list)
    files: dict[str, int] = field(default_factory=dict)

def compute(s: str) -> int:
    root = Node('/', None)
    current = root
    lines = s.splitlines()
    for line in lines[1:]:
        #print(f'{line}')
        parts = line.split()
        if (parts[0] == '$'):
            #command
            if (parts[1] == 'cd'):
                if (parts[2] == '..'):
                    #up
                    current = current.parent
                else:
                    #down
                    for child in current.childNodes:
                        if child.dir == parts[2]:
                            current = child
                            break
                pass
            elif (parts[1] == 'ls'):
                pass
        elif (str.isnumeric(parts[0])):
            #file
            current.files[parts[1]] = int(parts[0])
        elif (parts[0] == 'dir'):
            #dir
            current.childNodes.append(Node(parts[1], Node(current.dir, current.parent, current.childNodes, current.files)))
    
    #print(f'Tree is {root}')

    def size(current: Node):
        global totalSize
        cSize = 0

        #print(f'current {current.dir}')
        for child in current.childNodes:
            cSize += size(child)
        
        for f in current.files.values():
            #print(f'Filesize is {f}')
            cSize += f

        if (cSize <= MAX):
            #print(f'Size is smaller than {MAX}, current {current.dir}, size {cSize}')
            totalSize += cSize
        

        return cSize
    
    size(root)
    return totalSize


INPUT_S = '''\
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
'''
EXPECTED = 95437


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
