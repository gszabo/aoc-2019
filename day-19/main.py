from computer import Computer, InputReader, OutputWriter


def cell_is_inside_beam(program, x, y):
    input_buffer = [x, y]
    output_buffer = []

    c = Computer(program, InputReader(input_buffer), OutputWriter(output_buffer))
    c.run()

    return output_buffer[0] == 1


def first_in_row(program, y):
    x = 0
    while True:
        if cell_is_inside_beam(program, x, y):
            return x
        x += 1


def first_in_column(program, x):
    y = 0
    while True:
        if cell_is_inside_beam(program, x, y):
            return y
        y += 1


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


def part_two():
    with open("./input.txt") as f:
        program = list(map(int, f.readline().strip().split(",")))

    y0 = int(input("y = "))
    x0 = first_in_row(program, y0)
    print(f"Lower left corner: {(x0, y0)}")

    x1 = x0 + 99
    y1 = first_in_column(program, x1)
    print(f"Upper right corner: {(x1, y1)}")

    width = x1 - x0 + 1
    height = y0 - y1 + 1
    print(f"(w, h) = {(width, height)}")

    # winning input was: y = 1264
    # Lower left corner: (619, 1264)
    # Upper right corner: (718, 1165)
    # (w, h) = (100, 100)
    #
    # From here the upper left corner is in (619, 1165)
    # and the answer is 6191165


if __name__ == "__main__":
    # part_one()
    part_two()
