from __future__ import annotations

from computer import Computer
from curses import wrapper
import curses
import pickle


NORTH = 1
SOUTH = 2
WEST = 3
EAST = 4


KEYMAP = {
    curses.KEY_DOWN: SOUTH,
    curses.KEY_UP: NORTH,
    curses.KEY_LEFT: WEST,
    curses.KEY_RIGHT: EAST,
}

INVERSE_DIRECTIONS = {
    NORTH: SOUTH,
    SOUTH: NORTH,
    WEST: EAST,
    EAST: WEST,
}


ORIGIN_X = 40
ORIGIN_Y = 20


class KeyboardInputReader:
    def __init__(self, stdscr, robot: Robot, output: ConsoleOutputWriter):
        self._stdscr = stdscr
        self._robot = robot
        self._output = output

    def read(self):
        global ORIGIN_Y
        global ORIGIN_X

        c = self._stdscr.getch()

        if c == ord("l"):
            self._robot.look_around()
        elif c == ord("w"):
            ORIGIN_Y += 10
        elif c == ord("a"):
            ORIGIN_X += 10
        elif c == ord("s"):
            ORIGIN_Y -= 10
        elif c == ord("d"):
            ORIGIN_X -= 10
        elif c == ord("p"):
            self._output.save_to_file()
        else:
            direction = KEYMAP[c]
            self._robot.try_to_step(direction)


class RobotInputReader:
    def __init__(self, robot: Robot):
        self._robot = robot

    def has_next(self):
        return self._robot.new_pos is not None

    def read_next(self):
        return self._robot.step_direction


class Robot:
    def __init__(self):
        self.pos = (0, 0)
        self.step_direction = None
        self.new_pos = None
        self._looking_around = False
        self._stepping_back = False
        self._look_around_steps = []

    def look_around(self):
        # try to step in every direction
        # to explore the possible directions
        self._looking_around = True
        self._stepping_back = False
        self._look_around_steps.extend([NORTH, SOUTH, WEST, EAST])

        self._next_look_around_step()

    def try_to_step(self, direction):
        x, y = self.pos
        if direction == NORTH:
            self.new_pos = (x, y - 1)
        elif direction == SOUTH:
            self.new_pos = (x, y + 1)
        elif direction == WEST:
            self.new_pos = (x - 1, y)
        elif direction == EAST:
            self.new_pos = (x + 1, y)
        else:
            raise Exception("sth is wrong")

        self.step_direction = direction

    def step_success(self):
        self.pos = self.new_pos

        if self._looking_around and not self._stepping_back:
            self._look_around_steps.insert(0, INVERSE_DIRECTIONS[self.step_direction])
            self._stepping_back = True
            self._next_look_around_step()

        elif self._looking_around and self._stepping_back:
            self._stepping_back = False
            self._next_look_around_step()

        else:
            self.new_pos = None
            self.step_direction = None

    def step_failed(self):
        if self._looking_around:
            # try next direction
            self._stepping_back = False
            self._next_look_around_step()
        else:
            self.new_pos = None
            self.step_direction = None

    def _next_look_around_step(self):
        if len(self._look_around_steps) == 0:
            self._looking_around = False
            self._stepping_back = False
            self.new_pos = None
            self.step_direction = None
        else:
            self.try_to_step(self._look_around_steps.pop(0))


class ConsoleOutputWriter:
    def __init__(self, robot: Robot):
        self.walls = set()
        self.corridors = set([robot.pos])
        self.oxygen_tank = None
        self.robot = robot

    def write(self, value):
        if value == 0:
            self.walls.add(self.robot.new_pos)
            self.robot.step_failed()
        elif value == 1:
            self.corridors.add(self.robot.new_pos)
            self.robot.step_success()
        elif value == 2:
            self.oxygen_tank = self.robot.new_pos
            self.corridors.add(self.robot.new_pos)
            self.robot.step_success()
        else:
            raise Exception("wrong value in output: " + value)

    def save_to_file(self):
        with open("./output.dat", "wb") as f:
            data = {
                "walls": self.walls,
                "corridors": self.corridors,
                "oxygen": self.oxygen_tank,
            }
            pickle.dump(data, f)


def draw(stdscr, output: ConsoleOutputWriter):
    stdscr.clear()

    write_to_screen(stdscr, 0, 0, f"Robot @ {output.robot.pos}")
    for x, y in output.walls:
        write_to_screen(stdscr, ORIGIN_Y + y, ORIGIN_X + x, "#")
    for x, y in output.corridors:
        write_to_screen(stdscr, ORIGIN_Y + y, ORIGIN_X + x, ".")
    if output.oxygen_tank is not None:
        x, y = output.oxygen_tank
        write_to_screen(stdscr, ORIGIN_Y + y, ORIGIN_X + x, "O")
    x, y = output.robot.pos
    write_to_screen(stdscr, ORIGIN_Y + y, ORIGIN_X + x, "R")


def write_to_screen(screen, y: int, x: int, text: str):
    height, width = screen.getmaxyx()
    if 0 <= x < width and 0 <= y < height:
        screen.addstr(y, x, text)


def play(stdscr):
    curses.curs_set(0)

    robot = Robot()

    output_writer = ConsoleOutputWriter(robot)
    keyboard_reader = KeyboardInputReader(stdscr, robot, output_writer)
    robot_input_reader = RobotInputReader(robot)

    with open("./input.txt") as f:
        program = list(map(int, f.readline().strip().split(",")))
    c = Computer(program, robot_input_reader, output_writer)

    # Ctrl+C can exit this loop
    while True:
        draw(stdscr, output_writer)
        keyboard_reader.read()
        c.run()


def neighbours(cell, corridors):
    x, y = cell
    candidates = [
        (x + 1, y),
        (x - 1, y),
        (x, y + 1),
        (x, y - 1),
    ]
    return [c for c in candidates if c in corridors]


def part_one():
    with open("./output.dat", "rb") as f:
        data = pickle.load(f)

    corridors = data["corridors"]
    oxygen = data["oxygen"]

    # doing a BFS on the manually collected data
    # to obtain the distances from the starting point
    start = (0, 0)
    distances = {start: 0}
    discovered = {start}

    to_visit = [start]

    while len(to_visit) > 0:
        cell = to_visit.pop(0)
        d_cell = distances[cell]
        for neighbour in neighbours(cell, corridors):
            if neighbour not in discovered:
                to_visit.append(neighbour)
                discovered.add(neighbour)
                distances[neighbour] = d_cell + 1

    answer = distances[oxygen]

    print(answer)


def part_two():
    with open("./output.dat", "rb") as f:
        data = pickle.load(f)

    corridors = data["corridors"]
    oxygen = data["oxygen"]

    # doing a BFS on the manually collected data
    # to obtain the distances from the oxygen tank
    start = oxygen
    distances = {start: 0}
    discovered = {start}

    to_visit = [start]

    while len(to_visit) > 0:
        cell = to_visit.pop(0)
        cell_distance = distances[cell]
        for neighbour in neighbours(cell, corridors):
            if neighbour not in discovered:
                to_visit.append(neighbour)
                discovered.add(neighbour)
                distances[neighbour] = cell_distance + 1

    answer = max(distances.values())

    print(answer)


if __name__ == "__main__":
    # this is to manually explore the whole maze
    # wrapper(play)

    part_one()
    print()
    part_two()

