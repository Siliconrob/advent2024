import copy
import itertools
from _pyrepl.completing_reader import complete
from collections import deque, Counter
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
        file_blocks = list(itertools.repeat(id, length))
        current_file_blocks = [*current_file_blocks, *file_blocks]
        if current_empties:
            empty_blocks = list(itertools.repeat(None, next(current_empties)))
            current_file_blocks = [*current_file_blocks, *empty_blocks]
    while None in current_file_blocks:
        sizeof = len(current_file_blocks)
        location = current_file_blocks.index(None)
        last_item = current_file_blocks[-1]
        current_file_blocks[location] = last_item
        current_file_blocks = current_file_blocks[:sizeof - 1]
    return current_file_blocks


def part1_solve(input_data: str) -> int:
    current_fs = parse_input(input_data)
    compressed_files = move_blocks(current_fs)
    checksum = sum([index * compressed_files[index] for index in range(len(compressed_files))])
    return checksum


def move_files(input_fs: FileSystem) -> list[int]:
    blocks_table = {}
    current_empties = peekable(input_fs.emtpy_blocks)

    def empties_key(id: int) -> str:
        return f"empties_{id}"

    last_block = 0
    for (id, length) in input_fs.files.items():
        blocks_table[id] = list(itertools.repeat(id, length))
        if current_empties:
            blocks_table[empties_key(id)] = list(itertools.repeat(None, next(current_empties)))
        last_block += 1

    last_block -= 1

    # Moved blocks turn into empties so need to figure that out
    while last_block > 1:
        for index in range(len(input_fs.emtpy_blocks)):
            current_empty = blocks_table[empties_key(index)]
            if index - 1 >= last_block or not None in current_empty:
                continue
            current_file_blocks = blocks_table.get(last_block, None)
            file_stats = Counter(current_empty)
            if current_file_blocks is None:
                break
            if file_stats.get(None) < len(current_file_blocks):
                continue
            current_file_blocks = blocks_table.pop(last_block)
            while len(current_file_blocks) > 0:
                current_file_block = current_file_blocks.pop()
                current_empty[current_empty.index(None)] = current_file_block
        last_block -= 1

    flat_blocks = [item for sublist in blocks_table.values() for item in sublist]
    return flat_blocks


def part2_solve(input_data: str) -> int:
    current_fs = parse_input(input_data)
    compressed_files = move_files(current_fs)
    checksum = sum([index * compressed_files[index] for index in range(len(compressed_files)) if
                    compressed_files[index] is not None])
    return checksum


def main() -> None:
    puzzle = Puzzle(year=2024, day=9)
    input_lines = puzzle.input_data
    example = puzzle.examples.pop()
    example_input = example.input_data

    # if int(example.answer_a) == ic(part1_solve(example_input)):
    #     puzzle.answer_a = ic(part1_solve(input_lines))

    if 2858 == ic(part2_solve(example_input)):
        puzzle.answer_b = ic(part2_solve(input_lines))


if __name__ == '__main__':
    main()
