# Day 3

https://adventofcode.com/2019/day/3

I used a Python 3 script, again. I created types for `Point` and `Segment` (given with its start and end point)
with `@dataclass` annotations (learned something new). I parsed each given input line into a `List[Segment]`, representing
the _path_ of each wire.

For part 1, searching for intersections, I iterated through the two lists in a nested loop and checked if each segment
intersects any segment in the other list.

For part 2, I needed to calculate the wire steps for each intersection. As I iterated through the two lists, I kept 
two variables that were increased with the length of each segment.