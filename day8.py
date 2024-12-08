import copy
import itertools
from collections import deque
from collections.abc import Callable
from dataclasses import dataclass, field
from functools import reduce
from aocd.models import Puzzle
from icecream import ic
from sympy import symbols, Function, Eq, Piecewise
from sympy import solve

f = Function('f')
from sympy.abc import x, y, z, a, b, c, d, e


@dataclass
class Equation:
    result: int = 0
    inputs: list[int] = field(default_factory=list)


def part1_solve(input_data: list[str]) -> int:
    max_x, max_y = len(input_data), len(input_data[0])
    antenna_groups = find_antennas(input_data)
    anti_nodes = []
    for (antenna_type, antenna_group) in antenna_groups.items():
        # f = ic(list())
        # k = ic(list(itertools.pairwise(antenna_group)))
        for antenna_pair in itertools.combinations(antenna_group, 2):
            location1, location2 = antenna_pair[0], antenna_pair[1]
            y_diff = location1[0] - location2[0]
            x_diff = location1[1] - location2[1]
            # left right rising diagonal
            # if location1[1][0] > location2[1][0] and location1[1][1] < location2[1][1]:
            poss_points = set([
                (location1[0] - y_diff, location1[1] - x_diff),
                (location1[0] + y_diff, location1[1] + x_diff),
                (location2[0] - y_diff, location2[1] - x_diff),
                (location2[0] + y_diff, location2[1] + x_diff)
            ])
            current_points = [location1, location2]
            poss_points = poss_points - set(current_points)
            for point in poss_points:
                point_y, point_x = point[0], point[1]
                if -1 < point_y < max_y and -1 < point_x < max_x:
                    anti_nodes.append(point)
    # antennas = ic([item for sublist in antenna_groups.values() for item in sublist])
    return len(set(anti_nodes))


def print_map(input_data, uniques):
    lines = []

    for y in range(len(input_data)):
        line = []
        for x in range(len(input_data[y])):
            point_value = input_data[y][x]
            if (y, x) in uniques:
                point_value = "#"
            line.append(point_value)
        lines.append("".join(line))
    ic(lines)


def find_antennas(input_data):
    current_node_sets = {}
    for y in range(len(input_data)):
        for x in range(len(input_data[y])):
            point_value = input_data[y][x]
            if point_value == '.':
                continue
            current_points = current_node_sets.get(point_value)
            if current_points is None:
                current_node_sets[point_value] = [(y, x)]
                continue
            current_points.append((y, x))
            current_node_sets[point_value] = current_points
    return current_node_sets


def part2_solve(input_data: list[str], terminators: list[Callable], calcs: dict) -> int:
    # return general_solve(input_data, terminators, calcs)
    pass


def main() -> None:
    puzzle = Puzzle(year=2024, day=8)
    input_lines = puzzle.input_data.splitlines()
    example = puzzle.examples.pop()
    example_input = example.input_data.splitlines()

    # if int(example.answer_a) == ic(part1_solve(example_input)):
    #     puzzle.answer_a = ic(part1_solve(input_lines))

    if 11387 == ic(part2_solve(example_input, terminators, calcs)):
        puzzle.answer_b = ic(part2_solve(input_lines, terminators, calcs))


if __name__ == '__main__':
    main()
