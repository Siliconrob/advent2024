from dataclasses import dataclass, field
from itertools import cycle
import numpy as np
from aocd.models import Puzzle
from icecream import ic


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


def part1_solve(input_data: list[str]) -> int:
    blocker = "#"
    guard = Guard()
    parsed = []
    for row_index in range(len(input_data)):
        row = list(input_data[row_index].replace(".", "0"))
        if guard.direction in row:
            guard.position.x = row.index(guard.direction)
            guard.position.y = row_index
        parsed.append(row)
    matrix = ic(np.array(parsed, dtype=str))
    current_pos = guard.position
    turn = cycle('^>v<')
    while not is_end(current_pos, matrix.shape):
        possible_pos = next_position(guard)
        current_square = matrix[guard.position.y][guard.position.x]
        current_square = int(current_square) + 1 if current_square.isnumeric() else 1
        matrix[guard.position.y][guard.position.x] = current_square
        if is_end(possible_pos, matrix.shape):
            break
        if matrix[possible_pos.y][possible_pos.x] == blocker:
            guard.direction = next(turn)
            continue
        guard.position.x, guard.position.y = possible_pos.x, possible_pos.y
        current_pos = possible_pos
    return ic(sum([1 for iy, ix in np.ndindex(matrix.shape) if matrix[iy, ix].isnumeric() and int(matrix[iy, ix]) > 0]))


def part2_solve(input_data: list[str]) -> int:
    blocker = "#"
    guard = Guard()
    parsed = []
    for row_index in range(len(input_data)):
        row = list(input_data[row_index].replace(".", "0"))
        if guard.direction in row:
            guard.position.x = row.index(guard.direction)
            guard.position.y = row_index
        parsed.append(row)
    matrix = ic(np.array(parsed, dtype=str))
    current_pos = guard.position
    turn = cycle('^>v<')
    while not is_end(current_pos, matrix.shape):
        possible_pos = next_position(guard)
        current_square = matrix[guard.position.y][guard.position.x]
        current_square = int(current_square) + 1 if current_square.isnumeric() else 1
        matrix[guard.position.y][guard.position.x] = current_square
        if is_end(possible_pos, matrix.shape):
            break
        if matrix[possible_pos.y][possible_pos.x] == blocker:
            guard.direction = next(turn)
            continue
        guard.position.x, guard.position.y = possible_pos.x, possible_pos.y
        current_pos = possible_pos
    return ic(sum([1 for iy, ix in np.ndindex(matrix.shape) if matrix[iy, ix].isnumeric() and int(matrix[iy, ix]) > 0]))


def main() -> None:
    puzzle = Puzzle(year=2024, day=6)
    input_lines = puzzle.input_data.splitlines()
    example = puzzle.examples.pop()
    example_input = example.input_data.splitlines()

    # if int(example.answer_a) == ic(part1_solve(example_input)):
    #     puzzle.answer_a = ic(part1_solve(input_lines))

    if 6 == ic(part2_solve(example_input)):
        puzzle.answer_b = ic(part2_solve(input_lines))


if __name__ == '__main__':
    main()
