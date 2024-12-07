import copy
import itertools
from collections import deque
from collections.abc import Callable
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


def calculate(possible_solution: deque, calcs) -> int:
    current_result = 0
    while possible_solution:
        item = possible_solution.popleft()
        if current_result == 0:
            current_result = item
        else:
            next_item = possible_solution.popleft()
            current_result = calcs.get(item)(current_result, next_item)
    return current_result


def join_all_values(input_values: list[int]) -> int:
    return int("".join([str(z) for z in input_values]))


def solve(input_equation: Equation, terminators: list[Callable], calcs: dict) -> bool:
    if sum([1 if input_equation.result == terminator(input_equation.inputs) else 0 for terminator in terminators]) > 0:
        return True
    current_inputs = deque(input_equation.inputs)
    for solution in run_combinations(current_inputs, input_equation, calcs):
        if len(solution) == 0:
            return False
        if input_equation.result == calculate(copy.deepcopy(solution), calcs):
            return True
    return False


def run_combinations(current_inputs, input_equation, calcs):
    current_solutions = [deque([current_inputs.popleft()])]
    while len(current_inputs) > 0 and len(current_solutions) > 0:
        value = current_inputs.popleft()
        next_possibles = []
        for possible in current_solutions:
            partial_result = calculate(copy.deepcopy(possible), calcs)
            for (operator, fn) in calcs.items():
                if fn(partial_result, value) <= input_equation.result:
                    next_possibles.append(deque(itertools.chain(possible, [operator], [value])))
        current_solutions = next_possibles
        if len(current_solutions) == 0:
            break
    return current_solutions


def general_solve(input_data: list[str], terminators: list[Callable], calcs: dict) -> int:
    valid_equations = []
    for current_equation in [parse_line(line) for line in input_data]:
        if solve(current_equation, terminators, calcs):
            valid_equations.append(current_equation)
    return sum([z.result for z in valid_equations])


def part1_solve(input_data: list[str], terminators: list[Callable], calcs: dict) -> int:
    return general_solve(input_data, terminators, calcs)


def part2_solve(input_data: list[str], terminators: list[Callable], calcs: dict) -> int:
    return general_solve(input_data, terminators, calcs)


def main() -> None:
    puzzle = Puzzle(year=2024, day=7)
    input_lines = puzzle.input_data.splitlines()
    example = puzzle.examples.pop()
    example_input = example.input_data.splitlines()

    terminators = [
        lambda inputs: reduce(lambda x, y: x * y, inputs),
        lambda inputs: reduce(lambda x, y: x + y, inputs)
    ]
    calcs = {
        "*": lambda x, y: x * y,
        "+": lambda x, y: x + y
    }
    if int(example.answer_a) == ic(part1_solve(example_input, terminators, calcs)):
        puzzle.answer_a = ic(part1_solve(input_lines, terminators, calcs))

    terminators.append(lambda inputs: join_all_values(inputs))
    calcs["||"] = lambda x, y: join_all_values([x, y])

    if 11387 == ic(part2_solve(example_input, terminators, calcs)):
        puzzle.answer_b = ic(part2_solve(input_lines, terminators, calcs))


if __name__ == '__main__':
    main()
