import copy
import enum
import functools
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
from scipy.signal import correlate, correlate2d
from shapely.geometry.polygon import Polygon, LinearRing
from sympy import symbols, Function, Eq, Piecewise, nsolve
from sympy import solve
from sympy.codegen.fnodes import Program

f = Function('f')
from sympy.abc import x, y, z, a, b, c, d, e

def node_label(y: int, x: int) -> str:
    return f'{y},{x}'

def find_path(current_grid: np.ndarray, start_node, end_node, cheat_nodes: list[str] = []) -> networkx.Graph:
    moves = [
        (0, -1),  # left
        (-1, 0),  # up
        (0, 1),  # right
        (1, 0)  # down
    ]

    wall = '#'
    g = nx.Graph()
    max_y_bounds = current_grid.shape[0] - 1
    max_x_bounds = current_grid.shape[1] - 1

    for (y, x), input_value in np.ndenumerate(current_grid):
        if input_value == wall and node_label(y, x) not in cheat_nodes:
            continue
        current_node = node_label(y, x)
        if g.has_node(current_node) is False:
            g.add_node(current_node, name=input_value)
        for move in moves:
            next_y, next_x = y + move[0], x + move[1]
            if next_y < 0 or next_y > max_y_bounds:
                continue
            if next_x < 0 or next_x > max_x_bounds:
                continue
            next_pos_value = current_grid[next_y][next_x]
            next_node = node_label(next_y, next_x)
            if next_pos_value != wall:
                if g.has_node(next_node) is False:
                    g.add_node(next_node, name=input_value)
                g.add_edge(current_node, next_node)
    return nx.shortest_path(g, start_node, end_node)


def find_cheat_blocks(the_grid: np.array, pattern: np.array) -> List[Tuple[int, int]]:
    matches = correlate2d(the_grid.astype(str), pattern.astype(str), mode='valid', fillvalue='#')
    return matches




def part1_solve(input_lines: list[str], max_saving: int) -> int:
    grid_size = len(input_lines) - 2
    input_grid = np.zeros((grid_size, grid_size), dtype=str)

    for y in range(grid_size):
        for x in range(grid_size):
            input_grid[y, x] = input_lines[y + 1][x + 1]

    start_y, start_x = np.where(input_grid == 'S')
    end_y, end_x = np.where(input_grid == 'E')

    start_node = node_label(start_y[0],start_x[0])
    end_node = node_label(end_y[0],end_x[0])
    shortest_path = find_path(input_grid, start_node, end_node)
    shortest_path_length = len(shortest_path) - 1

    cheat_paths = {}

    valid_blocks = ['.', 'E', 'S']

    up_down_cheat_blocks = []
    for y in range(grid_size):
        for x in range(1, grid_size - 1):
            if input_grid[y][x] == '#' and input_grid[y, x - 1] in valid_blocks and input_grid[y, x + 1] in valid_blocks:
                up_down_cheat_blocks.append(node_label(y, x))
    for cheat_block in up_down_cheat_blocks:
        cheat_block_path = find_path(input_grid, start_node, end_node, [cheat_block])
        current_path_length = len(cheat_block_path) - 1
        if current_path_length < shortest_path_length:
            path_saving = shortest_path_length - current_path_length
            if path_saving <= max_saving:
                paths_count = cheat_paths.get(path_saving, 0)
                cheat_paths[path_saving] = paths_count + 1

    left_right_cheat_blocks = []
    for y in range(1, grid_size - 1):
        for x in range(grid_size):
            if input_grid[y][x] == '#' and input_grid[y - 1, x] in valid_blocks and input_grid[y + 1, x] in valid_blocks:
                left_right_cheat_blocks.append(node_label(y, x))
    for cheat_block in left_right_cheat_blocks:
        cheat_block_path = find_path(input_grid, start_node, end_node, [cheat_block])
        current_path_length = len(cheat_block_path) - 1
        if current_path_length < shortest_path_length:
            path_saving = shortest_path_length - current_path_length
            if path_saving <= max_saving:
                paths_count = cheat_paths.get(path_saving, 0)
                cheat_paths[path_saving] = paths_count + 1
    ic(cheat_paths)

    valid_cheats = sum([paths for saving, paths in cheat_paths.items()])
    # up_down = np.array([
    #     ['.'],
    #     ['#'],
    #     ['.']
    # ], dtype=str)
    # up_down_cheat_blocks = find_cheat_blocks(input_grid, up_down)
    # left_right = find_cheat_blocks(input_grid, np.array([['.','#','.']]))
    return valid_cheats


def part2_solve(input_segments: list[str]) -> int:
    return general_solve(input_segments, True)


def main() -> None:
    puzzle = Puzzle(year=2024, day=20)
    input_lines = puzzle.input_data.splitlines()
    example = puzzle.examples.pop()
    example_input = example.input_data.splitlines()

    if 44 == ic(part1_solve(example_input, 100)):
        puzzle.answer_a = ic(part1_solve(input_lines, 100))

    # if 16 == ic(part2_solve(example_input)):
    #     puzzle.answer_b = ic(part2_solve(input_lines))


if __name__ == '__main__':
    main()
