import copy
import itertools
import sys
from _pyrepl.completing_reader import complete
from collections import deque, Counter
from collections.abc import Callable
from dataclasses import dataclass, field
import time
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


def general_solve(input_data: str, rounds: int) -> int:
    stones = input_data.split(" ")
    blink_ops = [
        lambda x: '1' if int(x) == 0 else None,
        lambda x: split_string(x) if len(x) % 2 == 0 else None,
        lambda x: str(int(x) * 2024)
    ]

    for round in range(rounds):
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
        ic(f"{round}")
        ic(f"{new_stones}")
        stones = new_stones
    return len(stones)


def part1_solve(input_data: str) -> int:
    return general_solve(input_data, 25)


def next_values(op_value: str) -> list[str]:
    blink_ops = [
        lambda x: '1' if int(x) == 0 else None,
        lambda x: split_string(x) if len(x) % 2 == 0 else None,
        lambda x: str(int(x) * 2024)
    ]
    for op in blink_ops:
        current_stones = op(op_value)
        if current_stones is None:
            continue
        if type(current_stones) is list:
            return current_stones
        else:
            return [current_stones]


def run_op(input_values: deque, round_sum: int, all_rounds_sum: int, round: int):
    current_item = input_values.popleft()
    if current_item is None:
        round += 1
        if round == 75:
            return all_rounds_sum + round_sum
    if current_item is None:
        input_values.append(None)
        return run_op(input_values, 0, all_rounds_sum + round_sum, round)
    input_values.extend(next_values(current_item))
    return run_op(input_values, round_sum + 1, all_rounds_sum, round)


def part2_solve(input_data: str) -> int:
    stones = input_data.split(" ")
    current_queue = deque(stones)
    current_queue.append(None)
    all_stones = run_op(current_queue, 0, 0, 0)
    return all_stones


def main() -> None:
    puzzle = Puzzle(year=2024, day=11)
    input_lines = puzzle.input_data
    example = puzzle.examples.pop()
    example_input = "125 17"

    # if int(example.answer_a) == ic(part1_solve(example_input)):
    #     puzzle.answer_a = ic(part1_solve(input_lines))

    sys.setrecursionlimit(1500000)

    ic(part2_solve(example_input))

    # puzzle.answer_b = ic(part2_solve(input_lines))

    # if 81 == ic(part2_solve(example_input)):
    #     puzzle.answer_b = ic(part2_solve(input_lines))


if __name__ == '__main__':
    main()
