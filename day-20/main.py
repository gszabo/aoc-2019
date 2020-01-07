from pprint import pprint
from collections import defaultdict, deque


def read_input(path):
    with open(path) as f:
        # provide padding to avoid index out of range
        # only strip \n from right, leave other space chars
        lines = [line.rstrip("\n") for line in f.readlines()]
    return lines


def add_padding(lines):
    """
    Provides 1 cell padding on top, left, right, bottom edges
    to avoid index out of range errors in the algorithm
    """
    result = [" " + line + " " for line in lines]
    width = len(result[0])
    result.insert(0, " " * width)
    result.append(" " * width)
    return result


def parse_input(lines):
    passages = set()
    portals = defaultdict(list)

    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            cell = (x, y)

            if char == ".":
                passages.add(cell)
            elif char.isupper():
                other_char = None
                portal_cell = None

                # look down or right for pair
                # portal labels are read left-right or top-down
                # also look for open tile next to portal
                if lines[y + 1][x].isupper():
                    # vertical
                    other_char = lines[y + 1][x]
                    if lines[y + 2][x] == ".":
                        portal_cell = (x, y + 2)
                    elif lines[y - 1][x] == ".":
                        portal_cell = (x, y - 1)
                    else:
                        raise Exception("did not find portal")
                elif lines[y][x + 1].isupper():
                    # horizontal
                    other_char = lines[y][x + 1]
                    if lines[y][x + 2] == ".":
                        portal_cell = (x + 2, y)
                    elif lines[y][x - 1] == ".":
                        portal_cell = (x - 1, y)
                    else:
                        raise Exception("did not find portal")

                # other_char can stay None if we stand on the
                # second character of the portal label
                if other_char is not None:
                    portal = char + other_char
                    portals[portal].append(portal_cell)

    # sanity check portal parsing
    for portal, tiles in portals.items():
        if portal in {"AA", "ZZ"}:
            assert len(tiles) == 1
        else:
            assert len(tiles) == 2

    return passages, portals


def create_portal_tile_mapping(portals):
    """
    Returns a mapping for every portal's tile pair
    Eg. if portals is {"AB": [(x1, y1), (x2, y2)]}
    this function returns {(x1, y1): (x2, y2), (x2, y2): (x1, y1)}

    Ignores "AA" and "ZZ" portals
    """

    result = {}

    for portal, tiles in portals.items():
        if portal in {"AA", "ZZ"}:
            continue
        tile_1, tile_2 = tiles
        result[tile_1] = tile_2
        result[tile_2] = tile_1

    return result


def neighbours(pos, passages, portal_tile_map):
    x, y = pos
    candidates = [
        (x - 1, y),
        (x + 1, y),
        (x, y - 1),
        (x, y + 1),
    ]
    for c in candidates:
        if c in passages:
            yield c
    if pos in portal_tile_map:
        yield portal_tile_map[pos]


def shortest_path_dijkstra(start, target, passages, portal_tile_map):
    discovered = set()

    distances = {}
    tentative_distances = {start: 0}

    while len(tentative_distances) > 0:
        current = min(tentative_distances.items(), key=lambda pair: pair[1])[0]

        discovered.add(current)
        distances[current] = tentative_distances[current]
        del tentative_distances[current]

        if target in discovered:
            break

        for n in neighbours(current, passages, portal_tile_map):
            if n in discovered:
                continue

            if n in tentative_distances:
                tentative_distances[n] = min(
                    tentative_distances[n], distances[current] + 1
                )
            else:
                tentative_distances[n] = distances[current] + 1

    return distances[target]


def shortest_path_bfs(start, target, passages, portal_tile_map):
    discovered = {start}
    distances = {start: 0}
    to_visit = deque([start])

    while len(to_visit) > 0:
        current = to_visit.popleft()

        for n in neighbours(current, passages, portal_tile_map):
            if n in discovered:
                continue

            distances[n] = distances[current] + 1
            discovered.add(n)
            to_visit.append(n)

        if target in discovered:
            break

    return distances[target]


def part_one():
    lines = add_padding(read_input("./input.txt"))
    passages, portals = parse_input(lines)

    portal_tile_map = create_portal_tile_mapping(portals)

    start = portals["AA"][0]
    target = portals["ZZ"][0]

    # BFS can be used because every "edge" (step) in the graph
    # has weight 1
    print(shortest_path_bfs(start, target, passages, portal_tile_map))
    print(shortest_path_dijkstra(start, target, passages, portal_tile_map))


if __name__ == "__main__":
    part_one()

