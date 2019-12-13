from __future__ import annotations

from collections import defaultdict

from computer import Computer, InputReader

EMPTY = 0
WALL = 1
BLOCK = 2
HORIZONTAL_PADDLE = 3
BALL = 4

CHARS = {EMPTY: " ", WALL: "#", BLOCK: "X", HORIZONTAL_PADDLE: "=", BALL: "o"}


class Screen:
    def __init__(self):
        self._grid = defaultdict(int)

    def put_tile(self, x, y, tile_type):
        self._grid[(x, y)] = tile_type

    def number_of_tiles(self, tile_type):
        return len([tile for tile in self._grid.values() if tile == tile_type])


class ScreenOutputWriter:
    def __init__(self, screen: Screen):
        self._screen = screen
        self._buffer = []

    def write(self, value):
        self._buffer.append(value)
        if len(self._buffer) == 3:
            self._flush_to_screen()

    def _flush_to_screen(self):
        x, y, tile_type = self._buffer
        self._screen.put_tile(x, y, tile_type)
        self._buffer.clear()


def part_one():
    with open("./input.txt") as f:
        program = list(map(int, f.readline().strip().split(",")))

    screen = Screen()

    c = Computer(program, InputReader([]), ScreenOutputWriter(screen))
    c.run()

    answer = screen.number_of_tiles(BLOCK)

    print(answer)


def part_two():
    # screen is about 40x25
    # maybe try the curses library
    # https://docs.python.org/3/howto/curses.html#curses-howto

    with open("./input.txt") as f:
        program = list(map(int, f.readline().strip().split(",")))

    screen = Screen()
    # TODO: segment display for score
    # TODO: joystick input
    # TODO: maybe throttle computer running?

    c = Computer(program, InputReader([]), ScreenOutputWriter(screen))
    c.run()


if __name__ == "__main__":
    part_one()
