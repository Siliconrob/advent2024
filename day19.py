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
from shapely.geometry.polygon import Polygon, LinearRing
from sympy import symbols, Function, Eq, Piecewise, nsolve
from sympy import solve
from sympy.codegen.fnodes import Program

f = Function('f')
from sympy.abc import x, y, z, a, b, c, d, e


def find_matches(search_pattern: str, towel_types: list[str]):
    for towel in sorted(towel_types, key=lambda t: len(t), reverse=True):
        if search_pattern.startswith(towel):
            yield towel


def run_matching(search_pattern: str, towel_types: list[str]):
    current_matches = find_matches(search_pattern, towel_types)
    if current_matches is None:
        return None
    partial_matches = deque([(current_match, search_pattern[len(current_match):]) for current_match in current_matches])
    while partial_matches:
        match_to_check = partial_matches.popleft()
        k, v = match_to_check
        next_matches = find_matches(v, towel_types)
        for next_match in next_matches:
            next_key = k + next_match
            if next_key == search_pattern:
                return search_pattern
            partial_matches.append((k + next_match, v[len(next_match):]))
    return None


def part1_solve(input_segments: list[str]) -> int:
    towel_types = [towel.strip() for towel in input_segments[0].split(',')]
    searched = []

    patterns = input_segments[1].splitlines()
    for pattern_index in range(len(patterns)):
        pattern = patterns[pattern_index]
        searched.append(run_matching(pattern, towel_types))
        ic(f'{pattern_index} of {len(patterns)} complete')
    valid_patterns = len(list(filter(lambda x: x is not None, searched)))
    return valid_patterns


def part2_solve(input_data: str, grid_size: int) -> str:
    return 0


def main() -> None:
    puzzle = Puzzle(year=2024, day=19)
    input_lines = puzzle.input_data.split('\n\n')
    example = puzzle.examples.pop()
    example_input = example.input_data.split('\n\n')

    if int(example.answer_a) == ic(part1_solve(example_input)):
        puzzle.answer_a = ic(part1_solve(input_lines))
    # if 22 == ic(part1_solve(example_input, 7, 12)):
    #     puzzle.answer_a = ic(part1_solve(input_lines, 71, 1024))

    # if "6,1" == ic(part2_solve(example_input, 7)):
    #     puzzle.answer_b = ic(part2_solve(input_lines, 71))


if __name__ == '__main__':
    main()
