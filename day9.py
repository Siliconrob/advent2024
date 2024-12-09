import copy
import itertools
from _pyrepl.completing_reader import complete
from collections import deque
from collections.abc import Callable
from dataclasses import dataclass, field
from functools import reduce
from aocd.models import Puzzle
from icecream import ic
from more_itertools import peekable
from numpy.ma.core import empty
from sympy import symbols, Function, Eq, Piecewise
from sympy import solve

f = Function('f')
from sympy.abc import x, y, z, a, b, c, d, e


@dataclass
class FileSystem:
    files: dict = field(default_factory=dict)
    emtpy_blocks: list[int] = field(default_factory=list)


def parse_input(input_line: str) -> FileSystem:
    fs = FileSystem()
    current_file_index = 0
    for index in range(len(input_line)):
        current_item = int(input_line[index])
        if index % 2 == 0:
            fs.files[current_file_index] = current_item
            current_file_index += 1
            continue
        fs.emtpy_blocks.append(current_item)
    return fs


def move_blocks(input_fs: FileSystem) -> list[int]:
    current_file_blocks = []
    current_empties = peekable(input_fs.emtpy_blocks)
    for (id, length) in input_fs.files.items():
        file = "".join([str(z) for z in list(itertools.repeat(id, length))])
        current_file_blocks.append(file)
        if current_empties:
            empties = "".join(list(itertools.repeat('.', next(current_empties))))
            current_file_blocks.append(empties)

    complete = list("".join(current_file_blocks))
    while '.' in complete:
        sizeof = len(complete)
        location = complete.index('.')
        complete[location] = complete[-1]
        complete = complete[:sizeof - 1]

    blocks = [int(index) for index in complete]
    return blocks


def part1_solve(input_data: str) -> int:
    current_fs = parse_input(input_data)
    compressed_files = move_blocks(current_fs)
    checksum = sum([index * compressed_files[index] for index in range(len(compressed_files))])
    return checksum


def part2_solve(input_data: list[str]) -> int:
    pass


def main() -> None:
    puzzle = Puzzle(year=2024, day=9)
    input_lines = puzzle.input_data
    example = puzzle.examples.pop()
    example_input = example.input_data

    if int(example.answer_a) == ic(part1_solve(example_input)):
        puzzle.answer_a = ic(part1_solve(input_lines))

    # if 34 == ic(part2_solve(example_input)):
    #     puzzle.answer_b = ic(part2_solve(input_lines))


if __name__ == '__main__':
    main()
