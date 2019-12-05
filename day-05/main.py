

class Computer:

    def __init__(self, program, inputs):
        self.program = program
        self.inputs = inputs
        self.instruction_pointer = 0
        self.outputs = []
        self.stopped = False

    def run(self):
        while not self.stopped:
            instruction, parameters = self.decode()
            instruction(*parameters)
            self.instruction_pointer += 1 + len(parameters)
        
        return self.outputs

    def decode(self):
        command = self.program[self.instruction_pointer]
        opcode = command % 100
        opcodemap = {
            1: self.add,
            2: self.multiply,
            3: self.input,
            4: self.output,
            99: self.halt
        }
        input_argument_count_map = {
            1: 2,
            2: 2,
            3: 0,
            4: 1,
            5: 2,
            6: 2,
            7: 2,
            8: 2,
            99: 0
        }
        opcodes_with_output = [1, 2, 3]
        parameters = []
        
        input_argument_count = input_argument_count_map[opcode]
        if input_argument_count > 0:
            modes = list(f"{command//100:0{input_argument_count}}")
            for i in range(1, input_argument_count + 1):
                mode = modes.pop()
                if mode == "0":
                    # position mode
                    position = self.program[self.instruction_pointer + i]
                    parameters.append(self.program[position])
                elif mode == "1":
                    # immediate mode
                    value = self.program[self.instruction_pointer + i]
                    parameters.append(value)
                else:
                    raise Exception("unknown mode")

        if opcode in opcodes_with_output:
            # add result address to parameters
            result_addr = self.program[self.instruction_pointer + input_argument_count + 1]
            parameters.append(result_addr)
        
        return opcodemap[opcode], parameters

    def halt(self):
        self.stopped = True

    def add(self, lhs, rhs, result_addr):
        self.program[result_addr] = lhs + rhs

    def multiply(self, lhs, rhs, result_addr):
        self.program[result_addr] = lhs * rhs

    def input(self, result_addr):
        self.program[result_addr] = self.inputs.pop(0)

    def output(self, something):
        self.outputs.append(something)


def part_one():
    with open("./input.txt") as f:
        line = f.readline().strip()
    program = list(map(int, line.split(",")))
    inputs = [1]
    c = Computer(program, inputs)
    print(c.run())


if __name__ == "__main__":
    part_one()