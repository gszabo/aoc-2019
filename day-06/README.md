# Day 6

https://adventofcode.com/2019/day/6

Built two directed graphs from the input:
1. From orbited planet to orbiting planets (one to many)
2. From orbiting planet to its orbited planet (one to one)

Part 1 is essentially counting and summing the distances from each node to _COM_ (Center Of Mass).
For this I used a breadth-first-search (BFS) algorithm. `Graph 1` is the useful one here.

Part 2 is about finding the closest common "ancestor" in the graph of SAN and YOU, and counting
the steps from both points to reach that closest common ancestor. `Graph 2` is the useful one here.