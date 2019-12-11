from collections import defaultdict

from computer import Computer


class SpaceCraftSideReaderWriter:
    def __init__(self):
        self._field = defaultdict(int)
        self._robot_position = (0, 0)
        self._robot_direction = (0, 1)
        self._waiting_for_paint_color = True

    def painted_panels(self):
        return list(self._field.keys())

    def has_next(self):
        return True

    def read_next(self):
        return self._field[self._robot_position]

    def write(self, value):
        if self._waiting_for_paint_color:
            self._field[self._robot_position] = value
        else:
            self._turn(value)
            self._step()

        self._waiting_for_paint_color = not self._waiting_for_paint_color

    def _turn(self, direction):
        if direction == 0:
            # left
            dir_x, dir_y = self._robot_direction
            self._robot_direction = (-dir_y, dir_x)
        elif direction == 1:
            # right
            dir_x, dir_y = self._robot_direction
            self._robot_direction = (dir_y, -dir_x)
        else:
            raise Exception("unknown direction: " + direction)

    def _step(self):
        pos_x, pos_y = self._robot_position
        dir_x, dir_y = self._robot_direction
        self._robot_position = (pos_x + dir_x, pos_y + dir_y)


def part_one():
    with open("./input.txt") as f:
        program = list(map(int, f.readline().strip().split(",")))

    vmi = SpaceCraftSideReaderWriter()

    c = Computer(program, vmi, vmi)
    c.run()

    answer = len(vmi.painted_panels())

    print(answer)


if __name__ == "__main__":
    part_one()
