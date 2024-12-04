import numpy as np
from aocd.models import Puzzle
from icecream import ic
import re

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


def part1_solve(input_data: list[str]) -> int:
    match_pattern = "xmas"
    total = 0
    total += sum([find_pattern(line, match_pattern) for line in input_data])
    total += sum([find_pattern(line, match_pattern) for line in ["".join(column) for column in zip(*input_data)]])
    total += sum([find_pattern(line, match_pattern) for line in get_diagonals(input_data, len(match_pattern) - 1)])
    return total


def part2_solve(input_data: list[str]) -> int:
    match_pattern = "mas"
    total = 0
    row_blocks = []
    for column in range(len(input_data) - 2):
        for row in range(len(input_data[column]) - 2):
            sub_matrix = [current_row[row:row + 3] for current_row in input_data[column:column + 3]]
            diagonals = [
                "".join([sub_matrix[0][0], sub_matrix[1][1], sub_matrix[2][2]]),
                "".join([sub_matrix[2][0], sub_matrix[1][1], sub_matrix[0][2]])
            ]
            if find_pattern(diagonals[0], match_pattern) > 0 and find_pattern(diagonals[1], match_pattern) > 0:
                row_blocks.append(ic(sub_matrix))
                total += 1
    return total


def main() -> None:
    puzzle = Puzzle(year=2024, day=4)
    input_lines = puzzle.input_data.splitlines()
    example_line_part1 = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX""".splitlines()

    if 18 == ic(part1_solve(example_line_part1)):
        puzzle.answer_a = ic(part1_solve(input_lines))

    if 9 == ic(part2_solve(example_line_part1)):
        puzzle.answer_b = ic(part2_solve(input_lines))


if __name__ == '__main__':
    main()
