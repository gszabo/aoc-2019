# Day 22

https://adventofcode.com/2019/day/22

For part 1, at first I implemented the three possible steps with lists of numbers.
It gave the correct answer, but was waaaay too slow for part 2, so I had to come
up with a different approach.

From here on, let `N` denote the number of cards in the deck.

Every card shuffling step (even those that are outside of the problem) can be thought of 
as a (mathematical) function: for every `n in [0, 1, ..., N-1]` `f(n)` tells us where the
card at index `n` goes after the shuffling step. 

Since at the beginning every card is on the same index as it's value, part 1 can be solved
by calculating the first function of the input with 2019 as parameter, then feed the result
into the second function of the input, then feed the result into the third function of the
input, etc... If the input has `K` steps and `f_i` represents the function of the i. step, 
part one is calculating
```
f_K(...f_3(f_2(f_1(2019)))...)
```
or in other words
```
(f_1 | f_2 | f_3 | ... | f_K)(2019)
```
(pipe represents passing the result of one function to the next, like a unix pipe).

Combining or piping functions also result in functions, so it's possible to first pipe
the functions together, and calculate the resulting function with the desired argument.
By definition the two approaches yield the same result.

```
deal_into_new_stack(n) = N - 1 - n = -n - 1 (mod N)
deal_with_increment(inc)(n) = n * inc (mod N)
cut(C)(n) = n - C (mod N)
```

First order polynoms.

Since every card goes somewhere and no two cards go to the same place, every shuffle function
is a _bijection_. That means it can be inverted. 