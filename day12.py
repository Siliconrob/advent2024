import copy
import itertools
import sys
from _pyrepl.completing_reader import complete
from collections import deque, Counter
from collections.abc import Callable
from dataclasses import dataclass, field
import time
from functools import reduce, cache

import numpy as np
from aocd.models import Puzzle
from icecream import ic
from more_itertools import peekable
from numpy.ma.core import empty
from sympy import symbols, Function, Eq, Piecewise
from sympy import solve

f = Function('f')
from sympy.abc import x, y, z, a, b, c, d, e


@cache
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
        stones = new_stones
    return len(stones)


def part1_solve(input_data: str) -> int:
    return general_solve(input_data, 25)


@cache
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


# This is still too big because it keeps a large queue in memory while it works off of it
# def run_op(input_values: deque, round_sum: int, all_rounds_sum: int, round: int):
#     current_item = input_values.popleft()
#     if current_item is None:
#         round += 1
#         if round == 74:
#             return all_rounds_sum + round_sum
#     if current_item is None:
#         input_values.append(None)
#         return run_op(input_values, 0, all_rounds_sum + round_sum, round)
#     input_values.extend(next_values(current_item))
#     return run_op(input_values, round_sum + 1, all_rounds_sum, round)


@cache
def run_op(current_stone: str, current_round: int, total_rounds: int) -> int:
    if current_round == total_rounds:
        return 1
    current_round += 1
    if current_stone == '0':
        return run_op('1', current_round, total_rounds)
    if len(current_stone) % 2 == 1:
        return run_op(str(int(current_stone) * 2024), current_round, total_rounds)
    segments = split_string(current_stone)
    return run_op(segments[0], current_round, total_rounds) + run_op(segments[1], current_round, total_rounds)


def part2_solve(input_data: str) -> int:
    stones = input_data.split(" ")
    all_stones = 0
    current_queue = deque(stones)
    while current_queue:
        current_item = current_queue.popleft()
        if current_item is None:
            break
        all_stones += run_op(current_item, 0, 75)
    return all_stones


def main() -> None:
    puzzle = Puzzle(year=2024, day=12)
    input_lines = puzzle.input_data
    example = puzzle.examples.pop()
    example_input = "125 17"

    sys.setrecursionlimit(1500000)

    if int(example.answer_a) == ic(part1_solve(example_input)):
        puzzle.answer_a = ic(part1_solve(input_lines))

    ic(part2_solve(example_input))
    puzzle.answer_b = ic(part2_solve(input_lines))


if __name__ == '__main__':
    main()
