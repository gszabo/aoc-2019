

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
            instruction(parameters)
            self.instruction_pointer += 1 + len(parameters)
        
        return self.outputs

    def decode(self):
        command = self.program[self.instruction_pointer]
        opcode = command % 100
        opcodemap = {
            1: self.add,
            2: self.multiply,
            3: self.input,
            4: self.outputs,
            99: self.halt
        }
        parameters = [] # TODO
        return opcodemap[opcode], parameters

    def halt(self):
        self.stopped = True

    def add(self, lhs, rhs, result):
        self.program[result] = lhs + rhs

    def multiply(self, lhs, rhs, result):
        self.program[result] = lhs * rhs

    def input(self, result):
        self.program[result] = self.inputs.pop(0)

    def output(self, something):
        self.outputs.append(something)


    