from __future__ import annotations

import functools


def deal_into_new_stack(card_count):
    return Polynom(-1, -1, card_count)


def deal_with_increment(card_count, increment):
    return Polynom(0, increment, card_count)


def cut(card_count, n):
    return Polynom(-n, 1, card_count)


class Polynom:
    def __init__(self, a0: int, a1: int, modulo: int):
        self._a0 = a0 % modulo
        self._a1 = a1 % modulo
        self._modulo = modulo

    def evaluate(self, x: int):
        return (self._a1 * x + self._a0) % self._modulo

    def pipe(self, other: Polynom):
        """
        Returns (self | other)(x), ie. other(self(x))
        """

        if self._modulo != other._modulo:
            raise Exception("combining with different modulo")

        return Polynom(
            a0=other._a1 * self._a0 + other._a0,
            a1=other._a1 * self._a1,
            modulo=self._modulo,
        )

    def inverse(self):
        if self._a1 == 0:
            raise Exception("cannot invert constant")

        q = None
        for i in range(1, self._a1 + 1):
            if ((i * self._modulo) % self._a1) == (self._a1 - 1):
                q = i
                break

        inverter = (q * self._modulo + 1) // self._a1

        return Polynom(-inverter * self._a0, inverter, self._modulo)

    def __repr__(self):
        return f"({self._a1} * x + {self._a0}) mod {self._modulo}"


def read_input(path, deck_size):
    lines = []
    with open(path) as f:
        lines = list(map(str.strip, f.readlines()))

    polynoms = []

    for line in lines:
        if line == "deal into new stack":
            polynoms.append(deal_into_new_stack(deck_size))
        elif line.startswith("deal with increment"):
            increment = int(line[len("deal with increment ") :])
            polynoms.append(deal_with_increment(deck_size, increment))
        elif line.startswith("cut"):
            n = int(line[len("cut ") :])
            polynoms.append(cut(deck_size, n))
        else:
            raise Exception("unknown line: " + line)

    return polynoms


def part_one():
    DECK_SIZE = 10007

    polynoms = read_input("./input.txt", DECK_SIZE)

    combined = functools.reduce(Polynom.pipe, polynoms)

    answer = combined.evaluate(2019)

    print(answer)


def inverse_test_1():
    # inverting the combined polynom

    DECK_SIZE = 10007

    polynoms = read_input("./input.txt", DECK_SIZE)

    combined = functools.reduce(Polynom.pipe, polynoms)

    inverse = combined.inverse()

    answer = inverse.evaluate(4284)

    print(answer)


def inverse_test_2():
    # inverting each polynom individually and combining them in reverse order

    DECK_SIZE = 10007

    polynoms = read_input("./input.txt", DECK_SIZE)

    inverse = functools.reduce(Polynom.pipe, reversed(list(map(Polynom.inverse, polynoms))))

    answer = inverse.evaluate(4284)

    print(answer)


if __name__ == "__main__":
    part_one()
    inverse_test_1()
    inverse_test_2()
