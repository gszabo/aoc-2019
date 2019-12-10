from dataclasses import dataclass
from pprint import pprint


@dataclass
class Point:
    x: int
    y: int

    def __hash__(self):
        return hash((self.x, self.y))

    def __sub__(self, other):
        return DirectionVector(other.x - self.x, other.y - self.y)


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


def part_one():
    asteroids = []

    with open("./input.txt") as f:
        lines = list(map(list, map(str.strip, f.readlines())))

    for y in range(0, len(lines)):
        for x in range(0, len(lines[y])):
            if lines[y][x] == "#":
                asteroids.append(Point(x, y))

    def visible_asteroids(start):
        directions = set()

        for asteroid in asteroids:
            if asteroid == start:
                continue

            directions.add(asteroid - start)

        return len(directions)

    answer = max(map(visible_asteroids, asteroids))

    pprint(answer)

if __name__ == "__main__":
    part_one()
