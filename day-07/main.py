from computer import Computer, InputReader, OutputWriter, MultiOutputWriter, States
from permutations import generate_permutations, permutations_of


def run_amplifiers(phase_conf, program):
    buffer_0 = [phase_conf[0], 0]
    buffer_1 = [phase_conf[1]]
    buffer_2 = [phase_conf[2]]
    buffer_3 = [phase_conf[3]]
    buffer_4 = [phase_conf[4]]
    buffer_5 = []

    amp_a = Computer(program.copy(), InputReader(buffer_0), OutputWriter(buffer_1))
    amp_b = Computer(program.copy(), InputReader(buffer_1), OutputWriter(buffer_2))
    amp_c = Computer(program.copy(), InputReader(buffer_2), OutputWriter(buffer_3))
    amp_d = Computer(program.copy(), InputReader(buffer_3), OutputWriter(buffer_4))
    amp_e = Computer(program.copy(), InputReader(buffer_4), OutputWriter(buffer_5))

    amp_a.run()
    amp_b.run()
    amp_c.run()
    amp_d.run()
    amp_e.run()

    return (buffer_5[0], phase_conf)


def run_feedback_amplifiers(phase_conf, program):
    buffer_0 = [phase_conf[0], 0]
    buffer_1 = [phase_conf[1]]
    buffer_2 = [phase_conf[2]]
    buffer_3 = [phase_conf[3]]
    buffer_4 = [phase_conf[4]]
    thruster_buffer = []

    #####################################################
    # calling program.copy() is VERY important here     #
    # otherwise all computers modify the same memory    #
    # so the code to execute is not the expected one,   #
    # even on a new call to run_feedback_amplifiers.    #
    # (maybe Computer should do a defensive copy        #
    # itself)                                           #
    #                                                   #
    # It's a miracle that part one worked correctly     #
    # without calling copy                              #
    #####################################################
    amp_a = Computer(program.copy(), InputReader(buffer_0), OutputWriter(buffer_1))
    amp_b = Computer(program.copy(), InputReader(buffer_1), OutputWriter(buffer_2))
    amp_c = Computer(program.copy(), InputReader(buffer_2), OutputWriter(buffer_3))
    amp_d = Computer(program.copy(), InputReader(buffer_3), OutputWriter(buffer_4))
    amp_e = Computer(
        program.copy(),
        InputReader(buffer_4),
        MultiOutputWriter([buffer_0, thruster_buffer]),
    )

    amps = [amp_a, amp_b, amp_c, amp_d, amp_e]

    while not all([amp.state() == States.HALTED for amp in amps]):
        for amp in amps:
            amp.run()

    return (thruster_buffer[-1], phase_conf)


def part_one():
    with open("./input.txt") as f:
        line = f.readline().strip()
    program = list(map(int, line.split(",")))
    phase_configurations = generate_permutations(5)
    thruster_signals = map(
        lambda conf: run_amplifiers(conf, program), phase_configurations
    )
    print(max(thruster_signals, key=lambda pair: pair[0]))


def part_two():
    with open("./input.txt") as f:
        line = f.readline().strip()
    program = list(map(int, line.split(",")))
    phase_configurations = permutations_of([5, 6, 7, 8, 9])
    thruster_signals = map(
        lambda conf: run_feedback_amplifiers(conf, program), phase_configurations
    )
    print(max(thruster_signals, key=lambda pair: pair[0]))


if __name__ == "__main__":
    part_one()
    print()
    part_two()
