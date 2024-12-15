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
class Grid:
    min_x: int = 0
    min_y: int = 0
    max_x: int = 0
    max_y: int = 0


@dataclass
class Point:
    x: int = 0
    y: int = 0


@dataclass
class Move:
    delta_x: int = 0
    delta_y: int = 0

    def slope(self):
        return self.delta_y / self.delta_x


@dataclass
class Robot:
    location: Point = field(default_factory=Point)
    move: Move = field(default_factory=Move)

    def move_next(self, the_grid: Grid):
        next_x = (self.location.x + self.move.delta_x) % the_grid.max_x
        next_y = (self.location.y + self.move.delta_y) % the_grid.max_y
        self.location = Point(next_x, next_y)


def parse_robot(robot_inputs: list[str]) -> Robot:
    start_x, start_y, move_x, move_y = parse("p={:d},{:d} v={:d},{:d}", robot_inputs.strip())
    return Robot(Point(start_x, start_y), Move(move_x, move_y))


def update_blocks(blocks: np.array, robots: list[Robot]) -> None:
    for robot in robots:
        x = robot.location.x
        y = robot.location.y
        current = blocks[y, x]
        blocks[y, x] = current + 1


def move_all(robots: list[Robot], grid: Grid) -> None:
    for robot in robots:
        robot.move_next(grid)

# Make vectors of the start locations as a numpy array and then keep shifting
# in place and mod the positions by the grid bounds
def part2_solve(input_data: list[str], grid: Grid) -> int:
    robots = [parse_robot(x) for x in input_data]
    grid_shape = np.array([grid.max_x, grid.max_y])
    start_locations = np.array([[r.location.x, r.location.y] for r in robots])
    move_vectors = np.array([[r.move.delta_x, r.move.delta_y] for r in robots])
    for step in itertools.count():
        next_positions = (start_locations + step * move_vectors)
        wrapped_positions = next_positions % grid_shape
        if np.unique(wrapped_positions, axis=0).shape == start_locations.shape:
            break
    return step


def within_bounds(robot: Robot, grid_bounds: Grid) -> bool:
    is_in_x = grid_bounds.min_x <= robot.location.x <= grid_bounds.max_x
    is_in_y = grid_bounds.min_y <= robot.location.y <= grid_bounds.max_y
    return is_in_x and is_in_y


def part1_solve(input_data: list[str], grid: Grid, seconds: int) -> int:
    robots = [parse_robot(x) for x in input_data]
    second = 0
    while second < seconds:
        for robot in robots:
            robot.move_next(grid)
        second += 1

    blocks = np.zeros((grid.max_y, grid.max_x))
    update_blocks(blocks, robots)
    midpoint_x = grid.max_x // 2
    midpoint_y = grid.max_y // 2
    blocks[midpoint_y, :] = 0
    blocks[:, midpoint_x] = 0

    quadrants = {
        0: np.sum(blocks[:midpoint_y, :midpoint_x]),
        1: np.sum(blocks[:midpoint_y, midpoint_x:]),
        2: np.sum(blocks[midpoint_y:, :midpoint_x]),
        3: np.sum(blocks[midpoint_y:, midpoint_x:])
    }
    quad_value = ic(reduce(lambda x, y: x * y, quadrants.values()))
    return ic(quad_value)


def main() -> None:
    puzzle = Puzzle(year=2024, day=14)
    input_lines = puzzle.input_data.splitlines()
    input_grid = Grid(max_x=101, max_y=103)
    example = puzzle.examples.pop()
    example_input = example.input_data.splitlines()

    # example_input = "p=2,4 v=2,-3\n".splitlines()
    example_grid = Grid(max_x=11, max_y=7)

    seconds = 100
    if 12 == ic(part1_solve(example_input, example_grid, seconds)):
        puzzle.answer_a = ic(part1_solve(input_lines, input_grid, seconds))

    puzzle.answer_b = ic(part2_solve(input_lines, input_grid))


if __name__ == '__main__':
    main()
