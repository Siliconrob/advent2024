import copy
import itertools
import sys
from _pyrepl.completing_reader import complete
from collections import deque, Counter
from collections.abc import Callable
from dataclasses import dataclass, field
import time
from functools import reduce, cache
from typing import Tuple

import numpy as np
from aocd.models import Puzzle
from icecream import ic
from more_itertools import peekable, strip
from more_itertools.recipes import flatten, pairwise
from numpy.ma.core import empty, masked_array
from parse import parse
from scipy import ndimage
from shapely.geometry.polygon import Polygon, LinearRing
from sympy import symbols, Function, Eq, Piecewise, nsolve
from sympy import solve

f = Function('f')
from sympy.abc import x, y, z, a, b, c, d, e


@dataclass
class PrizeLocation:
    X: int = 0
    Y: int = 0


@dataclass
class ButtonMove:
    Name: str = None
    MoveX: int = 0
    MoveY: int = 0
    TokenCost: int = 0


@dataclass
class ClawGame:
    ButtonA: ButtonMove = field(default_factory=ButtonMove)
    ButtonB: ButtonMove = field(default_factory=ButtonMove)
    Prize: PrizeLocation = field(default_factory=PrizeLocation)

    def solve(self) -> Tuple[int, int]:
        x, y = symbols('x y')
        ax = self.ButtonA.MoveX
        ay = self.ButtonA.MoveY
        bx = self.ButtonB.MoveX
        by = self.ButtonB.MoveY
        ans1 = self.Prize.X
        ans2 = self.Prize.Y

        equation1 = Eq(ax * x + bx * y, ans1)
        equation2 = Eq(ay * x + by * y, ans2)
        solution = solve((equation1, equation2), (x, y))

        x_count = solution[x]
        y_count = solution[y]
        if x_count.is_Integer and y_count.is_Integer:
            return x_count * self.ButtonA.TokenCost + y_count * self.ButtonB.TokenCost
        return None


def parse_button(button_input: str, tokens: int) -> ButtonMove:
    button, x, y = parse("Button {:w}: X={:d}, Y={:d}", button_input.replace("+", "=").strip())
    return ButtonMove(button, x, y, tokens)


def parse_game(game_inputs: list[str]) -> ClawGame:
    buttonA = parse_button(game_inputs[0], 3)
    buttonB = parse_button(game_inputs[1], 1)
    x, y = parse("Prize: X={:d}, Y={:d}", game_inputs[2])
    prize = PrizeLocation(x, y)
    return ClawGame(buttonA, buttonB, prize)


def part2_solve(input_data_groups: list[str]) -> int:
    game_inputs = [line_group.splitlines() for line_group in input_data_groups]
    pass


def part1_solve(input_data_groups: list[str]) -> int:
    games = [parse_game(line_group.splitlines()) for line_group in input_data_groups]
    winning_games = {}
    for game_index in range(len(games)):
        game = games[game_index]
        game_result = ic(game.solve())
        if game_result is not None:
            winning_games[game_index + 1] = game_result
    return ic(sum(winning_games.values()))


def main() -> None:
    puzzle = Puzzle(year=2024, day=13)
    input_lines = puzzle.input_data.split("\n\n")
    example = puzzle.examples.pop()
    example_input = example.input_data.split("\n\n")

    if 480 == ic(part1_solve(example_input)):
        puzzle.answer_a = ic(part1_solve(input_lines))

    # if 1206 == ic(part2_solve(example_input)):
    #     puzzle.answer_b = ic(part2_solve(input_lines))


if __name__ == '__main__':
    main()
