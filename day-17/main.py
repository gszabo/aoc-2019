from computer import Computer, InputReader, OutputWriter


def is_intersection(x: int, y: int, grid):
    # assumes x-1, x+1, y-1, y+1 is all in range of the grid
    return (
        grid[y][x] == "#"
        and grid[y][x - 1] == "#"
        and grid[y][x + 1] == "#"
        and grid[y - 1][x] == "#"
        and grid[y + 1][x] == "#"
    )


def part_one():
    with open("./input.txt") as f:
        program = list(map(int, f.readline().strip().split(",")))

    output_buffer = []
    output_writer = OutputWriter(output_buffer)

    c = Computer(program, InputReader([]), output_writer)

    c.run()

    text = "".join(map(chr, output_buffer)).strip()
    lines = text.split("\n")

    answer = 0

    for y in range(1, len(lines) - 1):
        for x in range(1, len(lines[y]) - 1):
            if is_intersection(x, y, lines):
                answer += x * y

    print(answer)


def part_two():
    with open("./input.txt") as f:
        program = list(map(int, f.readline().strip().split(",")))

    # wake up robot
    program[0] = 2

    input_text = (
        "A,B,A,C,B,C,B,C,A,C\n"
        "R,12,L,10,R,12\n"
        "L,8,R,10,R,6\n"
        "R,12,L,10,R,10,L,8\n"
        "n\n"
    )
    input_buffer = list(map(ord, input_text))
    input_reader = InputReader(input_buffer)

    output_buffer = []
    output_writer = OutputWriter(output_buffer)

    c = Computer(program, input_reader, output_writer)

    c.run()

    answer = output_buffer[-1]

    print(answer)


if __name__ == "__main__":
    # part_one()
    # print()
    part_two()

