from computer import Computer, InputReader, OutputWriter, States


def test_waiting_for_input():
    program = [3, 5, 4, 5, 99, 500]
    input_buffer = []
    output_buffer = []

    TOT = Computer(program, InputReader(input_buffer), OutputWriter(output_buffer))
    TOT.run()

    assert TOT.state() == States.WAITING_FOR_INPUT
    assert output_buffer == []

    input_buffer.append(42)
    TOT.run()

    assert TOT.state() == States.HALTED
    assert output_buffer == [42]
