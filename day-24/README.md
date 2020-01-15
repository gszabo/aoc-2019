# Day 24

https://adventofcode.com/2019/day/24

## Part 1

This is a bounded game of life simulation. I just needed to follow the text of the
problem: for every simulation step, calculate the number of adjacent bugs for each
cell, and update the cells accordingly. 

To simplify the accessing the neighbours of a cell, I gave the matrix an extra row
and column of empty spaces on the four borders. That way, when iterating through the
"real" cells of the matrix, it is always safe to access the neighbours by the calculated
indexes.

To search for the first recurring state, I chose to store the string representations
of the matrices in a set. That was also useful for printing the matrices to the console.

For the "biodiversity" calculation, I created the matrix of 2-powers by hand, using the
<< operator.

## Part 2

With an infinite recursive space, there was no need to provide a "border" for the matrix
any more. 

In this part I identified cells with a `(level, x, y)` triplet. The hairiest part was
enumerating the neighbours of a cell. There was no trick to it, just a long `if .. elif .. `
chain for the possible cases.

The simulation step also changed from part 1. Rather than going through every cell in the
infinite space, I realized that only neighbours of bug cells have the possibility to change.
So in a first round, I _mark_ the neighbours of bug cells. Then for every marked cell I count
the number of neighbour bugs (there is at least one), and evaluate the rule to determine
if this cell is going to be a bug or an empty space. I evaluate the rules into a temporary space
(a dictionary with the cell as the key, and the new value as the value), and after every marked
cell has been evaluated, I update the original space.

Python's `defaultdict` type has been immensely helpful here. I only store in memory those levels
that has been at least once touched (read or written). With `defaultdict` I don't have to worry in
my code whether the level I'm accessing has already been created or not, because if it hasn't, then
`defaultdict` creates a new empty level for me.