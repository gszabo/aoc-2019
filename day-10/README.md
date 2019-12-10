# Day 10

https://adventofcode.com/2019/day/10

The key class in my solution is `DirectionVector`. It represents a direction on the plane. 
It's a value object with the semantics that two vectors that point in the same direction
should be equal. To achieve this, it internally divides it's `x` and `y` coordinates
with their _greatest common divisor_. This is sufficient, because the coordinates are
integer numbers.

You can create a `DirectionVector` by invoking the constructor, or you could 
**subtract two points** from each other.

With that weapon in the pocket, part 1 is just calculating every direction vector
from every asteroid, putting them in a set, and checking the size of the set. 
Since `DirectionVector` is a value object, if two asteroids are on the same line
from the view point, only one direction is going to be counted. 

My solution for part 2:
1. group asteroids by direction (looked from the laser station). 
In Python the result of this is a `dict`. The keys are the direction vectors, 
the values are lists of points that fall in that direction.
2. sort every group by the distance from the laser station
3. sort the directions by the rotation angle from the upward direction.
Calculating the rotation angle involves using the inverse tangent function.
4. Iterate through the directions and for each direction
vaporize (ie. remove and collect in another list) the first asteroid in that
direction (if there's any asteroid left in that direction).
5. Repeat step 4 until every asteroid is vaporized. 

