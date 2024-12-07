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


# Went to youtube and watch this https://www.youtube.com/watch?v=v96h9BMwrSY
# to get the sets approach right
def patrol(start_y, start_x, input_data, current_y=-1, current_x=-1):
    seen = set()
    y, x = start_y, start_x
    move_y, move_x = -1, 0

    rows = len(input_data)
    columns = len(input_data[0])

    while True:
        if not (0 <= y < rows and 0 <= x < columns):
            return len(seen) if current_y == -1 else False
        if input_data[y][x] == "#" or (y == current_y and x == current_x):
            y -= move_y
            x -= move_x
            move_y, move_x = move_x, -move_y
        elif (y, x, move_y, move_x) in seen:
            return True
        else:
            if current_y == -1:
                seen.add((y, x))
            else:
                seen.add((y, x, move_y, move_x))
            y += move_y
            x += move_x


# Need to do a continuously rebuilt placement of the block
def part2_solve(input_data: list[str]) -> int:
    start_positions = next((y, x) for y, line in enumerate(input_data) for x, char in enumerate(line) if char == "^")
    rows = len(input_data)
    columns = len(input_data[0])
    new_maps = ic(
        sum(patrol(start_positions[0], start_positions[1], input_data, y, x) for y in range(rows) for x in range(columns) if input_data[y][x] == "."))
    return new_maps


def main() -> None:
    puzzle = Puzzle(year=2024, day=6)
    input_lines = puzzle.input_data.splitlines()
    example = puzzle.examples.pop()
    example_input = example.input_data.splitlines()

    if int(example.answer_a) == ic(part1_solve(example_input)):
        puzzle.answer_a = ic(part1_solve(input_lines))

    if 6 == ic(part2_solve(example_input)):
        puzzle.answer_b = ic(part2_solve(input_lines))


if __name__ == '__main__':
    main()
