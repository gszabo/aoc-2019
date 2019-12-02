PUZZLE_INPUT = [
    1,
    0,
    0,
    3,
    1,
    1,
    2,
    3,
    1,
    3,
    4,
    3,
    1,
    5,
    0,
    3,
    2,
    9,
    1,
    19,
    1,
    19,
    5,
    23,
    1,
    9,
    23,
    27,
    2,
    27,
    6,
    31,
    1,
    5,
    31,
    35,
    2,
    9,
    35,
    39,
    2,
    6,
    39,
    43,
    2,
    43,
    13,
    47,
    2,
    13,
    47,
    51,
    1,
    10,
    51,
    55,
    1,
    9,
    55,
    59,
    1,
    6,
    59,
    63,
    2,
    63,
    9,
    67,
    1,
    67,
    6,
    71,
    1,
    71,
    13,
    75,
    1,
    6,
    75,
    79,
    1,
    9,
    79,
    83,
    2,
    9,
    83,
    87,
    1,
    87,
    6,
    91,
    1,
    91,
    13,
    95,
    2,
    6,
    95,
    99,
    1,
    10,
    99,
    103,
    2,
    103,
    9,
    107,
    1,
    6,
    107,
    111,
    1,
    10,
    111,
    115,
    2,
    6,
    115,
    119,
    1,
    5,
    119,
    123,
    1,
    123,
    13,
    127,
    1,
    127,
    5,
    131,
    1,
    6,
    131,
    135,
    2,
    135,
    13,
    139,
    1,
    139,
    2,
    143,
    1,
    143,
    10,
    0,
    99,
    2,
    0,
    14,
    0,
]

PART_TWO_TARGET = 19690720


def part_one():
    program = create_modified_program(12, 2)
    result = run_program(program)
    print(f"Answer: {result[0]}")


def part_two():
    for noun in range(0, 100):
        for verb in range(0, 100):
            print(f"Trying noun={noun} verb={verb}")
            input_program = create_modified_program(noun, verb)
            program_result = run_program(input_program)
            if program_result[0] == PART_TWO_TARGET:
                print("DONE")
                print(f"Answer: {100*noun + verb}")
                return (noun, verb)


def run_program(program):
    # make a clone to not modify input object
    program = program[:]
    pc = 0
    while True:
        command = program[pc]
        if command == 1:
            pos1, pos2, end_pos = program[pc + 1 : pc + 4]
            program[end_pos] = program[pos1] + program[pos2]
            pc += 4
        elif command == 2:
            pos1, pos2, end_pos = program[pc + 1 : pc + 4]
            program[end_pos] = program[pos1] * program[pos2]
            pc += 4
        elif command == 99:
            return program
        else:
            raise Exception(f"unknown opcode: {command} at position {pc}")


def create_modified_program(noun, verb):
    result = PUZZLE_INPUT[:]
    result[1] = noun
    result[2] = verb
    return result


if __name__ == "__main__":
    print("Part 1")
    part_one()
    print("\n\nPart 2")
    part_two()

