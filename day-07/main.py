from computer import Computer
from permutations import generate_permutations


def run_amplifiers(phase_conf, program):
    amp_a = Computer(program, [phase_conf[0], 0])
    amp_b = Computer(program, [phase_conf[1], amp_a.run()[0]])
    amp_c = Computer(program, [phase_conf[2], amp_b.run()[0]])
    amp_d = Computer(program, [phase_conf[3], amp_c.run()[0]])
    amp_e = Computer(program, [phase_conf[4], amp_d.run()[0]])
    return (amp_e.run()[0], phase_conf)


def part_one():
    with open("./input.txt") as f:
        line = f.readline().strip()
    program = list(map(int, line.split(",")))
    phase_configurations = generate_permutations(5)
    thruster_signals = map(lambda conf: run_amplifiers(conf, program), phase_configurations)
    print(max(thruster_signals, key = lambda pair: pair[0]))


if __name__ == "__main__":
    part_one()
