import copy
import itertools
from collections import deque
from dataclasses import dataclass, field
from functools import reduce
from aocd.models import Puzzle
from icecream import ic


@dataclass
class Equation:
    result: int = 0
    inputs: list[int] = field(default_factory=list)


def parse_line(input_line: str) -> Equation:
    parts = input_line.split(":")
    return Equation(int(parts[0]), [int(z) for z in parts[1].strip().split(" ")])


def calculate(possible_solution: deque) -> int:
    current_result = 0
    while possible_solution:
        item = possible_solution.popleft()
        if current_result == 0:
            current_result = item
            continue
        next_item = possible_solution.popleft()
        if item == "*":
            current_result = current_result * next_item
        elif item == "+":
            current_result = current_result + next_item
        else:
            current_result = join_all_values([current_result, next_item])
    return current_result


def join_all_values(input_values: list[int]) -> int:
    return int("".join([str(z) for z in input_values]))


def solve(input_equation: Equation) -> bool:
    if input_equation.result == reduce(lambda x, y: x * y, input_equation.inputs):
        return True
    if input_equation.result == reduce(lambda x, y: x + y, input_equation.inputs):
        return True
    if input_equation.result == join_all_values(input_equation.inputs):
        return True
    current_inputs = deque(input_equation.inputs)
    solutions = [deque([current_inputs.popleft()])]
    while len(current_inputs) > 0 and len(solutions) > 0:
        value = current_inputs.popleft()
        next_possibles = []
        for possible in solutions:
            partial_result = calculate(copy.deepcopy(possible))
            if partial_result * value <= input_equation.result:
                mult_partial = deque(itertools.chain(possible, ["*"], [value]))
                next_possibles.append(mult_partial)
            if partial_result + value <= input_equation.result:
                add_partial = deque(itertools.chain(possible, ["+"], [value]))
                next_possibles.append(add_partial)
            if join_all_values([partial_result, value]) <= input_equation.result:
                join_partial = deque(itertools.chain(possible, ["||"], [value]))
                next_possibles.append(join_partial)
        solutions = next_possibles
        if len(solutions) == 0:
            return False
    for solution in solutions:
        if input_equation.result == calculate(copy.deepcopy(solution)):
            return True
    return False


def part1_solve(input_data: list[str]) -> int:
    valid_equations = []
    for current_equation in [parse_line(line) for line in input_data]:
        if solve(current_equation):
            valid_equations.append(current_equation)
    return sum([z.result for z in valid_equations])


def part2_solve(input_data: list[str]) -> int:
    valid_equations = []
    for current_equation in [parse_line(line) for line in input_data]:
        if solve(current_equation):
            valid_equations.append(current_equation)
    return sum([z.result for z in valid_equations])


def main() -> None:
    puzzle = Puzzle(year=2024, day=8)
    input_lines = puzzle.input_data.splitlines()
    example = puzzle.examples.pop()
    example_input = example.input_data.splitlines()

    if int(example.answer_a) == ic(part1_solve(example_input)):
        puzzle.answer_a = ic(part1_solve(input_lines))

    if 11387 == ic(part2_solve(example_input)):
        puzzle.answer_b = ic(part2_solve(input_lines))


if __name__ == '__main__':
    main()
