from computer import Computer

class AsciiInputOutput:

    def __init__(self):
        self._buffer = []

    def has_next(self):
        if len(self._buffer) == 0:
            line = input("> ")
            line += "\n"
            self._buffer.extend(map(ord, line))
        
        return True

    def read_next(self):
        return self._buffer.pop(0)

    def write(self, value):
        if 0 <= value <= 255:
            print(chr(value), end="")
        else:
            print(value)


if __name__ == "__main__":
    with open("./input.txt") as f:
        program = list(map(int, f.readline().strip().split(",")))

    io = AsciiInputOutput()
    c = Computer(program, io, io)

    c.run()

    