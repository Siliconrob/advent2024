import copy
import enum
import itertools
import sys
from _pyrepl.completing_reader import complete
from collections import deque, Counter
from collections.abc import Callable
from copy import deepcopy
from dataclasses import dataclass, field
import time
from functools import reduce, cache
from heapq import heappop, heappush
from typing import Tuple, List

import networkx
import networkx as nx
import numpy as np
from aocd.models import Puzzle
from icecream import ic
from more_itertools import peekable, strip
from more_itertools.recipes import flatten, pairwise
from numpy.f2py.auxfuncs import throw_error
from numpy.ma.core import empty, masked_array
from parse import parse
from scipy import ndimage
from shapely.geometry.polygon import Polygon, LinearRing
from sympy import symbols, Function, Eq, Piecewise, nsolve
from sympy import solve
from sympy.codegen.fnodes import Program

f = Function('f')
from sympy.abc import x, y, z, a, b, c, d, e


@enum.unique
class Opcode(enum.Enum):
    adv = 0
    bxl = 1
    bst = 2
    jnz = 3
    bxc = 4
    out = 5
    bdv = 6
    cdv = 7


def part2_solve(input_data: str) -> int:
    return 0


def read_registers(registers_inputs: list[str]) -> dict[int]:
    registers = {}
    for input in registers_inputs.splitlines():
        id, value = parse("Register {:w}: {:d}", input)
        registers[id] = value
    return registers


def parse_program(input_data: str) -> Program:
    inputs = input_data.split('\n\n')
    registers = read_registers(inputs[0])
    input_list = [int(x) for x in inputs[1].split(":")[1].split(",")]
    return input_list, registers


@dataclass
class Computer:
    registers: dict = field(default_factory=dict)
    instruction_ptr: int = 0
    output: list[str] = field(default_factory=list)

    def formatted_output(self) -> str:
        return ",".join(self.output)

    def retrieve_operand(self, operand: int) -> int:
        if operand < 4:
            return operand
        if operand == 4:
            return self.registers.get('A')
        if operand == 5:
            return self.registers.get('B')
        if operand == 6:
            return self.registers.get('C')
        if operand == 7:
            return None

    def run_instruction(self, opcode: Opcode, operand: int) -> None:
        combo_operand = self.retrieve_operand(operand)

        numerator = self.registers.get('A')
        denominator = pow(2, combo_operand) if combo_operand is not None else 1

        if opcode == Opcode.adv:
            self.registers['A'] = numerator // denominator
        if opcode == Opcode.bxl:
            self.registers['B'] = self.registers.get('B') ^ operand
        if opcode == Opcode.bst:
            self.registers['B'] = combo_operand % 8
        if opcode == Opcode.jnz:
            if self.registers.get('A') != 0:
                self.instruction_ptr = operand
                return
        if opcode == Opcode.bxc:
            self.registers['B'] = self.registers.get('B') ^ self.registers.get('C')
        if opcode == Opcode.out:
            self.output.extend(list(str(combo_operand % 8)))
        if opcode == Opcode.bdv:
            self.registers['B'] = numerator // denominator
        if opcode == Opcode.cdv:
            self.registers['C'] = numerator // denominator
        self.instruction_ptr += 2


def instruction_test1(input_registers: dict) -> None:
    # If register C contains 9, the program 2,6 would set register B to 1
    input_registers['C'] = 9
    instructions = [2, 6]
    simulator = Computer(input_registers)
    while simulator.instruction_ptr < len(instructions):
        opcode = Opcode(instructions[simulator.instruction_ptr])
        operand = instructions[simulator.instruction_ptr + 1]
        simulator.run_instruction(opcode, operand)
    assert (input_registers.get('B') == 1)


def instruction_test2(input_registers: dict) -> None:
    # If register A contains 10, the program 5,0,5,1,5,4 would output 0,1,2
    input_registers['A'] = 10
    instructions = [5, 0, 5, 1, 5, 4]
    simulator = Computer(input_registers)
    while simulator.instruction_ptr < len(instructions):
        opcode = Opcode(instructions[simulator.instruction_ptr])
        operand = instructions[simulator.instruction_ptr + 1]
        simulator.run_instruction(opcode, operand)
    results = simulator.formatted_output()
    assert (results == "0,1,2")


def instruction_test3(input_registers: dict) -> None:
    # If register A contains 2024, the program 0,1,5,4,3,0 would output 4,2,5,6,7,7,7,7,3,1,0 and leave 0 in register A.
    input_registers['A'] = 2024
    instructions = [0, 1, 5, 4, 3, 0]
    simulator = Computer(input_registers)

    while simulator.instruction_ptr < len(instructions):
        opcode = Opcode(instructions[simulator.instruction_ptr])
        operand = instructions[simulator.instruction_ptr + 1]
        simulator.run_instruction(opcode, operand)

    results = simulator.formatted_output()
    assert (results == "4,2,5,6,7,7,7,7,3,1,0")
    assert (input_registers.get('A') == 0)


def instruction_test4(input_registers: dict) -> None:
    # If register B contains 29, the program 1,7 would set register B to 26
    input_registers['B'] = 29
    instructions = [1, 7]
    simulator = Computer(input_registers)

    while simulator.instruction_ptr < len(instructions):
        opcode = Opcode(instructions[simulator.instruction_ptr])
        operand = instructions[simulator.instruction_ptr + 1]
        simulator.run_instruction(opcode, operand)
    assert (input_registers.get('B') == 26)


def instruction_test5(input_registers: dict) -> None:
    # If register B contains 2024 and register C contains 43690, the program 4,0 would set register B to 44354
    input_registers['B'] = 2024
    input_registers['C'] = 43690
    instructions = [4, 0]
    simulator = Computer(input_registers)

    while simulator.instruction_ptr < len(instructions):
        opcode = Opcode(instructions[simulator.instruction_ptr])
        operand = instructions[simulator.instruction_ptr + 1]
        simulator.run_instruction(opcode, operand)
    assert (input_registers.get('B') == 44354)


def part1_solve(input_data: str) -> int:
    instructions, registers = parse_program(input_data)
    simulator = Computer(registers)
    while simulator.instruction_ptr < len(instructions):
        opcode = Opcode(instructions[simulator.instruction_ptr])
        operand = instructions[simulator.instruction_ptr + 1]
        simulator.run_instruction(opcode, operand)
    return ic(simulator.formatted_output())


def main() -> None:
    puzzle = Puzzle(year=2024, day=17)
    input_lines = puzzle.input_data
    example = puzzle.examples.pop()
    example_input = example.input_data

    test_registers = {'A': 0, 'B': 0, 'C': 0}
    instruction_test1(deepcopy(test_registers))
    instruction_test2(deepcopy(test_registers))
    instruction_test3(deepcopy(test_registers))
    instruction_test4(deepcopy(test_registers))
    instruction_test5(deepcopy(test_registers))

    if "4,6,3,5,6,3,5,2,1,0" == ic(part1_solve(example_input)):
        puzzle.answer_a = ic(part1_solve(input_lines))

    if 117440 == ic(part2_solve(example_input)):
        puzzle.answer_b = ic(part2_solve(input_lines))


if __name__ == '__main__':
    main()
