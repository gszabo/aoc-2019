# Day 12

https://adventofcode.com/2019/day/12

For part 1, I created `Position`, `Velocity` and `Moon` classes, implemented the steps
of a simulation step, and calculated the energy formula after 1000 steps.

Part 2 was hard and misleading for me. At first I had no idea. After discussing the problem
with a colleague (superficially), he suggested that this is a cycle detection problem in
a graph. So I looked up and implemented the Tortoise and the Hare algorithm. I haven't heard
about that algorithm before, so thanks to Arnold Farkas for teaching me that. Here are two
good sources:
- https://en.wikipedia.org/wiki/Cycle_detection#Floyd's_Tortoise_and_Hare
- https://stackoverflow.com/questions/2936213/explain-how-finding-cycle-start-node-in-cycle-linked-list-work

However, that algorithm did not finish in time on my machine, and that was an indicator that I need
to find a different approach. At the end, I reached for help on the [solution megathread](https://www.reddit.com/r/adventofcode/comments/e9j0ve/2019_day_12_solutions/fakyn6l).

The basic idea is this:
1. Movement on the x-axis is independent from y and z axes, and vica versa. So I need to find
cycles in the movement of the system along the x, y and z axes independently. The least common
multiple of the three cycle lengths is going to be the cycle length of the whole system movement.
2. We assume the system is going back to its initial state (start position and zero velocity).
I don't think this is generally true, but it works on the example input and on my input as well.