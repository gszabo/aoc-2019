# Day 19

https://adventofcode.com/2019/day/19

Part one was two nested for loops in the given range, and increasing a counter if the
Intcode output was 1.

Part two was a manual guessing. I created helper functions that find the first cell
of the beam in a row or in a column. The user gives an input `y` coordinate, the
code finds the first cell of the beam in that row, and that cell is the lower left
corner of the 100x100 box. Then it finds the first cell in the column 99 columns away
from the lower left corner. It prints the result and the user if left to decide whether
the given area is large enough to fit the 100x100 box.