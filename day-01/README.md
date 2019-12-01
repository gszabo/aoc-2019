# Day 1

https://adventofcode.com/2019/day/1

I chose to solve this with a spreadsheet. In part 1 I applied the given formula applied to every item
and summed together. In part 2 I changed the given formula to include a `MAX(formula, 0)` part and
recursively applied to the output of the previous formula until the value reached 0. It was all done
by hand, and it was feasible since it only required about 10 applications for each input item.

