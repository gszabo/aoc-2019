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

    buffer = []
    output = OutputWriter(buffer)

    c = Computer(program, InputReader([]), output)

    c.run()

    text = "".join(map(chr, buffer)).strip()
    lines = text.split("\n")

    answer = 0

    for y in range(1, len(lines) - 1):
        for x in range(1, len(lines[y]) - 1):
            if is_intersection(x, y, lines):
                answer += x * y

    print(answer)


if __name__ == "__main__":
    part_one()

