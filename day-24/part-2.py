from collections import defaultdict

WIDTH = 5
HEIGHT = 5

CENTER_X = WIDTH // 2
CENTER_Y = HEIGHT // 2

EMPTY_SPACE = "."
BUG = "#"


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
    return sum(
        1
        for matrix in grids_by_level.values()
        for value in matrix.values()
        if value == BUG
    )


def find_possible_affected_cells(grids_by_level):
    marked_cells = set()

    for level, matrix in grids_by_level.items():
        for (x, y), value in matrix.items():
            if value == BUG:
                marked_cells.add((level, x, y))
                marked_cells.update(neighbours(level, x, y))

    return marked_cells


def next_value(current_value, bug_neighbour_count):
    if current_value == BUG:
        return BUG if bug_neighbour_count == 1 else EMPTY_SPACE
    else:
        return BUG if bug_neighbour_count in {1, 2} else EMPTY_SPACE


def fertility_factor(grids_by_level, level, x, y):
    neighbour_values = (
        grids_by_level[ll][(xx, yy)] for (ll, xx, yy) in neighbours(level, x, y)
    )
    return sum(1 for v in neighbour_values if v == BUG)


def simulation_step(grids_by_level):
    marked_cells = find_possible_affected_cells(grids_by_level)

    updates = {}

    for level, x, y in marked_cells:
        current_value = grids_by_level[level][(x, y)]
        bug_neighbour_count = fertility_factor(grids_by_level, level, x, y)

        updates[(level, x, y)] = next_value(current_value, bug_neighbour_count)

    for (level, x, y), update_value in updates.items():
        grids_by_level[level][(x, y)] = update_value

    return grids_by_level


def part_two():
    SIMULATION_STEP_COUNT = 200

    grids_by_level = defaultdict(empty_matrix)

    level_zero = grids_by_level[0]

    with open("./input.txt") as f:
        lines = list(map(str.strip, f.readlines()))

    for x in range(0, WIDTH):
        for y in range(0, HEIGHT):
            if x != CENTER_X or y != CENTER_Y:
                level_zero[(x, y)] = lines[y][x]

    for _ in range(0, SIMULATION_STEP_COUNT):
        grids_by_level = simulation_step(grids_by_level)

    # report(grids_by_level)

    answer = bug_count(grids_by_level)

    print(answer)


if __name__ == "__main__":
    part_two()
