# Day 20

https://adventofcode.com/2019/day/20

## Parsing

The trickiest part for me was parsing the input, identifying portals
and deciding whether the portal is on the inner or the outer edge of the donut.

To make parsing easier, after I read in the input, I add a 1-width "border" of empty 
space (full width empty line to beginning and end of the input, and one space to the 
beginning and end of each line) so that looking ahead of back from a portal never 
causes index out of range errors.

I read the input line by line (top to bottom), from left to right. If the current
character is an uppercase letter, then I try to find the second character of the portal.
The names of the portals are read from left-to-right or top-to-bottom, so I look for the
second character one step right (horizontal portal) and one step down (vertical portal).
This means that I'm only going to find another character if I'm currently on the first 
character of the portal. This is OK.

Once it's established whether the current portal is horizontal or vertical, I look for
the passage tile next to the portal. This can be either two steps forward (down for vertical,
right for horizontal) or one step backward (up for vertical, left for horizontal), 
since we are on the first character of a portal.

After that we still need to find whether the current portal is an outer or an inner one.
For that I take a horizontal or vertical (depending on the portal type) cross section of the
input: either the characters in the current line, or in the current column. Then, stepping
through character I look for _edges_: eg. ` .`, `. `, `.X`, `X.`, etc changes. One cross
section can have two or four edges. Two if the cross section does not go through the middle hole,
or four if it does. The first and last edges found are outer edges, the middle two (if they exist)
are inner edges. From that we can find which edge the passage tile next to the portal belongs to.

I placed sanity check assertions at the end of the portal and edge parsing code.

For the pathfinding algorithm it's useful to provide a mapping from one side of the portal to
the other side.

## Pathfinding

The BFS algorithm was a sufficient tool to find the shortest path.
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