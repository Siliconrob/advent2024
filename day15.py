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


def parse_inputs(input_data: str, doubled: bool = False) -> Tuple[np.ndarray, deque[str]]:
    input_segments = input_data.split("\n\n")
    movements = deque(input_segments.pop())
    input_map = input_segments.pop().splitlines()
    grid = []
    for row in input_map:
        if doubled is False:
            grid.append(list(row))
        else:
            input_map_row = list(row)
            doubled_row = []
            for input in input_map_row:
                if input == "@":
                    doubled_row.append("@")
                    doubled_row.append(".")
                else:
                    if input == "O":
                        doubled_row.append("[")
                        doubled_row.append("]")
                    else:
                        doubled_row.append(input)
                        doubled_row.append(input)
            grid.append(doubled_row)
    map = np.array(grid, dtype=str)
    return map, movements

def part2_solve(input_data: str) -> int:
    map, movements = parse_inputs(input_data, True)

    wall = '#'
    left_box = '['
    right_box = ']'
    robot = '@'

    empty = '.'

    def get_robot_pos():
        robot_y, robot_x = np.where(map == robot)
        return robot_y[0], robot_x[0]

    moves = {
        "<": (0, -1),  # left
        "^": (-1, 0),  # up
        ">": (0, 1),  # right
        "v": (1, 0)  # down
    }

    while movements:
        next_move = movements.popleft()
        if not next_move in moves:
            continue
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
            move_line = map[:, robot_pos[1]][robot_pos[0] + 1:]

        empties = np.where(move_line == empty)[0]
        if len(empties) == 0:
            continue

        swap_index = None
        start = len(move_line) - 2 if direction == -1 else 1
        end = -1 if direction == -1 else len(move_line)
        for i in n_range(start, end):
            current_item = move_line[i]
            if current_item == wall:
                break
            if current_item == box:
                continue
            swap_index = i
            break

        if swap_index is None:
            continue

        move_line[swap_index] = box
        map[next_pos[0]][next_pos[1]] = robot
        map[robot_pos[0]][robot_pos[1]] = empty

    boxes = np.where(map == box)
    gps_coords = {}
    for location in list(zip(boxes[0], boxes[1])):
        gps_coords[(location[0], location[1])] = location[0] * 100 + location[1]
    return sum(gps_coords.values())


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
        "<": (0, -1),  # left
        "^": (-1, 0),  # up
        ">": (0, 1),  # right
        "v": (1, 0)  # down
    }

    while movements:
        next_move = movements.popleft()
        if not next_move in moves:
            continue
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
            move_line = map[:, robot_pos[1]][robot_pos[0] + 1:]

        empties = np.where(move_line == empty)[0]
        if len(empties) == 0:
            continue

        swap_index = None
        start = len(move_line) - 2 if direction == -1 else 1
        end = -1 if direction == -1 else len(move_line)
        for i in n_range(start, end):
            current_item = move_line[i]
            if current_item == wall:
                break
            if current_item == box:
                continue
            swap_index = i
            break

        if swap_index is None:
            continue

        move_line[swap_index] = box
        map[next_pos[0]][next_pos[1]] = robot
        map[robot_pos[0]][robot_pos[1]] = empty

    boxes = np.where(map == box)
    gps_coords = {}
    for location in list(zip(boxes[0], boxes[1])):
        gps_coords[(location[0], location[1])] = location[0] * 100 + location[1]
    return sum(gps_coords.values())


def n_range(start, stop):
    return range(start, stop, int(abs(stop - start) / (stop - start)))


def main() -> None:
    puzzle = Puzzle(year=2024, day=15)
    input_lines = puzzle.input_data
    example = puzzle.examples.pop()
    example_input = example.input_data

    limited_example_input = """########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<"""

    # if 2028 == ic(part1_solve(limited_example_input)) and 10092 == ic(part1_solve(example_input)):
    #     puzzle.answer_a = ic(part1_solve(input_lines))

    part_example_input = """#######
#...#.#
#.....#
#..OO@#
#..O..#
#.....#
#######

<vv<<^^<<^^"""

    ic(part2_solve(part_example_input))


if __name__ == '__main__':
    main()
