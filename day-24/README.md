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