import itertools
from collections import Counter
from typing import Tuple
from aocd.models import Puzzle
from icecream import ic
from parse import parse


def parse_line(input_line: str) -> list[int]:
    return [int(x) for x in input_line.split(" ")]


def get_pair_diffs(computed_pairs, is_decreasing) -> list[int]:
    diffs = []
    for pair in computed_pairs:
        diffs.append(pair[0] - pair[1] if is_decreasing else pair[1] - pair[0])
    return diffs


def is_report_safe(diffs: list[int], is_decreasing: bool) -> bool:
    for current_diff in diffs:
        if current_diff <= 0:
            return False
        if current_diff > 3:
            return False
        continue
    return True


def part1_solve(input_lines: list[str]) -> int:
    safe_reports = 0
    for line in input_lines:
        report_values = parse_line(line)
        is_decreasing = report_values[0] > report_values[-1]
        pair_diffs = ic(get_pair_diffs(itertools.pairwise(report_values), is_decreasing))
        safe_reports += 1 if is_report_safe(pair_diffs, is_decreasing) else 0
    return safe_reports


def part2_solve(list1: list[int], list2: list[int]) -> int:
    scores = []
    list2_counts = Counter(list2)
    for list1_number in list1:
        matches = list2_counts.get(list1_number)
        scores.append(0 if matches is None else matches * list1_number)
    return sum(scores)


def main() -> None:
    puzzle = Puzzle(year=2024, day=2)
    example = puzzle.examples.pop()

    if int(example.answer_a) == ic(part1_solve(example.input_data.splitlines())):
        puzzle.answer_a = ic(part1_solve(puzzle.input_data.splitlines()))

    # Example answer b is not parsing right from  says 9 when it is supposed to be 31
    # if int(example.answer_b) == ic(part2_solve(example_list1, example_list2)):
    # if 31 == ic(part2_solve(example_list1, example_list2)):
    #     puzzle.answer_b = ic(part2_solve(list1, list2))


if __name__ == '__main__':
    main()
