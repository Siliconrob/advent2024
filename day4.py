import itertools
from collections import Counter
from typing import Tuple
from aocd.models import Puzzle
from icecream import ic
from parse import parse
import re
from more_itertools import peekable


def left_to_right_diagonals(input_data: list[str]) -> list[str]:
    lines = []
    size = len(input_data)
    for col in range(size):
        diagonal = []
        x, y = 0, col
        while x < size and y < size:
            diagonal.append(input_data[x][y])
            x += 1
            y += 1
        lines.append("".join(diagonal))
    for row in range(1, size):
        diagonal = []
        x, y = row, 0
        while x < size and y < size:
            diagonal.append(input_data[x][y])
            x += 1
            y += 1
        lines.append("".join(diagonal))
    return lines


def right_to_left_diagonals(input_data: list[str]) -> list[str]:
    lines = []
    size = len(input_data)
    for col in range(size):
        diagonal = []
        x, y = 0, col
        while x < size and y >= 0:
            diagonal.append(input_data[x][y])
            x += 1
            y -= 1
        lines.append("".join(diagonal))
    for row in range(1, size):
        diagonal = []
        x, y = row, size - 1
        while x < size and y >= 0:
            diagonal.append(input_data[x][y])
            x += 1
            y -= 1
        lines.append("".join(diagonal))
    return lines


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
    total += sum([find_pattern(line, match_pattern) for line in left_to_right_diagonals(input_data)])
    total += sum([find_pattern(line, match_pattern) for line in right_to_left_diagonals(input_data)])
    return total

    #     horizontal_matches.append(len(re.findall(match_pattern, line, flags=re.IGNORECASE)))
    #     horizontal_matches.append(len(re.findall(match_pattern, line[::-1], flags=re.IGNORECASE)))
    # total += sum(horizontal_matches)

    # for line in ["".join(column) for column in zip(*input_data)]:
    #     vertical_matches.append(len(re.findall(match_pattern, line, flags=re.IGNORECASE)))
    #     vertical_matches.append(len(re.findall(match_pattern, line[::-1], flags=re.IGNORECASE)))
    # total += sum(vertical_matches)
    #
    # for line in left_to_right_diagonals(input_data):
    #     left_to_right.append(len(re.findall(match_pattern, line, flags=re.IGNORECASE)))
    #     left_to_right.append(len(re.findall(match_pattern, line[::-1], flags=re.IGNORECASE)))
    # total += sum(left_to_right)
    #
    # for line in right_to_left_diagonals(input_data):
    #     right_to_left.append(len(re.findall(match_pattern, line, flags=re.IGNORECASE)))
    #     right_to_left.append(len(re.findall(match_pattern, line[::-1], flags=re.IGNORECASE)))
    # total += sum(right_to_left)
    #
    # return total
    # instructions = re.findall(multiply_match_pattern, input_data)
    # return instructions_total(instructions)


def instructions_total(instructions: list[str]) -> int:
    instructions_sum = []
    for instruction in instructions:
        number1, number2 = parse("mul({:d},{:d})", instruction)
        instructions_sum.append(number1 * number2)
    return sum(instructions_sum)


def part2_solve(input_data: str) -> int:
    line_sum = []
    for segment in input_data.split(r"do()"):
        end_markers = peekable(re.finditer(r"don't\(\)", segment))
        if end_markers:
            extract_segment = ic(segment[:next(end_markers).start()])
        else:
            extract_segment = ic(segment[:len(segment)])
        instructions = re.findall(multiply_match_pattern, extract_segment)
        line_sum.append(instructions_total(instructions))
    return ic(sum(line_sum))


def main() -> None:
    puzzle = Puzzle(year=2024, day=4)
    example = puzzle.examples.pop()

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

    # if 48 == ic(part2_solve(example_line_part2)):
    #     puzzle.answer_b = ic(part2_solve(input_lines))


if __name__ == '__main__':
    main()
