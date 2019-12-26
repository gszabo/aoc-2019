# Day 15

https://adventofcode.com/2019/day/15

I created a Console based UI (with the help of the [curses library](https://docs.python.org/3/howto/curses.html))
and manually explored the area. Then, I saved the collected walls, corridors and oxygen start position
to a [file](./output.dat) (it's a binary file, serialized with Python's `pickle` library).

After that, part one was a [BFS](https://en.wikipedia.org/wiki/Breadth-first_search) from the robot's starting position
to the oxygen tank, to calculate the shortest distance.

Part two was very similar. In that case the starting point of the BFS was the oxygen tank, and the answer
is the largest distance found in the area. This is because oxygen spreads in each minute like a new layer
in the BFS algorithm.