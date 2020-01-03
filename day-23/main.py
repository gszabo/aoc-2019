from computer import Computer, InputReader


class NetworkOutputWriter:
    def __init__(self, inputs):
        self._inputs = inputs
        self._buffer = []

    def write(self, value):
        self._buffer.append(value)
        if len(self._buffer) == 3:
            addr, x, y = self._buffer
            if addr == 255:
                print("ANSWER", y)
            self._inputs[addr].extend([x, y])
            self._buffer = []


def part_one():
    COMPUTER_COUNT = 50

    with open("./input.txt") as f:
        program = list(map(int, f.readline().strip().split(",")))

    inputs = {}
    computers = {}
    for i in range(0, COMPUTER_COUNT):
        inputs[i] = [i]
        output = NetworkOutputWriter(inputs)
        computers[i] = Computer(program, InputReader(inputs[i]), output)

    while True:
        for i in range(0, COMPUTER_COUNT):
            computers[i].run(100)


if __name__ == "__main__":
    part_one()
