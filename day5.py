from collections import deque, defaultdict
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
        current_value = current_values.popleft()
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

# Read this thoroughly
# https://llego.dev/posts/implementing-topological-sort-python/
def topological_sort_kahn(graph):
    vertices = defaultdict(int)  # Track indegrees
    queue = []  # Initialize queue
    # Calculate indegrees
    for node in graph:
        for neighbour in graph[node]:
            vertices[neighbour] += 1
    # Add nodes with 0 indegree to queue
    for node in graph:
        if vertices[node] == 0:
            queue.append(node)
    topological_order = []
    # Process until queue is empty
    while queue:
        # Remove node from queue and add to topological order
        node = queue.pop(0)
        # check for end point nodes
        nodes = graph.get(node, [])
        if len(nodes) == 0:
            continue
        topological_order.append(node)
        # Reduce indegree for its neighbors
        for neighbour in nodes:
            vertices[neighbour] -= 1
            # Add new 0 indegree nodes to queue
            if vertices[neighbour] == 0:
                queue.append(neighbour)

    return topological_order


def part2_solve(input_data: list[str]) -> int:
    data_parts = input_data.split("\n\n")
    updates = ic(data_parts.pop().splitlines())
    rules_input = ic(data_parts.pop().splitlines())
    current_rules = ic(parse_rules(rules_input))

    invalid_updates = []
    for current_update in updates:
        update_ints = [int(x) for x in current_update.split(",")]
        if not is_ordering_valid(update_ints, current_rules):
            invalid_updates.append(update_ints)

    reorderings = []
    for invalid_update in sorted(invalid_updates, key=len, reverse=True):
        update_rules = {invalid: current_rules.get(invalid, []) for invalid in invalid_update}
        path = topological_sort_kahn(update_rules)
        to_remove = set(path).difference(set(invalid_update))
        complete = [node for node in path if node not in to_remove]
        if is_ordering_valid(complete, current_rules):
            reorderings.append(complete)
    midpoints = ic(sum([valid_update[int(len(valid_update) / 2)] for valid_update in reorderings]))
    return midpoints


def main() -> None:
    puzzle = Puzzle(year=2024, day=5)
    input_lines = puzzle.input_data
    example = puzzle.examples.pop()
    example_input = example.input_data

    if int(example.answer_a) == ic(part1_solve(example_input)):
        puzzle.answer_a = ic(part1_solve(input_lines))

    if 123 == ic(part2_solve(example_input)):
        puzzle.answer_b = ic(part2_solve(input_lines))


if __name__ == '__main__':
    main()
