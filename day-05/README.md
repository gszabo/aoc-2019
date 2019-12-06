# Day 5

https://adventofcode.com/2019/day/5

It was time to reimplement the machine from [Day 2](../day-02).

The basic idea is:
1. decode the instruction at the instruction pointer
    - what instruction to run
    - calculate the parameters (resolve if position mode, just read the value if immediate mode)
    - add output address to store result, if needed. It is important that this is always in
    position mode, but it must not be resolved (by looking up the value at that position),
    the actual address needs to be passed into the function
2. run the instruction
3. move the instruction pointer to next instruction
    - jump statements complicated this. At the end I only move the pointer
    if no jumps happened, and I do that by comparing the value of the
    instruction pointer before and after running the instruction.