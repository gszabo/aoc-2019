# Day 7

https://adventofcode.com/2019/day/7

For part 2 I had to add a _waiting for input_ feature to the `Computer` class.
Besides, I refactored the input/output handling and state maintenance. This way the buffers
that serve as connections between the amps are more visible in the code.

Lessons learned:
- generating permutations:
    - should look up backtrack algorithms
    - my version is probably very memory inefficient
    - maybe it would have been faster if I had just written out
      the permutations by hand
- shared mutable memory is dangerous
    - I used them as buffers between the amps, one end produces values,
      other end consumes them, this is fine here
    - I **accidentally** used share mutable memory for the program code
      of the amplifiers. I didn't do a defensive copy neither in the
      `Computer` class, nor in `main`. It's a miracle that I still got
      the good answer for part 1, but it caused massive amount of 
      debugging in part 2. Basically the amps were changing each others'
      code under themselves, when they should have only been changing
      their **own** code. To debug this, I had to manually interpret 
      one of the given sample programs ([see here](./debug_part_2_sample_program_1.txt)),
      and figure out why I had infinite loops instead of nicely halting
      programs.