import copy
import itertools
from _pyrepl.completing_reader import complete
from collections import deque, Counter
from collections.abc import Callable
from dataclasses import dataclass, field
from functools import reduce

import numpy as np
from aocd.models import Puzzle
from icecream import ic
from more_itertools import peekable
from numpy.ma.core import empty
from sympy import symbols, Function, Eq, Piecewise
from sympy import solve

f = Function('f')
from sympy.abc import x, y, z, a, b, c, d, e


# @dataclass
# class Stone:
#     value = int = None
#
#     def split


def parse_inputs(input_data):
    start_points = []
    data_points = []
    for y in range(len(input_data)):
        data_rows = []
        for x in range(len(input_data[y])):
            grid_value = int(input_data[y][x])
            if grid_value == 0:
                start_points.append((y, x))
            data_rows.append(grid_value)
        data_points.append(data_rows)
    matrix = np.array(data_points)
    bounds = ic(matrix.shape)
    return bounds, matrix, start_points


def split_string(input_text: str) -> list[str]:
    mid = len(input_text) // 2
    left_half = ''.join(itertools.islice(input_text, mid))
    right_half = ''.join(itertools.islice(input_text, mid, None))
    return [str(int(left_half)), str(int(right_half))]


def part1_solve(input_data: str) -> int:
    stones = input_data.split(" ")
    blink_ops = [
        lambda x: '1' if int(x) == 0 else None,
        lambda x: split_string(x) if len(x) % 2 == 0 else None,
        lambda x: str(int(x) * 2024)
    ]

    for rounds in range(25):
        new_stones = []
        for stone in stones:
            for op in blink_ops:
                current_stones = op(stone)
                if current_stones is None:
                    continue
                if type(current_stones) is list:
                    new_stones.extend(current_stones)
                else:
                    new_stones.append(current_stones)
                break
        # ic(f"{round}: {new_stones}")
        stones = new_stones
    return len(stones)


def part2_solve(input_data: str) -> int:
    bounds, matrix, start_points = parse_inputs(input_data)
    all_paths = {}
    for y, x in start_points:
        paths = {}
        current_stack = deque([(y, x)])
        while current_stack:
            current_y, current_x = current_stack.pop()
            neighbors = [
                (current_y - 1, current_x),
                (current_y + 1, current_x),
                (current_y, current_x - 1),
                (current_y, current_x + 1),
            ]
            current_value = matrix[current_y][current_x]
            if current_value == 9:
                id = f"({current_y},{current_x})"
                current_paths = paths.get(id, None)
                if current_paths is None:
                    paths[id] = [current_stack]
                else:
                    current_paths.append(current_stack)
            for pos_y, pos_x in neighbors:
                if -1 < pos_y < bounds[0] and -1 < pos_x < bounds[1]:
                    if current_value + 1 == matrix[pos_y][pos_x]:
                        current_stack.append((pos_y, pos_x))
        all_paths[f"({y},{x})"] = paths

    total_paths = 0
    for paths in all_paths.values():
        for current_path in paths.values():
            total_paths += len(current_path)
    return total_paths


def main() -> None:
    puzzle = Puzzle(year=2024, day=11)
    input_lines = puzzle.input_data
    example = puzzle.examples.pop()
    example_input = "125 17"

    if int(example.answer_a) == ic(part1_solve(example_input)):
        puzzle.answer_a = ic(part1_solve(input_lines))

    # if 81 == ic(part2_solve(example_input)):
    #     puzzle.answer_b = ic(part2_solve(input_lines))


if __name__ == '__main__':
    main()
