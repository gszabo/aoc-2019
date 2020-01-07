from collections import deque
from functools import wraps


def memoize(f):
    cache = {}

    @wraps(f)
    def memoized(*args):
        if args in cache:
            return cache[args]
        else:
            result = f(*args)
            cache[args] = result
            return result

    return memoized


def part_one():
    with open("./input.txt") as f:
        lines = list(map(str.strip, f.readlines()))

    walls = set()
    corridors = set()
    keys = dict()
    keys_by_pos = dict()
    doors = dict()
    doors_by_pos = dict()

    start_pos = None

    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            cell = (x, y)
            if char == "#":
                walls.add(cell)
            elif char == "@":
                start_pos = cell
                corridors.add(cell)
            elif char == ".":
                corridors.add(cell)
            elif char.islower():
                keys[char] = cell
                keys_by_pos[cell] = char
                corridors.add(cell)
            elif char.isupper():
                doors[char] = cell
                doors_by_pos[cell] = char
                corridors.add(cell)

    def neighbours(pos):
        x, y = pos
        yield (x + 1, y)
        yield (x - 1, y)
        yield (x, y + 1)
        yield (x, y - 1)

    def reachable_keys_from(pos, obtained_keys):
        # BFS from pos along the corridors
        # to every reachable unobtained key
        to_visit = deque([pos])
        discovered = {pos}
        distances = {pos: 0}

        result = {}

        while len(to_visit) > 0:
            current = to_visit.popleft()
            for cell in filter(corridors.__contains__, neighbours(current)):
                if cell in discovered:
                    continue

                if cell in doors_by_pos:
                    door = doors_by_pos[cell]
                    key = door.lower()
                    if key in obtained_keys:
                        # we have the key to the door
                        # step on the door
                        to_visit.append(cell)
                        discovered.add(cell)
                        distances[cell] = distances[current] + 1

                elif cell in keys_by_pos:
                    key = keys_by_pos[cell]
                    if key in obtained_keys:
                        # this key already picked up
                        # step on this cell
                        to_visit.append(cell)
                        discovered.add(cell)
                        distances[cell] = distances[current] + 1
                    else:
                        # this is new key, stop here
                        discovered.add(cell)
                        distances[cell] = distances[current] + 1
                        result[key] = distances[cell]

                else:
                    # should be regular corridor cell
                    to_visit.append(cell)
                    discovered.add(cell)
                    distances[cell] = distances[current] + 1

        return result

    @memoize
    def shortest_path_from(pos, obtained_keys):
        if len(obtained_keys) == len(keys):
            return 0, []

        rk = reachable_keys_from(pos, obtained_keys)

        candidates = []

        for key, path_len in rk.items():
            further_path_len, further_path = shortest_path_from(
                keys[key], obtained_keys | {key}
            )
            candidates.append((path_len + further_path_len, [key] + further_path))

        return min(candidates, key=lambda pair: pair[0])

    # frozenset, so that the memoize decorator can hash it
    answer = shortest_path_from(start_pos, frozenset())

    print(answer)


def part_two():
    with open("./input-2.txt") as f:
        lines = list(map(str.strip, f.readlines()))

    walls = set()
    corridors = set()
    keys = dict()
    keys_by_pos = dict()
    doors = dict()
    doors_by_pos = dict()

    entrances = list()

    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            cell = (x, y)
            if char == "#":
                walls.add(cell)
            elif char == "@":
                entrances.append(cell)
                corridors.add(cell)
            elif char == ".":
                corridors.add(cell)
            elif char.islower():
                keys[char] = cell
                keys_by_pos[cell] = char
                corridors.add(cell)
            elif char.isupper():
                doors[char] = cell
                doors_by_pos[cell] = char
                corridors.add(cell)

    def neighbours(pos):
        x, y = pos
        yield (x + 1, y)
        yield (x - 1, y)
        yield (x, y + 1)
        yield (x, y - 1)

    def reachable_keys_from(pos, obtained_keys):
        # BFS from pos along the corridors
        # to every reachable unobtained key
        to_visit = deque([pos])
        discovered = {pos}
        distances = {pos: 0}

        result = {}

        while len(to_visit) > 0:
            current = to_visit.popleft()
            for cell in filter(corridors.__contains__, neighbours(current)):
                if cell in discovered:
                    continue

                if cell in doors_by_pos:
                    door = doors_by_pos[cell]
                    key = door.lower()
                    if key in obtained_keys:
                        # we have the key to the door
                        # step on the door
                        to_visit.append(cell)
                        discovered.add(cell)
                        distances[cell] = distances[current] + 1

                elif cell in keys_by_pos:
                    key = keys_by_pos[cell]
                    if key in obtained_keys:
                        # this key already picked up
                        # step on this cell
                        to_visit.append(cell)
                        discovered.add(cell)
                        distances[cell] = distances[current] + 1
                    else:
                        # this is new key, stop here
                        discovered.add(cell)
                        distances[cell] = distances[current] + 1
                        result[key] = distances[cell]

                else:
                    # should be regular corridor cell
                    to_visit.append(cell)
                    discovered.add(cell)
                    distances[cell] = distances[current] + 1

        return result

    @memoize
    def shortest_path_from(positions, obtained_keys):
        if len(obtained_keys) == len(keys):
            return 0, []

        candidates = []

        for i, pos in enumerate(positions):
            rk = reachable_keys_from(pos, obtained_keys)

            for key, path_len in rk.items():
                new_positions = list(positions)
                new_positions[i] = keys[key]
                further_path_len, further_path = shortest_path_from(
                    tuple(new_positions), obtained_keys | {key}
                )
                candidates.append((path_len + further_path_len, [f"{i}{key}"] + further_path))

        return min(candidates, key=lambda pair: pair[0])

    # frozenset, so that the memoize decorator can hash it
    answer = shortest_path_from(tuple(entrances), frozenset())

    print(answer)


if __name__ == "__main__":
    part_one()
    print()
    part_two()
