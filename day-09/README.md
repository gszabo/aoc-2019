# Day 9

https://adventofcode.com/2019/day/9

Changes to my `Intcode` computer:
- _relative mode_
    - It was easy to add to _input_ arguments, but harder for _output_ arguments.
      Immediate mode was not supported for output arguments, so calculating the result
      address was kind of a shortcut before. But it had to support relative mode, so
      I made output argument resolution very similar to input argument resolution.
    - Created an `ArgumentModes` enum so I can use it in the `if .. elif ..` statements,
      instead of magic `"0", "1", "2"` values.
- larger memory than the initial program
    - I chose to initialize a list 10-times as large as the initial program, all to zeroes
      and copied the the program at the beginning of that memory. This makes a copy of the
      program, so it avoids the shared mutable memory problem I found in [Day 7](../day-07).
    - Other options could have been:
        - declare a large constant and always create a list/array with that size
        - dynamically extend the program's memory when needed
- support large numbers
    - this was already working, because python's `int` type is arbitrary precision.