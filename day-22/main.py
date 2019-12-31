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
        self._a0 = a0
        self._a1 = a1
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


def part_one():
    DECK_SIZE = 10007

    lines = []
    with open("./input.txt") as f:
        lines = list(map(str.strip, f.readlines()))

    polynoms = []

    for line in lines:
        if line == "deal into new stack":
            polynoms.append(deal_into_new_stack(DECK_SIZE))
        elif line.startswith("deal with increment"):
            increment = int(line[len("deal with increment ") :])
            polynoms.append(deal_with_increment(DECK_SIZE, increment))
        elif line.startswith("cut"):
            n = int(line[len("cut ") :])
            polynoms.append(cut(DECK_SIZE, n))
        else:
            raise Exception("unknown line: " + line)

    combined = functools.reduce(Polynom.pipe, polynoms)

    answer = combined.evaluate(2019)

    print(answer)


if __name__ == "__main__":
    part_one()
