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
from more_itertools import peekable
from more_itertools.recipes import flatten
from numpy.ma.core import empty, masked_array
from scipy import ndimage
from sympy import symbols, Function, Eq, Piecewise
from sympy import solve

f = Function('f')
from sympy.abc import x, y, z, a, b, c, d, e


@dataclass
class PlantPlot:
    plant: str = None
    area: int = 0
    perimeter: int = 0

    def price(self):
        return self.area * self.perimeter


def part2_solve(input_data: str) -> int:
    pass


def expand_point(position: Tuple[int, int]) -> list[Tuple[int, int]]:
    y, x = position
    return [
        (y, x + 1),
        (y, x - 1),
        (y - 1, x),
        (y + 1, x)
    ]


def general_solve(input_data: str, part_b: bool) -> int:
    plot_types = Counter("".join(input_data))
    matrix = np.array([list(line) for line in input_data], dtype=str)
    plant_plots = []
    for plot_kind, count in plot_types.most_common():
        masked_array = np.zeros(matrix.shape)
        points = np.argwhere(matrix == plot_kind)
        for point in points:
            masked_array[point[0], point[1]] = 1
        plots, features = ndimage.measurements.label(masked_array)
        for feature_index in range(features):
            plot_locations = np.argwhere(plots == feature_index + 1)
            wall_locations = list(flatten([expand_point(plot_location) for plot_location in plot_locations]))
            to_remove = [(plot_location[0], plot_location[1]) for plot_location in plot_locations]
            possible_walls = Counter(wall_locations)
            if part_b:
                wall_bounds = set([poss_point for poss_point, value in possible_walls.items() if poss_point not in to_remove])
                wall_counts = {}
                y_axis = sorted({pos[0] for pos in wall_bounds})
                for y in y_axis:
                    x_axis = sorted(pos[1] for pos in wall_bounds if pos[0] == y)
                    horizontal = sum((x_axis[i + 1] - x_axis[i]) > 1 for i in range(len(x_axis) - 1)) + 1
                    vertical = sum((y_axis[i + 1] - y_axis[i]) > 1 for i in range(len(y_axis) - 1)) + 1
                    z = horizontal + vertical

                    # check_points = [(y, x_axis[i]) if (x_axis[i + 1] - x_axis[i]) > 1 else None for i in range(len(x_axis) - 1)]
                    # if len(list(filter(lambda x: x is not None, check_points))) == 0:
                    #     wall_counts[y] = 1
                    # else:
                    #     for check_point in check_points:
                    #         ic(check_point)
                    # wall_counts[y] = sum((x_axis[i + 1] - x_axis[i]) > 1 for i in range(len(x_axis) - 1)) + 1
                walls = 0
            else:
                walls = sum(
                    [value if poss_point not in to_remove else 0 for poss_point, value in possible_walls.items()])
            plant_plots.append(PlantPlot(plot_kind, len(to_remove), walls))
    ic(plant_plots)
    total_walls = sum([plant_plot.price() for plant_plot in plant_plots])
    return total_walls


def part1_solve(input_data: str) -> int:
    return general_solve(input_data, False)


def part2_solve(input_data: str) -> int:
    return general_solve(input_data, True)


def main() -> None:
    puzzle = Puzzle(year=2024, day=12)
    input_lines = puzzle.input_data.splitlines()
    example = puzzle.examples.pop()
    # example_input = example.input_data

    example_input = """RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE""".split("\n")

    example_input = """AAAA
BBCD
BBCC
EEEC""".splitlines()

    # if int(example.answer_a) == ic(part1_solve(example_input)):
    #     puzzle.answer_a = ic(part1_solve(input_lines))

    if 1206 == ic(part2_solve(example_input)):
        puzzle.answer_b = ic(part2_solve(input_lines))


if __name__ == '__main__':
    main()
