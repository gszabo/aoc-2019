from __future__ import annotations

from collections import defaultdict
from curses import wrapper
from time import sleep

import curses

from computer import Computer, InputReader

EMPTY = 0
WALL = 1
BLOCK = 2
HORIZONTAL_PADDLE = 3
BALL = 4

CHARS = {EMPTY: " ", WALL: "#", BLOCK: "X", HORIZONTAL_PADDLE: "=", BALL: "o"}

BALL_POS = {"x": 0}
PADDLE_POS = {"x": 0}


class Screen:
    def __init__(self):
        self._grid = defaultdict(int)
        self.score = 0
        self.max_score = 0
        

    def put_tile(self, x, y, tile_type):
        self._grid[(x, y)] = tile_type
        if tile_type == BALL:
            BALL_POS["x"] = x
        if tile_type == HORIZONTAL_PADDLE:
            PADDLE_POS["x"] = x

    def number_of_tiles(self, tile_type):
        return len([tile for tile in self._grid.values() if tile == tile_type])

    def print_to(self, stdscr):
        stdscr.clear()

        for y in range(0, 25):
            for x in range(0, 40):
                stdscr.addstr(y, x, CHARS[self._grid[(x, y)]])

        stdscr.addstr(11, 50, "Score:")
        stdscr.addstr(12, 50, str(self.score))

        stdscr.addstr(11, 70, "Max score:")
        stdscr.addstr(12, 70, str(self.max_score))

        stdscr.refresh()


class JoystickInput:
    def __init__(self, stdscr):
        self._stdscr = stdscr
        self._value = 0

    def has_next(self):
        return True

    def read_next(self):
        try:
            c = self._stdscr.getch()
            if c == curses.KEY_LEFT:
                self.left()
            elif c == curses.KEY_RIGHT:
                self.right()
            elif c == curses.KEY_DOWN:
                self._value = 0
        except:
            pass
        # sleep(0.5)
        # result = self._value
        # self._value = 0
        # return result
        if PADDLE_POS["x"] < BALL_POS["x"]:
            return 1
        elif BALL_POS["x"] < PADDLE_POS["x"]:
            return -1
        else:
            return 0

    def left(self):
        self._value = -1

    def right(self):
        self._value = 1


class ScreenOutputWriter:
    def __init__(self, screen: Screen, stdscr):
        self._screen = screen
        self._stdscr = stdscr
        self._buffer = []

    def write(self, value):
        self._buffer.append(value)
        if len(self._buffer) == 3:
            self._flush_to_screen()

    def _flush_to_screen(self):
        x, y, value = self._buffer
        
        if x == -1 and y == 0:
            # TODO: refactor this
            self._screen.max_score = max(value, self._screen.score)
            self._screen.score = value
        else:
            self._screen.put_tile(x, y, value)

        if self._stdscr is not None:
            self._screen.print_to(self._stdscr)
        
        self._buffer.clear()


def part_one():
    with open("./input.txt") as f:
        program = list(map(int, f.readline().strip().split(",")))

    screen = Screen()

    c = Computer(program, InputReader([]), ScreenOutputWriter(screen, None))
    c.run()

    answer = screen.number_of_tiles(BLOCK)

    print(answer)


def part_two(stdscr):
    # screen is about 40x25
    # maybe try the curses library
    # https://docs.python.org/3/howto/curses.html#curses-howto

    with open("./input.txt") as f:
        program = list(map(int, f.readline().strip().split(",")))

    screen = Screen()
    joystick = JoystickInput(stdscr)
    # TODO: maybe throttle computer running?

    curses.halfdelay(10)

    # insert coin
    program[0] = 2

    c = Computer(program, joystick, ScreenOutputWriter(screen, stdscr))
    c.run()

    curses.nocbreak()

    stdscr.getkey()



if __name__ == "__main__":
    wrapper(part_two)
