from collections import deque
from functools import wraps

from frozendict import frozendict


class Vault:
    """
    Immutable representation of the vault.
    """

    def __init__(
        self, walls, corridors, keys, keys_by_pos, doors, doors_by_pos, entrances
    ):
        self.walls = frozenset(walls)
        self.corridors = frozenset(corridors)
        self.keys = frozendict(keys)
        self.keys_by_pos = frozendict(keys_by_pos)
        self.doors = frozendict(doors)
        self.doors_by_pos = frozendict(doors_by_pos)
        self.entrances = tuple(entrances)

    def neighbours(self, pos):
        x, y = pos
        candidates = [
            (x + 1, y),
            (x - 1, y),
            (x, y + 1),
            (x, y - 1),
        ]
        for c in candidates:
            if c in self.corridors:
                yield c

    def reachable_keys_from(self, pos, obtained_keys):
        # BFS from pos along the corridors
        # to every reachable unobtained key
        to_visit = deque([pos])
        discovered = {pos}
        distances = {pos: 0}

        result = {}

        while len(to_visit) > 0:
            current = to_visit.popleft()
            for cell in self.neighbours(current):
                if cell in discovered:
                    continue

                if cell in self.doors_by_pos:
                    door = self.doors_by_pos[cell]
                    key = door.lower()
                    if key in obtained_keys:
                        # we have the key to the door
                        # step on the door
                        to_visit.append(cell)
                        discovered.add(cell)
                        distances[cell] = distances[current] + 1

                elif cell in self.keys_by_pos:
                    key = self.keys_by_pos[cell]
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

    @staticmethod
    def create(lines):
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

        return Vault(
            walls, corridors, keys, keys_by_pos, doors, doors_by_pos, entrances
        )


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


def update(_tuple, index, new_value):
    result = list(_tuple)
    result[index] = new_value
    return tuple(result)


def part_one():
    with open("./input.txt") as f:
        lines = list(map(str.strip, f.readlines()))

    vault = Vault.create(lines)

    @memoize
    def shortest_path_from(pos, obtained_keys):
        if len(obtained_keys) == len(vault.keys):
            return 0, []

        paths = []

        rk = vault.reachable_keys_from(pos, obtained_keys)
        for key, key_distance in rk.items():
            path_len, path = shortest_path_from(vault.keys[key], obtained_keys | {key})
            paths.append((key_distance + path_len, [key] + path))

        return min(paths, key=lambda pair: pair[0])

    start_pos = vault.entrances[0]

    # frozenset, so that the memoize decorator can hash it
    answer = shortest_path_from(start_pos, frozenset())

    print(answer)


def part_two():
    with open("./input-2.txt") as f:
        lines = list(map(str.strip, f.readlines()))

    vault = Vault.create(lines)

    @memoize
    def shortest_path_from(positions, obtained_keys):
        if len(obtained_keys) == len(vault.keys):
            return 0, []

        paths = []

        for i, pos in enumerate(positions):
            rk = vault.reachable_keys_from(pos, obtained_keys)

            for key, key_distance in rk.items():
                new_pos = update(positions, i, vault.keys[key])
                path_len, path = shortest_path_from(new_pos, obtained_keys | {key})
                paths.append((key_distance + path_len, [f"{i}{key}"] + path))

        return min(paths, key=lambda pair: pair[0])

    # frozenset, so that the memoize decorator can hash it
    answer = shortest_path_from(tuple(vault.entrances), frozenset())

    print(answer)


if __name__ == "__main__":
    part_one()
    print()
    part_two()
