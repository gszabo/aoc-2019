from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Position:
    x: int
    y: int
    z: int

    def add_velocity(self, velocity: Velocity):
        return Position(self.x + velocity.x, self.y + velocity.y, self.z + velocity.z)

    def abs_sum(self):
        return abs(self.x) + abs(self.y) + abs(self.z)

    def __repr__(self):
        return f"x={self.x:3}, y={self.y:3}, z={self.z:3}"


@dataclass
class Velocity:
    x: int
    y: int
    z: int

    def change(self, delta_x, delta_y, delta_z):
        return Velocity(self.x + delta_x, self.y + delta_y, self.z + delta_z)

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
        self.pos = self.pos.add_velocity(self.vel)

    def apply_gravity(self, other_moon: Moon):
        delta_x = sign(other_moon.pos.x - self.pos.x)
        delta_y = sign(other_moon.pos.y - self.pos.y)
        delta_z = sign(other_moon.pos.z - self.pos.z)
        self.vel = self.vel.change(delta_x, delta_y, delta_z)

    def total_energy(self):
        potential_energy = self.pos.abs_sum()
        kinetic_energy = self.vel.abs_sum()
        return potential_energy * kinetic_energy


def simulate_moons(step_count, moons):
    for _ in range(0, step_count):
        moons = simulation_step(moons)
    return moons


def simulation_step(moons):
    for (moon1, moon2) in every_pair(moons, moons):
        if moon1 != moon2:
            moon1.apply_gravity(moon2)

    for moon in moons:
        moon.move()

    return moons


def find_cycle_for_axis(moons, axis):
    # mutates the objects inside moons!!!
    # if you want to call this function multiple times,
    # recreate moons every time

    def state(moons):
        return [(getattr(moon.pos, axis), getattr(moon.vel, axis)) for moon in moons]

    initial_state = state(moons)

    i = 0
    while True:
        moons = simulation_step(moons)
        i += 1
        if state(moons) == initial_state:
            return i


def gcd(a, b):
    """
    Greatest common divisor
    """
    if a <= 0 or b <= 0:
        raise Exception("gcd here is only implemented for positive integers")

    while b != 0:
        a, b = b, a % b

    return a


def lcm(a, b):
    """
    Least common multiple
    """
    return a * b // gcd(a, b)



def create_input():
    return [
        Moon(Position(16, -8, 13)),
        Moon(Position(4, 10, 10)),
        Moon(Position(17, -5, 6)),
        Moon(Position(13, -3, 0)),
    ]


def part_one():
    moons = create_input()

    step_count = 1000

    moons = simulate_moons(step_count, moons)

    answer = sum(map(Moon.total_energy, moons))

    print(answer)


def part_two():
    x_cycle = find_cycle_for_axis(create_input(), "x")
    y_cycle = find_cycle_for_axis(create_input(), "y")
    z_cycle = find_cycle_for_axis(create_input(), "z")
    answer = lcm(x_cycle, lcm(y_cycle, z_cycle))
    print(answer)


if __name__ == "__main__":
    part_one()
    print()
    part_two()
