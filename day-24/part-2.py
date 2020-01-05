from collections import defaultdict

WIDTH = 5
HEIGHT = 5

CENTER_X = WIDTH // 2
CENTER_Y = HEIGHT // 2

EMPTY_SPACE = "."
BUG = "#"

# egy szimulacios lepes:
# megkeresni a bugokat es megjelolni a szomszedaikat, illetve a bug cellajat is
# a megjelolt cellakon vegigmenni es kiertekelni a szabalyokat

# cella azonositas: (level, x, y)


def neighbours(level, x, y):
    if x == CENTER_X and y == CENTER_Y:
        raise Exception("cannot get neighbours of center")

    first_list = [
        (level, x + 1, y),
        (level, x - 1, y),
        (level, x, y + 1),
        (level, x, y - 1),
    ]

    result = []

    for ll, xx, yy in first_list:
        if (
            0 <= xx < WIDTH
            and 0 <= yy < HEIGHT
            and not (xx == CENTER_X and yy == CENTER_Y)
        ):
            result.append((ll, xx, yy))
        elif xx < 0:
            result.append((ll - 1, CENTER_X - 1, CENTER_Y))
        elif xx >= WIDTH:
            result.append((ll - 1, CENTER_X + 1, CENTER_Y))
        elif yy < 0:
            result.append((ll - 1, CENTER_X, CENTER_Y - 1))
        elif yy >= HEIGHT:
            result.append((ll - 1, CENTER_X, CENTER_Y + 1))
        elif xx == CENTER_X and yy == CENTER_Y:
            if x == (CENTER_X - 1):
                result.extend([(level + 1, 0, y) for y in range(0, HEIGHT)])
            elif x == (CENTER_X + 1):
                result.extend([(level + 1, WIDTH - 1, y) for y in range(0, HEIGHT)])
            elif y == (CENTER_Y - 1):
                result.extend([(level + 1, x, 0) for x in range(0, WIDTH)])
            elif y == (CENTER_Y + 1):
                result.extend([(level + 1, x, HEIGHT - 1) for x in range(0, WIDTH)])
            else:
                raise Exception("this shouldn't happen")
        else:
            raise Exception("this shouldn't happen")

    return result


def empty_matrix():
    result = {}

    for x in range(0, WIDTH):
        for y in range(0, HEIGHT):
            if x != CENTER_X or y != CENTER_Y:
                result[(x, y)] = EMPTY_SPACE

    return result


def report(grids_by_level):
    levels = sorted(list(grids_by_level.keys()))

    for level in levels:
        print(f"Depth {level}:")
        for y in range(0, HEIGHT):
            for x in range(0, WIDTH):
                if x == CENTER_X and y == CENTER_Y:
                    print("?", end="")
                else:
                    print(grids_by_level[level][(x, y)], end="")
            print()
        print()


def bug_count(grids_by_level):
    count = 0

    for matrix in grids_by_level.values():
        for value in matrix.values():
            if value == BUG:
                count += 1

    return count


def part_two():
    grids_by_level = defaultdict(empty_matrix)

    level_zero = grids_by_level[0]

    with open("./input.txt") as f:
        lines = list(map(str.strip, f.readlines()))

    for x in range(0, WIDTH):
        for y in range(0, HEIGHT):
            if x != CENTER_X or y != CENTER_Y:
                level_zero[(x, y)] = lines[y][x]

    for _ in range(0, 200):
        marked_cells = set()

        for level, matrix in grids_by_level.items():
            for (x, y), value in matrix.items():
                if value == BUG:
                    marked_cells.add((level, x, y))
                    marked_cells.update(neighbours(level, x, y))

        updates = {}

        for level, x, y in marked_cells:
            current_value = grids_by_level[level][(x, y)]
            neighbour_values = [
                grids_by_level[ll][(xx, yy)] for (ll, xx, yy) in neighbours(level, x, y)
            ]
            bug_neighbour_count = len(
                list(filter(lambda v: v == BUG, neighbour_values))
            )

            if current_value == BUG:
                next_value = BUG if bug_neighbour_count == 1 else EMPTY_SPACE
            else:
                next_value = BUG if bug_neighbour_count in {1, 2} else EMPTY_SPACE

            updates[(level, x, y)] = next_value

        for (level, x, y), next_value in updates.items():
            grids_by_level[level][(x, y)] = next_value

    # report(grids_by_level)

    answer = bug_count(grids_by_level)

    print(answer)


if __name__ == "__main__":
    part_two()
