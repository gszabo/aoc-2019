from __future__ import annotations

from enum import Enum


class Computer:
    def __init__(self, program, input_reader: InputReader, output_writer: OutputWriter):
        self.program = program
        self._input_reader = input_reader
        self._output_writer = output_writer
        self.instruction_pointer = 0
        self._state = States.CREATED

    def __repr__(self):
        return f"({self._state} IP={self.instruction_pointer} COMMAND={self.program[self.instruction_pointer]})"

    def run(self):
        if self._state == States.HALTED:
            return

        self._state = States.RUNNING

        while self._state != States.HALTED:
            instruction, parameters = self.decode()

            instruction_pointer_before = self.instruction_pointer

            instruction(*parameters)

            if self._state == States.WAITING_FOR_INPUT:
                break

            if instruction_pointer_before == self.instruction_pointer:
                # no jump happened, so we move the instruction pointer
                # to the next instruction (jump over this opcode and parameters)
                self.instruction_pointer += 1 + len(parameters)

    def state(self):
        return self._state

    def decode(self):
        opcodemap = {
            1: self.add,
            2: self.multiply,
            3: self.read_input,
            4: self.write_output,
            5: self.jump_if_true,
            6: self.jump_if_false,
            7: self.less_than,
            8: self.equals,
            99: self.halt,
        }
        input_argument_count_map = {
            1: 2,
            2: 2,
            3: 0,
            4: 1,
            5: 2,
            6: 2,
            7: 2,
            8: 2,
            99: 0,
        }
        opcodes_with_output = [1, 2, 3, 7, 8]

        command = self.program[self.instruction_pointer]
        opcode = command % 100

        parameters = []

        input_argument_count = input_argument_count_map[opcode]
        if input_argument_count > 0:
            modes = list(f"{command//100:0{input_argument_count}}")
            for i in range(1, input_argument_count + 1):
                mode = modes.pop()
                if mode == "0":
                    # position mode
                    position = self.program[self.instruction_pointer + i]
                    parameters.append(self.program[position])
                elif mode == "1":
                    # immediate mode
                    value = self.program[self.instruction_pointer + i]
                    parameters.append(value)
                else:
                    raise Exception("unknown mode")

        if opcode in opcodes_with_output:
            # add result address to parameters
            result_addr = self.program[
                self.instruction_pointer + input_argument_count + 1
            ]
            parameters.append(result_addr)

        return opcodemap[opcode], parameters

    def halt(self):
        self._state = States.HALTED

    def add(self, lhs, rhs, result_addr):
        self.program[result_addr] = lhs + rhs

    def multiply(self, lhs, rhs, result_addr):
        self.program[result_addr] = lhs * rhs

    def read_input(self, result_addr):
        if not self._input_reader.has_next():
            self._state = States.WAITING_FOR_INPUT
            return
        self.program[result_addr] = self._input_reader.read_next()

    def write_output(self, something):
        self._output_writer.write(something)

    def jump_if_true(self, param, jump_address):
        if param != 0:
            self.instruction_pointer = jump_address

    def jump_if_false(self, param, jump_address):
        if param == 0:
            self.instruction_pointer = jump_address

    def less_than(self, lhs, rhs, result_addr):
        if lhs < rhs:
            self.program[result_addr] = 1
        else:
            self.program[result_addr] = 0

    def equals(self, lhs, rhs, result_addr):
        if lhs == rhs:
            self.program[result_addr] = 1
        else:
            self.program[result_addr] = 0


class States(Enum):
    CREATED = 1
    HALTED = 2
    WAITING_FOR_INPUT = 3
    RUNNING = 4


class InputReader:
    def __init__(self, buffer: list):
        self._buffer = buffer

    def has_next(self):
        return len(self._buffer) > 0

    def read_next(self):
        return self._buffer.pop(0)


class OutputWriter:
    def __init__(self, buffer: list):
        self._buffer = buffer

    def write(self, item):
        self._buffer.append(item)


class MultiOutputWriter:
    def __init__(self, buffers: list):
        self._buffers = buffers

    def write(self, item):
        for buffer in self._buffers:
            buffer.append(item)
