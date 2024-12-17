import copy
import itertools
import sys
from _pyrepl.completing_reader import complete
from collections import deque, Counter
from collections.abc import Callable
from dataclasses import dataclass, field
import time
from functools import reduce, cache
from heapq import heappop, heappush
from typing import Tuple

import networkx
import networkx as nx
import numpy as np
from aoc_lube.utils import extract_maze
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


def parse_map(input_map: list[str]) -> np.ndarray:
    grid = []
    for row in input_map[1:len(input_map) - 1]:
        elements = list(row)
        grid.append(elements[1:len(elements) - 1])
    map = np.array(grid, dtype=str)
    return map


def find_node_by_attribute(graph: networkx.Graph, search_by: str, search_value: str):
    for node, data in graph.nodes(data=True):
        if data.get(search_by) == search_value:
            return node
    return None


def translate_node_to_coords(node_value: str) -> Tuple[int, int]:
    values = node_value.strip().split(",")
    return int(values[0]), int(values[1])


def add_turns(next_node_pos, current_node_pos, current_direction: str) -> list[str]:
    current_y, current_x = translate_node_to_coords(current_node_pos)
    next_y, next_x = translate_node_to_coords(next_node_pos)

    if next_y > current_y:
        if current_direction == 'N':
            return ['E', 'S']
        if current_direction in ['E', 'W']:
            return ['S']
        return []
    if next_y < current_y:
        if current_direction == 'S':
            return ['E', 'N']
        if current_direction in ['E', 'W']:
            return ['N']
        return []
    if next_x > current_x:
        if current_direction == 'W':
            return ['N', 'E']
        if current_direction in ['N', 'S']:
            return ['E']
        return []
    if next_x < current_x:
        if current_direction == 'E':
            return ['N', 'W']
        if current_direction in ['N', 'S']:
            return ['W']
        return []
    return []


def part2_solve(input_data: str) -> int:
    return 0


def part1_solve(input_data: str) -> int:
    map = parse_map(input_data)
    wall = '#'
    start = 'S'
    end = 'E'

    moves = [
        (0, -1),  # left
        (-1, 0),  # up
        (0, 1),  # right
        (1, 0)  # down
    ]
    g = nx.Graph()
    max_y_bounds = map.shape[0] - 1
    max_x_bounds = map.shape[1] - 1
    start_node = None
    end_node = None

    for (y, x), map_value in np.ndenumerate(map):
        if map_value == wall:
            continue
        current_node = f'{y},{x}'
        if map_value == start:
            start_node = current_node
        if map_value == end:
            end_node = current_node
        if g.has_node(current_node) is False:
            g.add_node(current_node, name=map_value)
        for move in moves:
            next_y, next_x = y + move[0], x + move[1]
            if next_y < 0 or next_y > max_y_bounds:
                continue
            if next_x < 0 or next_x > max_x_bounds:
                continue
            next_pos_value = map[next_y][next_x]
            next_node = f'{next_y},{next_x}'
            if next_pos_value != wall:
                if g.has_node(next_node) is False:
                    g.add_node(next_node, name=map_value)
                g.add_edge(current_node, next_node)

    best_path = None
    best_path_score = 0
    for path in nx.shortest_simple_paths(g, start_node, end_node):
        ic(f'{len(path)} {best_path_score}')
        directions = ['E']
        current_direction = directions[-1]
        the_path = deque(path)
        previous_node = None
        current_path_score = 0
        while the_path:
            current_node = the_path.popleft()
            if current_node == end_node:
                break
            current_path_score += 1
            if previous_node is None:
                previous_node = current_node
                continue
            turns = add_turns(current_node, previous_node, current_direction)
            if len(turns) > 0:
                directions.extend(turns)
                current_direction = turns[-1]
                current_path_score += 1000 * len(turns)
            previous_node = current_node
            if best_path_score == 0:
                continue
            if current_path_score > best_path_score:
                break
        if best_path_score == 0 or current_path_score < best_path_score:
            best_path_score = current_path_score
            best_path = path
    ic(best_path)
    return best_path_score


def main() -> None:
    puzzle = Puzzle(year=2024, day=16)
    input_lines = puzzle.input_data.splitlines()
    example = puzzle.examples.pop()
    example_input = example.input_data.splitlines()

    if 7036 == ic(part1_solve(example_input)):
        puzzle.answer_a = ic(part1_solve(input_lines))

    if 45 == ic(part2_solve(example_input)):
        puzzle.answer_b = ic(part2_solve(input_lines))


if __name__ == '__main__':
    main()
