# Day 22

https://adventofcode.com/2019/day/22

For part 1, at first I implemented the three possible steps with lists of numbers.
It gave the correct answer, but was waaaay too slow for part 2, so I had to come
up with a different approach.

## Part 1

From here on, let `N` denote the number of cards in the deck.

Every card shuffling step (even those that are outside of the problem) can be thought of 
as a (mathematical) function: for every `n in [0, 1, ..., N-1]` `f(n)` tells us where the
card at index `n` goes after the shuffling step.

The three possible shuffling steps can be expressed as these functions:
```
deal_into_new_stack(n) = N - 1 - n = -n - 1 (mod N)
deal_with_increment(n) = n * inc (mod N) [for a given inc increment]
cut(n) = n - C (mod N) [for a given C cut size (C can be negative)]
```

_Note_: The creator of the problem guarantees that the increments and `N`s are chosen
so that no two cards go to the same spot, ie. `if x != y then f(x) != f(y)`. 

Doing multiple shuffling steps (eg. dealing into new stack, then cutting 3, etc) can also be
represented as a function. That function is the _composition_ of the functions of the
individual steps. The input is a list of shuffling steps, so the whole input can be
substituted with only one function: the composition of its steps. That one function
places every card just like bunch of steps in the input would.

Each type of function is linear (adding a modulo N to end does not affect linearity). 
Each one of them can be written as
```
f(n) = a1 * n + a0 (mod N)
```
The compositions of linear functions are also linear functions. For example if we have two linear
functions `f` and `g`:
```
f(n) = a1 * n + a0 (mod N)
g(n) = b1 * n + b0 (mod N)
```
then the composition `f∘g` or `g|f` (unix pipe like notation) or simply `f(g(n))`, where `g` is applied 
first and then `f` to the result of `g` can be expressed as:
```
f(g(n)) = a1 * (b1 * n + b0) + a0 = a1 * b1 * n + a1 * b0 + a0 (mod N)
                                    -------       ------------
                                    linear        constant part
                                    coefficient
```

With that in mind, the solution to part 1 is:
1. Determine the function `f` that is the composition of the functions of each
shuffling step in the input. 
    - We know that each step and `f` is a linear function.
    - We just need to combine the first two steps, then the result with the third step,
      then the result with the forth step, etc until the last step in the input.
    - Every combination step requires a fixed amount of calculation (two multiplications and one addition).
    - This all means calculating `f` can be done in linear time with respect to the length of the input.
2. Calculate the `f(2019)` expression.

_Note_: In the code I called the type to represent these linear functions a `Polynom`, because they are
first degree polynoms. The `Polynom` type has a `pipe` method for composition and an `evaluate` method
to calculate the function for a given index.

## Part 2

[TBD]

Part 2 asks the question what card lands on index 2020. 

Since every card goes somewhere and no two cards go to the same place, every shuffle function
is a _bijection_. That means it can be inverted. 