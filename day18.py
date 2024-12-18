import copy
import enum
import itertools
import sys
from _pyrepl.completing_reader import complete
from collections import deque, Counter
from collections.abc import Callable
from copy import deepcopy
from dataclasses import dataclass, field
import time
from functools import reduce, cache
from heapq import heappop, heappush
from typing import Tuple, List

import networkx
import networkx as nx
import numpy as np
from aocd.models import Puzzle
from icecream import ic
from more_itertools import peekable, strip
from more_itertools.recipes import flatten, pairwise
from numpy.f2py.auxfuncs import throw_error
from numpy.ma.core import empty, masked_array
from parse import parse
from scipy import ndimage
from shapely.geometry.polygon import Polygon, LinearRing
from sympy import symbols, Function, Eq, Piecewise, nsolve
from sympy import solve
from sympy.codegen.fnodes import Program

f = Function('f')
from sympy.abc import x, y, z, a, b, c, d, e


def find_path(current_grid: np.ndarray) -> networkx.Graph:
    moves = [
        (0, -1),  # left
        (-1, 0),  # up
        (0, 1),  # right
        (1, 0)  # down
    ]

    wall = '#'

    graph = nx.Graph()
    g = nx.Graph()
    max_y_bounds = current_grid.shape[0] - 1
    max_x_bounds = current_grid.shape[1] - 1
    start_node = f'0,0'
    end_node = f'{max_y_bounds},{max_x_bounds}'

    for (y, x), input_value in np.ndenumerate(current_grid):
        if input_value == wall:
            continue
        current_node = f'{y},{x}'
        if g.has_node(current_node) is False:
            g.add_node(current_node, name=input_value)
        for move in moves:
            next_y, next_x = y + move[0], x + move[1]
            if next_y < 0 or next_y > max_y_bounds:
                continue
            if next_x < 0 or next_x > max_x_bounds:
                continue
            next_pos_value = current_grid[next_y][next_x]
            next_node = f'{next_y},{next_x}'
            if next_pos_value != wall:
                if g.has_node(next_node) is False:
                    g.add_node(next_node, name=input_value)
                g.add_edge(current_node, next_node)
    return nx.shortest_path(g, start_node, end_node)


def part1_solve(input_data: str, grid_size: int, steps: int) -> int:
    input_grid = np.zeros((grid_size, grid_size), dtype=str)
    for coord in input_data:
        if steps == 0:
            break
        x, y = parse("{:d},{:d}", coord)
        input_grid[y, x] = '#'
        steps -= 1
    path = find_path(input_grid)
    return len(path) - 1


def part2_solve(input_data: str, grid_size: int) -> str:
    input_grid = np.zeros((grid_size, grid_size), dtype=str)

    blocking_coord = None
    for coord in input_data:
        x, y = parse("{:d},{:d}", coord)
        input_grid[y, x] = '#'
        try:
            path = find_path(input_grid)
        except networkx.exception.NetworkXNoPath:
            blocking_coord = coord
            break
    return blocking_coord


def main() -> None:
    puzzle = Puzzle(year=2024, day=18)
    input_lines = puzzle.input_data.splitlines()
    example = puzzle.examples.pop()
    example_input = example.input_data.splitlines()

    # if 22 == ic(part1_solve(example_input, 7, 12)):
    #     puzzle.answer_a = ic(part1_solve(input_lines, 71, 1024))

    if "6,1" == ic(part2_solve(example_input, 7)):
        puzzle.answer_b = ic(part2_solve(input_lines, 71))


if __name__ == '__main__':
    main()
