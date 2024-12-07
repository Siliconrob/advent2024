import copy
import itertools
from collections import deque
from dataclasses import dataclass, field
from functools import reduce
from itertools import cycle, pairwise
import numpy as np
from aocd.models import Puzzle
from icecream import ic


@dataclass
class Equation:
    result: int = 0
    inputs: list[int] = field(default_factory=list)


@dataclass
class Position:
    x: int = -1
    y: int = -1


@dataclass
class Guard:
    direction: str = '^'
    position: Position = field(default_factory=Position)


def is_end(current_position: Position, bounds) -> bool:
    max_x, max_y = bounds
    if current_position.x < 0 or current_position.x > max_x - 1:
        return True
    if current_position.y < 0 or current_position.y > max_y - 1:
        return True
    return False


def next_position(current_guard: Guard) -> Position:
    x, y = current_guard.position.x, current_guard.position.y
    if current_guard.direction == '^':
        return Position(x, y - 1)
    if current_guard.direction == '>':
        return Position(x + 1, y)
    if current_guard.direction == '<':
        return Position(x - 1, y)
    if current_guard.direction == 'v':
        return Position(x, y + 1)


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
        else:
            current_result = current_result + next_item
    return current_result


def solve(input_equation: Equation) -> bool:
    if input_equation.result == reduce(lambda x, y: x * y, input_equation.inputs):
        return True
    if input_equation.result == reduce(lambda x, y: x + y, input_equation.inputs):
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
    #
    #
    #
    #
    # blocker = "#"
    # guard = Guard()
    # parsed = []
    # for row_index in range(len(input_data)):
    #     row = list(input_data[row_index].replace(".", "0"))
    #     if guard.direction in row:
    #         guard.position.x = row.index(guard.direction)
    #         guard.position.y = row_index
    #     parsed.append(row)
    # matrix = ic(np.array(parsed, dtype=str))
    # current_pos = guard.position
    # turn = cycle('^>v<')
    # while not is_end(current_pos, matrix.shape):
    #     possible_pos = next_position(guard)
    #     current_square = matrix[guard.position.y][guard.position.x]
    #     current_square = int(current_square) + 1 if current_square.isnumeric() else 1
    #     matrix[guard.position.y][guard.position.x] = current_square
    #     if is_end(possible_pos, matrix.shape):
    #         break
    #     if matrix[possible_pos.y][possible_pos.x] == blocker:
    #         guard.direction = next(turn)
    #         continue
    #     guard.position.x, guard.position.y = possible_pos.x, possible_pos.y
    #     current_pos = possible_pos
    # return ic(sum([1 for iy, ix in np.ndindex(matrix.shape) if matrix[iy, ix].isnumeric() and int(matrix[iy, ix]) > 0]))


# Need to do a continuously rebuilt placement of the block
def part2_solve(input_data: list[str]) -> int:
    pass


def main() -> None:
    puzzle = Puzzle(year=2024, day=7)
    input_lines = puzzle.input_data.splitlines()
    example = puzzle.examples.pop()
    example_input = example.input_data.splitlines()

    if int(example.answer_a) == ic(part1_solve(example_input)):
        puzzle.answer_a = ic(part1_solve(input_lines))

    # if int(example.answer_b) == ic(part2_solve(example_input)):
    #     puzzle.answer_b = ic(part2_solve(input_lines))


if __name__ == '__main__':
    main()
