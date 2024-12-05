from collections import deque

import numpy as np
from aocd.models import Puzzle
from icecream import ic
import re
from parse import parse


def get_diagonals(input_data: list[str], min_length: 0) -> list[str]:
    row_data = ic([list(line) for line in input_data])
    matrix = ic(np.array(row_data, dtype=str))
    columns = len(input_data[0])
    diagonals = []
    for index in range(columns * -1, columns):
        diagonal_left_right = "".join(np.diagonal(matrix, offset=index).tolist())
        if len(diagonal_left_right) > min_length:
            diagonals.append(diagonal_left_right)
        diagonal_right_left = "".join(np.diagonal(np.fliplr(matrix), offset=-index).tolist())
        if len(diagonal_right_left) > min_length:
            diagonals.append(diagonal_right_left)
    return diagonals


def find_pattern(input_line: str, search: str) -> int:
    result = sum([
        len(re.findall(search, input_line, flags=re.IGNORECASE)),
        len(re.findall(search, input_line[::-1], flags=re.IGNORECASE))
    ])
    return result


def parse_rules(rules_input: list[str]) -> dict:
    rules = {}
    for rule in rules_input:
        key, value = parse("{:d}|{:d}", rule)
        current_rule = rules.get(key)
        if current_rule is not None:
            current_rule.append(value)
        else:
            current_rule = [value]
        rules[key] = current_rule
    return rules


def is_ordering_valid(current_update: list[int], current_rules: dict) -> bool:
    current_values = deque(current_update)
    is_valid = len(current_values) > 0
    while len(current_values) > 1:
        current_value = ic(current_values.popleft())
        matching_rule = current_rules.get(current_value)
        if matching_rule is None:
            is_valid = False
            break
        if len(current_values) != len(set(matching_rule) & set(current_values)):
            is_valid = False
            break
    return is_valid


def part1_solve(input_data: list[str]) -> int:
    data_parts = input_data.split("\n\n")
    updates = ic(data_parts.pop().splitlines())
    rules_input = ic(data_parts.pop().splitlines())
    current_rules = ic(parse_rules(rules_input))

    valid_updates = []
    for current_update in updates:
        update_ints = [int(x) for x in current_update.split(",")]
        if is_ordering_valid(update_ints, current_rules):
            valid_updates.append(update_ints)
    midpoints = ic(sum([valid_update[int(len(valid_update) / 2)] for valid_update in valid_updates]))
    return midpoints

def part2_solve(input_data: list[str]) -> int:
    match_pattern = "mas"
    total = 0
    # row_blocks = []
    for column in range(len(input_data) - 2):
        for row in range(len(input_data[column]) - 2):
            row_data = [list(current_row[row:row + 3]) for current_row in input_data[column:column + 3]]
            sub_matrix = np.array(row_data, dtype=str)
            diagonals = [
                "".join(np.diagonal(sub_matrix).tolist()),
                "".join(np.diagonal(np.fliplr(sub_matrix)).tolist())
            ]
            if sum([find_pattern(diagonal, match_pattern) for diagonal in diagonals]) >= 2:
                # row_blocks.append(ic(sub_matrix))
                total += 1
    return total


def main() -> None:
    puzzle = Puzzle(year=2024, day=5)
    input_lines = puzzle.input_data
    example = puzzle.examples.pop()
    example_input = example.input_data

    if int(example.answer_a) == ic(part1_solve(example_input)):
        puzzle.answer_a = ic(part1_solve(input_lines))

    # if example.answer_b == ic(part2_solve(example_line_part1)):
    #     puzzle.answer_b = ic(part2_solve(input_lines))


if __name__ == '__main__':
    main()
