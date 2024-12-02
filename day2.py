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


def report_error_counts(diffs: list[int]) -> list[int]:
    errors = []
    for index in range(len(diffs)):
        current_diff = diffs[index]
        if current_diff <= 0:
            errors.append(index)
            continue
        if current_diff > 3:
            errors.append(index)
            continue
        continue
    return errors


def part1_solve(input_lines: list[str]) -> int:
    safe_reports = 0
    for line in input_lines:
        report_values = parse_line(line)
        current_errors = report_details(report_values)
        safe_reports += 1 if len(current_errors) == 0 else 0
    return safe_reports


def part2_solve(input_lines: list[str]) -> int:
    safe_reports = 0
    for line in input_lines:
        report_values = parse_line(line)
        current_errors = report_details(report_values)
        if len(current_errors) == 0:
            safe_reports += 1
            continue

        pair_issue_index = current_errors.pop()
        report_values.pop(pair_issue_index)
        current_errors = report_details(report_values)
        if len(current_errors) == 0:
            safe_reports += 1
            continue

        report_values = parse_line(line)
        report_values.pop(pair_issue_index + 1)
        current_errors = report_details(report_values)
        safe_reports += 1 if len(current_errors) == 0 else 0

    return safe_reports


def report_details(report_values: list[int]) -> dict:
    is_decreasing = report_values[0] > report_values[-1]
    pair_diffs = ic(get_pair_diffs(itertools.pairwise(report_values), is_decreasing))
    return report_error_counts(pair_diffs)


def main() -> None:
    puzzle = Puzzle(year=2024, day=2)
    example = puzzle.examples.pop()

    input_lines = puzzle.input_data.splitlines()
    example_lines = example.input_data.splitlines()

    if int(example.answer_a) == ic(part1_solve(example_lines)):
        puzzle.answer_a = ic(part1_solve(input_lines))

    if int(example.answer_b) == ic(part2_solve(example_lines)):
        puzzle.answer_b = ic(part2_solve(input_lines))


if __name__ == '__main__':
    main()
