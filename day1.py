import itertools
from aocd import get_data
from aocd import submit
from aocd.models import Puzzle
from icecream import ic
from parse import parse

def part1(input_data: []):
    list1 = []
    list2 = []

    for input_line in input_data:
        number1, spacer, number2 = parse('{:d}{:s}{:d}', input_line)
        list1.append(number1)
        list2.append(number2)
    list1.sort()
    list2.sort()

    diffs = []
    for index in range(len(list1)):
        list1_number = list1[index]
        list2_number = list2[index]
        diff = abs(list1_number - list2_number)
        diffs.append(diff)
    part1 = sum(diffs)
    ic(part1)
    return part1


def main() -> None:
    puzzle = Puzzle(year=2024, day=1)
    data = puzzle.input_data.splitlines()
    # data = [
    #     '3   4',
    #     '4   3',
    #     '2   5',
    #     '1   3',
    #     '3   9',
    #     '3   3'
    # ]
    puzzle.answer_a = part1(data)


if __name__ == '__main__':
    main()
