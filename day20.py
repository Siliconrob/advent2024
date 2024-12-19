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


@cache
def run_matching(search_pattern: str, towel_types: frozenset[str]) -> int:
    matches = 0
    for towel in towel_types:
        if search_pattern == towel:
            matches += 1
        if search_pattern.startswith(towel):
            matches += run_matching(search_pattern[len(towel):], towel_types)
    return matches


def general_solve(input_segments: list[str], part_b: bool = False) -> int:
    towel_types = [towel.strip() for towel in input_segments[0].split(',')]
    patterns = input_segments[1].splitlines()

    searched = {}
    towels = frozenset(sorted(towel_types, key=lambda t: len(t), reverse=True))
    for pattern_index in range(len(patterns)):
        pattern = patterns[pattern_index]
        searched[pattern] = run_matching(pattern, towels)
    if part_b:
        return sum([v for k, v in searched.items()])
    return sum([1 if v > 0 else 0 for k, v in searched.items()])


def part1_solve(input_segments: list[str]) -> int:
    return general_solve(input_segments)


def part2_solve(input_segments: list[str]) -> int:
    return general_solve(input_segments, True)


def main() -> None:
    puzzle = Puzzle(year=2024, day=20)
    input_lines = puzzle.input_data.splitlines()
    example = puzzle.examples.pop()
    example_input = example.input_data.splitlines()

    if int(example.answer_a) == ic(part1_solve(example_input)):
        puzzle.answer_a = ic(part1_solve(input_lines))

    if 16 == ic(part2_solve(example_input)):
        puzzle.answer_b = ic(part2_solve(input_lines))


if __name__ == '__main__':
    main()
