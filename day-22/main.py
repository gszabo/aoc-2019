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

        if self._a1 == (self._modulo - 1) or self._a1 == 1:
            # we need this shortcut to be able to quickly invert
            # deal_into_new_stack
            inverter = self._a1
        else:
            q = None
            for i in range(1, self._a1 + 1):
                if ((i * self._modulo) % self._a1) == (self._a1 - 1):
                    q = i
                    break

            inverter = (q * self._modulo + 1) // self._a1

        return Polynom(-inverter * self._a0, inverter, self._modulo)

    def times(self, n: int):
        if n == 0:
            return Polynom.identity(self._modulo)
        else:
            result = self
            for _ in range(1, n):
                result = result.pipe(self)
            return result

    def __repr__(self):
        return f"({self._a1} * x + {self._a0}) mod {self._modulo}"

    @staticmethod
    def identity(modulo):
        return Polynom(0, 1, modulo)


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


def part_two():
    DECK_SIZE = 119315717514047
    LOOP_COUNT = 101_741_582_076_661

    polynoms = read_input("./input.txt", DECK_SIZE)
    inverse = functools.reduce(
        Polynom.pipe, reversed(list(map(Polynom.inverse, polynoms)))
    )

    # For the answer we need to compute the polynom inverse.times(LOOP_COUNT).
    # LOOP_COUNT is a huge number, so the above call won't finish in human time.
    # inverse.times(LOOP_COUNT) can be translated to
    # inverse.pipe(inverse).pipe(inverse)....pipe(inverse)
    #
    # Piping is associative:
    # a.pipe(b).pipe(c) == a.pipe(b.pipe(c))
    # so every (let's say) 1000 pipes can be grouped
    # and replaced with the result of inverse.times(1000).
    #
    # That way inverse.times(LOOP_COUNT) becomes
    # (inverse.times(1000).times(LOOP_COUNT // 1000)).pipe(inverse.times(LOOP_COUNT % 1000))
    #
    # LOOP_COUNT // 1000 is still too huge, but we can apply the same idea again and again

    # going up 3 decimal places at a time
    # Of course this could be replaced with a loop, but is looks nice
    # written out by hand
    one = inverse
    thousand = one.times(1000)
    million = thousand.times(1000)
    billion = million.times(1000)
    trillion = billion.times(1000)

    trillions = LOOP_COUNT // 1_000_000_000_000
    billions = LOOP_COUNT // 1_000_000_000 % 1000
    millions = LOOP_COUNT // 1_000_000 % 1000
    thousands = LOOP_COUNT // 1_000 % 1000
    ones = LOOP_COUNT % 1000

    full_inverse = (
        trillion.times(trillions)
        .pipe(billion.times(billions))
        .pipe(million.times(millions))
        .pipe(thousand.times(thousands))
        .pipe(one.times(ones))
    )

    answer = full_inverse.evaluate(2020)

    print(answer)


def inverse_test_1():
    # Check to see that the inverse gives back 2019 to the solution of part 1

    DECK_SIZE = 10007

    polynoms = read_input("./input.txt", DECK_SIZE)

    # inverting the combined polynom
    combined = functools.reduce(Polynom.pipe, polynoms)

    inverse = combined.inverse()

    answer = inverse.evaluate(4284)

    print(answer)


def inverse_test_2():
    # Check to see that the inverse gives back 2019 to the solution of part 1
    
    DECK_SIZE = 10007

    polynoms = read_input("./input.txt", DECK_SIZE)

    # inverting each polynom individually and combining them in reverse order
    inverse = functools.reduce(
        Polynom.pipe, reversed(list(map(Polynom.inverse, polynoms)))
    )

    answer = inverse.evaluate(4284)

    print(answer)


if __name__ == "__main__":
    part_one()
    inverse_test_1()
    inverse_test_2()
    part_two()
