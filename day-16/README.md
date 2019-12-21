# Day 16

https://adventofcode.com/2019/day/16

For the repeating pattern in part 1, I leveraged Python's generators and implemented 
the `skip` and `take` combinators myself. `take` is only there for debug purposes, 
the infinite generator is stopped when it is `zip`-ped together with the finite 
number of digits (ie. the input), because `zip` stops when the smaller iterable is
exhausted.

For part 2 I noticed that the offset points way over the half of the extended input.
This means that the pattern for the digit at the offset position is 0 zero below the
offset (meaning those digits in the input can be discarded), and 1 starting from the
offset all the way to the end. For the digit at position `offset + 1` the pattern is 
shifted 1 to the right. Hence, the algorithm can be simplified:
- digits below `offset` can be dropped
- digits starting from `offset` become the sum of the digits to their right 
(including themselves) modulo 10 (to get the last digit)
  - a little optimization can be achieved here. We don't need to always sum up
    digits to the right. We need to sum the digits once at position `offset`, and
    after that a digit at a position can be calculated by subtracting the digit
    from the next value of the previous digit. Ie.
    ```
    next_digits[offset] = sum(digits)
    for idx in offset+1 .. len(digits):
      next_digits[idx] = next_digits[idx - 1] - digits[idx - 1]
    ```
    Of course every position needs to be `mod 10` to get only the last digit.