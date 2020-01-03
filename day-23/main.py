from computer import Computer, InputReader


y_values = []


class NAT:
    def __init__(self, inputs):
        self._inputs = inputs
        self._x = None
        self._y = None

    def set_values(self, x, y):
        self._x = x
        self._y = y

    def release(self):
        if self._x is not None and self._y is not None:
            print("Releasing", self._x, self._y)
            self._inputs[0].extend([self._x, self._y])
            if len(y_values) > 0 and y_values[-1] == self._y:
                print("Found", self._y)
                raise Exception()
            y_values.append(self._y)

            self._x = None
            self._y = None
        else:
            print("Not releasing, values not yet set")


class NetworkOutputWriter:
    def __init__(self, inputs, nat):
        self._inputs = inputs
        self._nat = nat
        self._buffer = []

    def write(self, value):
        self._buffer.append(value)
        
        if len(self._buffer) == 3:
            addr, x, y = self._buffer
            
            if addr == 255:
                self._nat.set_values(x, y)
            else:
                self._inputs[addr].extend([x, y])
            
            self._buffer = []


def part_one():
    COMPUTER_COUNT = 50

    with open("./input.txt") as f:
        program = list(map(int, f.readline().strip().split(",")))

    inputs = {}
    computers = {}
    nat = NAT(inputs)
    
    for i in range(0, COMPUTER_COUNT):
        inputs[i] = [i]
        output = NetworkOutputWriter(inputs, nat)
        computers[i] = Computer(program, InputReader(inputs[i]), output)

    while True:
        all_empty_before = all([len(queue) == 0 for queue in inputs.values()])
        for i in range(0, COMPUTER_COUNT):
            computers[i].run(100)
        all_empty_after = all([len(queue) == 0 for queue in inputs.values()])

        if all_empty_before and all_empty_after:
            print("Network seems idle, releasing NAT")
            nat.release()



if __name__ == "__main__":
    part_one()
