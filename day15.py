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

# f = Function('f')
# from sympy.abc import x, y, z, a, b, c, d, e


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


def parse_inputs(input_data: str) -> Tuple[np.ndarray, deque[str]]:
    input_segments = input_data.split("\n\n")
    movements = deque(input_segments.pop())
    input_map = input_segments.pop().splitlines()
    grid = []
    for row in input_map:
        grid.append(list(row))

    map = np.array(grid, dtype=str)
    return (map, movements)

# def get_data(next_pos: Tuple[int, int], movement: str, the_map: np.ndarray) -> np.ndarray:


def part1_solve(input_data: str) -> int:
    map, movements = parse_inputs(input_data)

    wall = '#'
    box = 'O'
    robot = '@'
    empty = '.'

    def get_robot_pos():
        robot_y, robot_x = np.where(map == robot)
        return robot_y[0], robot_x[0]

    moves = {
        "<": (0, -1), # left
        "^": (-1, 0), # up
        ">": (0, 1), # right
        "v": (1, 0) # down
    }

    while movements:
        next_move = movements.popleft()
        move_action = moves[next_move]
        robot_pos = get_robot_pos()
        next_pos = (move_action[0] + robot_pos[0], move_action[1] + robot_pos[1])
        next_pos_data = map[next_pos[0]][next_pos[1]]
        if next_pos_data == wall:
            continue
        if next_pos_data == empty:
            map[robot_pos[0]][robot_pos[1]] = empty
            map[next_pos[0]][next_pos[1]] = robot
            continue

        direction = 1
        move_line = None
        if next_move == '>':
            move_line = map[robot_pos[0]][robot_pos[1] + 1:]
        if next_move == '<':
            move_line = map[robot_pos[0]][:robot_pos[1]]
            direction = -1
        if next_move == '^':
            direction = -1
            move_line = map[:, robot_pos[1]][0:robot_pos[0]]
        if next_move == 'v':
            move_line = map[:,robot_pos[1]][robot_pos[0] + 1:]

        empties = np.where(move_line == empty)[0]
        if len(empties) == 0:
            continue
        swap_index = 0


        for i in range(1, len(move_line)):
            current_item = move_line[i]
            if direction == -1:
                current_item = reversed(move_line)[i]
            if current_item == wall:
                break
            if current_item == box:
                continue
            swap_index = i
            break
        move_line[swap_index] = box
        map[next_pos[0]][next_pos[1]] = robot
        map[robot_pos[0]][robot_pos[1]] = empty
    return 0



def main() -> None:
    puzzle = Puzzle(year=2024, day=15)
    input_lines = puzzle.input_data
    example = puzzle.examples.pop()
    example_input = example.input_data

    # example_input = "p=2,4 v=2,-3\n".splitlines()

    limited_example_input = """########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<"""

    ic(part1_solve(limited_example_input))

    # if (2028 == ic(part1_solve(limited_example_input))) and (10092 == ic(part1_solve(example_input))):
    #     puzzle.answer_a = ic(part1_solve(input_lines))

    # if 81 == ic(part2_solve(example_input)):
    #     puzzle.answer_b =
    return


if __name__ == '__main__':
    main()
