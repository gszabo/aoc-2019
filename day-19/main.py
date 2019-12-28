from computer import Computer, InputReader, OutputWriter


def part_one():
    with open("./input.txt") as f:
        program = list(map(int, f.readline().strip().split(",")))

    answer = 0

    for y in range(0, 50):
        for x in range(0, 50):
            input_buffer = [x, y]
            output_buffer = []

            c = Computer(program, InputReader(input_buffer), OutputWriter(output_buffer))
            c.run()

            if output_buffer[0] == 1:
                answer += 1

    print(answer)


if __name__ == "__main__":
    part_one()
