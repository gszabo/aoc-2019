from collections import defaultdict

from computer import Computer

BLACK = 0
WHITE = 1


class PaintBoardReaderWriter:
    def __init__(self, start_color):
        self._board = defaultdict(int)

        self._robot_position = (0, 0)
        self._robot_direction = (0, 1)

        self._board[self._robot_position] = start_color

        self._waiting_for_paint_color = True

    def painted_panels(self):
        return list(self._board.keys())

    def print_board(self):
        x_min, x_max, y_min, y_max = self._board_range()

        full_board = []
        for _ in range(0, y_max - y_min + 1):
            black_row = [BLACK] * (x_max - x_min + 1)
            full_board.append(black_row)

        for (x, y), color in self._board.items():
            full_board[y - y_min][x - x_min] = color

        for row in reversed(full_board):
            # the top row has the largest y coordinate
            # but it's printed first
            # so we need to print in reversed order
            print("".join(map(self._pixel_to_print_char, row)))

    def _pixel_to_print_char(self, pixel):
        if pixel == BLACK:
            return " "
        else:
            return "\u2593"

    def _board_range(self):
        get_x = lambda pair: pair[0]
        get_y = lambda pair: pair[1]

        x_min = min(map(get_x, self._board.keys()))
        x_max = max(map(get_x, self._board.keys()))

        y_min = min(map(get_y, self._board.keys()))
        y_max = max(map(get_y, self._board.keys()))

        return x_min, x_max, y_min, y_max

    def has_next(self):
        return True

    def read_next(self):
        return self._board[self._robot_position]

    def write(self, value):
        # this write callback of the computer implements
        # painting, rotating and moving the robot

        if self._waiting_for_paint_color:
            self._board[self._robot_position] = value
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

    paint_board = PaintBoardReaderWriter(BLACK)

    c = Computer(program, paint_board, paint_board)
    c.run()

    answer = len(paint_board.painted_panels())

    print(answer)


def part_two():
    with open("./input.txt") as f:
        program = list(map(int, f.readline().strip().split(",")))

    paint_board = PaintBoardReaderWriter(WHITE)

    c = Computer(program, paint_board, paint_board)
    c.run()

    paint_board.print_board()


if __name__ == "__main__":
    part_one()
    print()
    part_two()
