# Day 20

https://adventofcode.com/2019/day/20

The trickiest part for me was parsing the input, identifying portals
and deciding whether the portal is on the inner or the outer edge of the donut.
To make parsing easier, I add a 1-width "border" of empty space to the input,
so that looking ahead of back from a portal never causes index out of range errors.

Other than that, the BFS algorithm was a sufficient tool to find the shortest path.
It is sufficient because every step ("edge") in the graph is uniform 1 weight.
When listing the neighbours of the current position, you need to take portals into
account, so you don't just use the passages to step. For part 1 that is all to it.
I also implemented the pathfinding also with Dijkstra's algorithm, because at first
I had a bug in the BFS implementation, got confused and thought BFS wasn't sufficient.
I left both implementations in the code so it can be seen that they produce the same
result.

For part 2 I extended the _position space_ with a third coordinate: the level. So the
pathfinding algorithm needs to find the shortest path from `('AA', 0)` to `('ZZ', 0)`.
BFS, again, is sufficient here. When listing the neighbours through portals, you need
to check if the portal can be used on the current level, and set the level of the
neighbour cell accordingly (`current - 1` for outer portals, `current + 1` for inner portals).
This algorithm cannot detect if there isn't any path from start to finish, because the 
inner portals can always take you to a more inner level, so the explorable space is infinite.
But if a path exists (and the problem description states that it exists), than it can find
the shortest one.