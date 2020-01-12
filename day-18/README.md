# Day 18

https://adventofcode.com/2019/day/18

This problem eluded me for a while. At first I had a backtrack like recursive algorithm:
1. make current position the entrance
2. check what keys are reachable from the current position 
(BFS along the corridors, taking into account doors and already obtained keys)
3. if there is only one key reachable
    1. go there and grab the key
    2. go to step 2
4. if there are multiple keys reachable
    1. for each key
        1. go there and grab the key
        2. go to step 2 and calculate the steps taken to pick up all keys
    2. choose the best (minimum steps) option 
    3. go to step 2

For the small examples this worked fine, but it did not finish
even for the example with 136 steps. It has 16 keys, and according to
my debugging, the algorithm was spending a lot of time on the 14th-15th level
of recursion. 

After digging around in my memory and on Wikipedia about shortest past algorithms,
somehow I stumbled upon the [dynamic programming](https://en.wikipedia.org/wiki/Dynamic_programming) approach. 
I sensed it would fit because it seemed to me that my algorithm was calculating the same sub problem
over and over again. To be more precise, this problem has
- optimal substructure: 
    
    The optimal solution to the problem can be calculated by the optimal solutions of the sub-problems.
    Here the sub-problems are the shortest key pickup order from each reachable key.
    One optimal key pickup order is also optimal if we only consider the last *n* keys. So the solution
    to the original problem is the one from the sub-problems whose path length and the distance from the
    current position to it's starting key added together is minimal.
- overlapping sub-problems:
    
    This means that the number of different sub-problems are not very large, so the recursive algorithm
    solves the same sub-problems over and over. This is true for this algorithm. 

That is why dynamic programming's trick can help here. The trick is to store / cache the results of the
sub-problems in a table and look up the result during the recursive algorithm, rather than to calculate
it over and over again. This trick sped up my code, so it produced a result in a couple of seconds.

In Python I implemented the caching with a `@memoize` decorator. For that I needed the recursive
function to have `hashable` arguments, so that the arguments could be a key in a dictionary. This 
was achieved by using a `frozenset` instance instead of a `set`.

Part 2 is fundamentally the same problem as part 1. The difference is that part 1 has only one current _position_
variable, and part 2 has four position variables, one for each robot, that start in their corresponding 
entrances. This increases the number of subproblems in one step of the recursive function, because
you need to check 4 robots for reachable keys and consider moving each to any of the reachable keys. On the
other hand, the reachable space for any robot is 1/4th of the size from part 1. In any case, dynamic programmings
caching trick helps here, too. Part 1 and part 2 together run in about 7.5 seconds on my machine.

