import itertools
from aocd import get_data


def extract_number_portion(input_line: str, text_numbers: list[str]) -> int:
    extracted_number = None
    number_positions = {}
    for current_index, current_character in enumerate(input_line):
        if current_character.isdigit():
            extracted_number = current_character
            number_positions[current_index] = int(current_character)
            break
    if extracted_number is None or 2 < current_index < len(input_line):
        if extracted_number is None:
            current_index = len(input_line)
        partial_line = input_line[:current_index]
        if partial_line.isalpha():
            for text_number in text_numbers:
                found_index = partial_line.find(text_number)
                if found_index > -1:
                    number_positions[found_index] = text_numbers.index(text_number) + 1
            number_keys = list(number_positions.keys())
            number_keys.sort()
            extracted_number = number_positions[number_keys[0]]
        else:
            for text_number in text_numbers:
                if text_number in partial_line:
                    extracted_number = text_numbers.index(text_number) + 1
                    break
    return extracted_number


def get_part2_extracted_number(input_line: str) -> int:
    valid_text_numbers = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
    first_digit = extract_number_portion(input_line, valid_text_numbers)
    reversed_text_numbers = []
    for text_number in valid_text_numbers:
        reversed_text_numbers.append(text_number[::-1])
    reversed_input_line = input_line[::-1]
    last_digit = extract_number_portion(reversed_input_line, reversed_text_numbers)
    return int(f'{first_digit}{last_digit}')


def get_part1_extracted_number(input_line: str) -> int:
    first_digit = None
    last_digit = None
    for current_character in input_line:
        if current_character.isdigit():
            first_digit = current_character
            break
    for current_character in input_line[::-1]:
        if current_character.isdigit():
            last_digit = current_character
            break
    return int(f'{first_digit}{last_digit}')


if __name__ == '__main__':
    # data = get_data(day=1, year=2023).splitlines()
    data = ['1abc2', 'pqr3stu8vwx', 'a1b2c3d4e5f', 'treb7uchet']
    data_part2 = ['two1nine', 'eightwothree', 'abcone2threexyz', 'xtwone3four', '4nineeightseven2', 'zoneight234',
                  '7pqrstsixteen']

    extracted_numbers_part1 = []
    extracted_numbers_part2 = []
    for current_line in data:
        extracted_numbers_part1.append(get_part1_extracted_number(current_line))
    print(f'Part 1 {sum(extracted_numbers_part1)}')

    for current_line in data_part2:
        extracted_numbers_part2.append(get_part2_extracted_number(current_line))
    print(f'Part 2 {sum(extracted_numbers_part2)}')
