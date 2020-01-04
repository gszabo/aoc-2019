WIDTH = 5
HEIGHT = 5

EMPTY_SPACE = "."
BUG = "#"

BIODIVERSITY_COEFFICIENT = [
    [1, 2, 4, 8, 16],
    [32, 64, 128, 256, 512],
    [1 << 10, 1 << 11, 1 << 12, 1 << 13, 1 << 14],
    [1 << 15, 1 << 16, 1 << 17, 1 << 18, 1 << 19],
    [1 << 20, 1 << 21, 1 << 22, 1 << 23, 1 << 24],
]


def create_empty_matrix():
    # adds "borders" to simplify calculations
    result = {}

    for y in range(-1, HEIGHT + 1):
        for x in range(-1, WIDTH + 1):
            result[(x, y)] = EMPTY_SPACE

    return result


def adjacent_bugs(x, y, matrix):
    neighbours = [
        matrix[(x - 1, y)],
        matrix[(x + 1, y)],
        matrix[(x, y - 1)],
        matrix[(x, y + 1)],
    ]
    return len(list(filter(lambda c: c == BUG, neighbours)))


def simulation_step(matrix):
    result = create_empty_matrix()

    for x in range(0, WIDTH):
        for y in range(0, HEIGHT):
            cell = matrix[(x, y)]
            bugs = adjacent_bugs(x, y, matrix)

            if cell == BUG:
                new_cell = BUG if bugs == 1 else EMPTY_SPACE
            else:
                new_cell = BUG if bugs in {1, 2} else EMPTY_SPACE

            result[(x, y)] = new_cell

    return result


def stringify(matrix):
    chars = []
    for y in range(0, HEIGHT):
        for x in range(0, WIDTH):
            chars.append(matrix[(x, y)])
        chars.append("\n")
    return "".join(chars)


def biodiversity_rating(matrix):
    result = 0

    for x in range(0, WIDTH):
        for y in range(0, HEIGHT):
            cell = matrix[(x, y)]
            coefficient = BIODIVERSITY_COEFFICIENT[y][x]
            if cell == BUG:
                result += coefficient

    return result


def part_one():
    m = create_empty_matrix()

    with open("./input.txt") as f:
        lines = list(map(str.strip, f.readlines()))
    for x in range(0, WIDTH):
        for y in range(0, HEIGHT):
            m[(x, y)] = lines[y][x]

    collector = set()
    collector.add(stringify(m))

    i = 0
    while True:
        m = simulation_step(m)
        i += 1

        s = stringify(m)
        if s in collector:
            print(f"Found first match after {i} steps")
            print(s)
            answer = biodiversity_rating(m)
            break
        else:
            collector.add(s)

    print(answer)


if __name__ == "__main__":
    part_one()
