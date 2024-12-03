import itertools
from collections import Counter
from typing import Tuple
from aocd.models import Puzzle
from icecream import ic
from parse import parse
import re
from more_itertools import peekable

multiply_match_pattern: str = r"mul\(\d+,\d+\)"


def part1_solve(input_data: str) -> int:
    instructions = re.findall(multiply_match_pattern, input_data)
    return instructions_total(instructions)


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
    puzzle = Puzzle(year=2024, day=3)
    example = puzzle.examples.pop()

    input_lines = puzzle.input_data
    example_line_part1 = example.input_data
    example_line_part2 = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"

    if 161 == ic(part1_solve(example_line_part1)):
        puzzle.answer_a = ic(part1_solve(input_lines))

    if 48 == ic(part2_solve(example_line_part2)):
        puzzle.answer_b = ic(part2_solve(input_lines))


if __name__ == '__main__':
    main()
