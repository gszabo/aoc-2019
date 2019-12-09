from computer import Computer, InputReader, OutputWriter


def part_one():
    with open("./input.txt") as f:
        program = list(map(int, f.readline().strip().split(",")))

    input = [1]
    output = []

    c = Computer(program, InputReader(input), OutputWriter(output))
    c.run()

    print(output)


if __name__ == "__main__":
    part_one()