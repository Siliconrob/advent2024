from collections import Counter
from typing import Tuple
from aocd.models import Puzzle
from icecream import ic
from parse import parse


def read_lists(lines_to_parse: list[str]) -> Tuple[list[int], list[int]]:
    list1 = []
    list2 = []

    for input_line in lines_to_parse:
        number1, spacer, number2 = parse('{:d}{:s}{:d}', input_line)
        list1.append(number1)
        list2.append(number2)
    list1.sort()
    list2.sort()
    return list1, list2


def part1_solve(list1: list[int], list2: list[int]) -> int:
    diffs = []
    for index in range(len(list1)):
        list1_number = list1[index]
        list2_number = list2[index]
        diff = abs(list1_number - list2_number)
        diffs.append(diff)
    return sum(diffs)


def part2_solve(list1: list[int], list2: list[int]) -> int:
    scores = []
    list2_counts = Counter(list2)
    for index in range(len(list1)):
        list1_number = list1[index]
        matches = list2_counts.get(list1[index])
        scores.append(0 if matches is None else matches * list1_number)
    return sum(scores)


def main() -> None:
    puzzle = Puzzle(year=2024, day=2)
    data = puzzle.input_data.splitlines()
    # data = [
    #     '3   4',
    #     '4   3',
    #     '2   5',
    #     '1   3',
    #     '3   9',
    #     '3   3'
    # ]
    list1, list2 = read_lists(data)
    puzzle.answer_a = ic(part1_solve(list1, list2))
    puzzle.answer_b = ic(part2_solve(list1, list2))


if __name__ == '__main__':
    main()
