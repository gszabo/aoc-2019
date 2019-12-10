import math
from collections import defaultdict
from dataclasses import dataclass

# x goes right
# y goes down


@dataclass
class Point:
    x: int
    y: int

    def __hash__(self):
        return hash((self.x, self.y))

    def __sub__(self, other):
        return DirectionVector(self.x - other.x, self.y - other.y)


@dataclass
class DirectionVector:
    x: int
    y: int

    def __init__(self, x, y):
        div = gcd(x, y)
        self.x = x // div
        self.y = y // div

    def __hash__(self):
        return hash((self.x, self.y))


def gcd(a: int, b: int) -> int:
    """
    Returns the greatest common divisor of |a| and |b|
    """
    a = abs(a)
    b = abs(b)

    a, b = max(a, b), min(a, b)

    if a == 0 and b == 0:
        raise Exception("gcd(0, 0)")

    # Euclidean algorithm
    while b != 0:
        a, b = b, a % b

    return a


def read_asteroids(path):
    asteroids = []

    with open(path) as f:
        lines = list(map(list, map(str.strip, f.readlines())))

    for y in range(0, len(lines)):
        for x in range(0, len(lines[y])):
            if lines[y][x] == "#":
                asteroids.append(Point(x, y))

    return asteroids


def visible_count_from(viewpoint, all):
    directions = set()

    for asteroid in all:
        if asteroid == viewpoint:
            continue

        directions.add(asteroid - viewpoint)

    return viewpoint, len(directions)


def angle_with_upwards(vector: DirectionVector) -> float:
    """
    Returns the rotation angle (in radians) 
    from the upward unit vector to the given vector.
    """

    upward = DirectionVector(0, -1)
    downward = DirectionVector(0, 1)

    if vector == upward:
        return 0
    elif vector == downward:
        return math.pi
    elif vector.x > 0:
        return math.pi / 2 + math.atan(vector.y / vector.x)
    elif vector.x < 0:
        return 3 * math.pi / 2 + math.atan(vector.y / vector.x)


def distance_from(p0):
    sqr = lambda x: x * x

    def distance(p):
        return sqr(p0.x - p.x) + sqr(p0.y - p.y)

    return distance


def collect_by_direction(asteroids, viewpoint):
    asteroids_by_direction = defaultdict(list)

    for asteroid in asteroids:
        direction = asteroid - viewpoint
        asteroids_by_direction[direction].append(asteroid)

    for asteroids_in_direction in asteroids_by_direction.values():
        asteroids_in_direction.sort(key=distance_from(viewpoint))

    return asteroids_by_direction


def vaporize(asteroids_by_direction):
    asteroid_count = sum(map(len, asteroids_by_direction.values()))

    directions = list(asteroids_by_direction.keys())
    directions.sort(key=angle_with_upwards)

    vaporized = []

    while len(vaporized) < asteroid_count:
        for direction in directions:
            asteroids_in_direction = asteroids_by_direction[direction]
            if len(asteroids_in_direction) > 0:
                vaporized.append(asteroids_in_direction.pop(0))

    return vaporized


def part_one():
    asteroids = read_asteroids("./input.txt")
    answer = max(
        map(lambda ast: visible_count_from(viewpoint=ast, all=asteroids), asteroids),
        key=lambda pair: pair[1],
    )
    print(answer)


def part_two():
    # result from part one
    laser_station = Point(14, 17)

    asteroids = read_asteroids("./input.txt")
    asteroids.remove(laser_station)

    asteroids_by_direction = collect_by_direction(asteroids, laser_station)

    vaporized = vaporize(asteroids_by_direction)

    luckiest = vaporized[199]
    answer = 100 * luckiest.x + luckiest.y

    print(answer)


if __name__ == "__main__":
    part_one()
    print()
    part_two()
