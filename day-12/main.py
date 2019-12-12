from __future__ import annotations

from dataclasses import dataclass
from pprint import pprint


@dataclass
class Position:
    x: int
    y: int
    z: int

    def add_velocity(self, velocity: Velocity):
        self.x += velocity.x
        self.y += velocity.y
        self.z += velocity.z

    def abs_sum(self):
        return abs(self.x) + abs(self.y) + abs(self.z)

    def __repr__(self):
        return f"x={self.x:3}, y={self.y:3}, z={self.z:3}"


@dataclass
class Velocity:
    x: int
    y: int
    z: int

    def abs_sum(self):
        return abs(self.x) + abs(self.y) + abs(self.z)

    def __repr__(self):
        return f"x={self.x:3}, y={self.y:3}, z={self.z:3}"


def sign(x: int) -> int:
    if x > 0:
        return 1
    elif x == 0:
        return 0
    else:
        return -1


def every_pair(iter1, iter2):
    for item1 in iter1:
        for item2 in iter2:
            yield (item1, item2)


class Moon:
    def __init__(self, pos: Position):
        self.pos = pos
        self.vel = Velocity(0, 0, 0)

    def __repr__(self):
        return f"pos=<{self.pos}>, vel=<{self.vel}>"

    def move(self):
        self.pos.add_velocity(self.vel)

    def apply_gravity(self, other_moon: Moon):
        self.vel.x += sign(other_moon.pos.x - self.pos.x)
        self.vel.y += sign(other_moon.pos.y - self.pos.y)
        self.vel.z += sign(other_moon.pos.z - self.pos.z)

    def total_energy(self):
        potential_energy = self.pos.abs_sum()
        kinetic_energy = self.vel.abs_sum()
        return potential_energy * kinetic_energy


def simulate_moons(step_count, moons):
    for _ in range(0, step_count):

        for (moon1, moon2) in every_pair(moons, moons):
            if moon1 != moon2:
                moon1.apply_gravity(moon2)

        for moon in moons:
            moon.move()

    return moons


def part_one():
    moons = [
        Moon(Position(16, -8, 13)),
        Moon(Position(4, 10, 10)),
        Moon(Position(17, -5, 6)),
        Moon(Position(13, -3, 0)),
    ]

    step_count = 1000

    moons = simulate_moons(step_count, moons)

    answer = sum(map(Moon.total_energy, moons))

    print(answer)


if __name__ == "__main__":
    part_one()
