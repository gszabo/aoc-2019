# Day 22

https://adventofcode.com/2019/day/22

For part 1, at first I implemented the three possible steps with lists of
numbers. It gave the correct answer, but was waaaay too slow for part 2, so I 
had to come up with a different approach.

## Part 1

From here on, let `N` denote the number of cards in the deck.

Every card shuffling step (even those that are outside of the problem) can be
thought of as a (mathematical) function: for every `n in [0, 1, ..., N-1]`
`f(n)` tells us where the card at index `n` goes after the shuffling step.

The three possible shuffling steps can be expressed as these functions:
```
deal_into_new_stack(n) = N - 1 - n = -n - 1 (mod N)
deal_with_increment(n) = n * inc (mod N) [for a given inc increment]
cut(n) = n - C (mod N) [for a given C cut size (C can be negative)]
```

_Note_: The creator of the problem guarantees that the increments and `N`s are 
chosen so that no two cards go to the same spot,
ie. `if x != y then f(x) != f(y)`. 

Doing multiple shuffling steps (eg. dealing into new stack, then cutting 3, etc)
can also be represented as a function. That function is the _composition_ of the
functions of the individual steps. The input is a list of shuffling steps, so
the whole input can be substituted with only one function: the composition of
its steps. That one function places every card just like the bunch of steps in
the input would.

Each type of function is linear (adding a modulo N to end does not affect
linearity). Each one of them can be written as
```
f(n) = a1 * n + a0 (mod N) ; a0 and a1 are integers
```
The compositions of linear functions are also linear functions. For example if
we have two linear functions `f` and `g`:
```
f(n) = a1 * n + a0 (mod N)
g(n) = b1 * n + b0 (mod N)
```
then the composition `f∘g` or `g|f` (unix pipe like notation) or simply 
`f(g(n))`, where `g` is applied first and then `f` to the result of `g` can 
be expressed as:
```
f(g(n)) = a1 * (b1 * n + b0) + a0 = a1 * b1 * n + a1 * b0 + a0 (mod N)
                                    -------       ------------
                                    linear        constant part
                                    coefficient
```

_Note_: `a1` and `a0` in a function `f(n) = a1 * n + a0 (mod N)` can be replaced
with their remainder modulo `N`. Eg. if `N=10` and `f(n) = 13 * n + 27 (mod 10)`
, then `f` can be rewritten as `f(n) = 3 * n + 7 (mod 10)`. So when computing
the composition of two functions, the linear coefficient and the constant may
end up being larger than `N`, but they can be reduced into the `0, 1, ..., N-1`
range.

With that in mind, the solution to part 1 is:
1. Determine the function `F` that is the composition of the functions of each
shuffling step in the input. 
    - We know that each step and `F` is a linear function.
    - We just need to combine the first two steps, then the result with the
      third step, then the result with the forth step, etc until the last step
      in the input.
    - Every combination step requires a fixed amount of calculation
      (two multiplications and one addition).
    - This all means calculating `F` can be done in linear time with respect to
      the length of the input.
2. Calculate the `F(2019)` expression.

_Note_: In the code I called the type to represent these linear functions a
`Polynom`, because they are first degree polynoms. The `Polynom` type has a
`pipe` method for composition and an `evaluate` method to calculate the function
for a given index.

## Part 2

Part 2 asks the question what card lands on index 2020. This question is the
_inverse_ of the question in part 1. Instead of evaluating the shuffling
function at a given index like `f(2020)`, we need to solve the equation
```
2020 = f(n)
```

### Inverting

The nature of card shuffling ensures that this question can be answered. After
a shuffling step every index is occupied by a card, and no two cards go to the
same index. So it is _exactly_ one card that lands on any index, meaning there
is only one answer to the question.

In mathematical terms, any shuffling function is a _bijection_, so it can be
inverted. I'll denote the inverse of `f` like `f^-1`. The answer is
`f^-1(2020)`.

How would we calculate the inverse of a shuffling function? Let `T` be the
target index in the question (here 2020).
```
T = f(n)
T = a1 * n + a0 (mod N)
T - a0 = a1 * n (mod N)
q * (T - a0) = n (mod N)
```
where `q` is a number from the `1, 2, ..., N-1` range that satisfies
```
q * a1 = 1 (mod N)
```

Such `q` exists if `a1 != 0` (constant functions cannot be inverted, but in our
card shuffling case, they are not valid functions either), and `a1` and `N` are
relative primes. Since `N` is a prime number in the problem, every `a1` in the
range of `1, 2, ..., N-1` are relative primes to it. 

So the inverse of `f(n) = a1 * n + a0 (mod N)` can be expressed as
```
f^-1(n) = q * (n - a0) = q * n - q * a0 (mod N)
```

However, calculating `q` can be tricky. We might iterate over the
`1, 2, ..., N-1` range, calculate `q * a1 (mod N)` and stop if we found 1. But
`N` is a _huge_ number in part 2, so this method is too slow. There are two
shortcuts:

1. If `a1 = 1` or `a1 = N - 1`, then `q = a1`. This is useful to invert the
   `deal into new stack` step.
2. It is enough to iterate over the `1, 2, ..., a1` range, and usually
   that is much smaller than the `1, 2, ..., N-1` range. To use this approach,
   find the `i` in the range of `1, 2, ..., a1` so that `i * N + 1` is
   divisible by `a1`. Since `a1` and `N` are relative primes, each `i * N + 1`
   value has a different remainder modulo `a1`, meaning one of them has zero
   remainder, ie. it is divisible by `a1`. In this case `q = (i * N + 1) / a1`.

In order to really exploit these shortcuts, we have to do more. After reading
in the input and composing the steps together, I end up with this function:
```
F(n) = 36917093953130 * n + 115619106397456 (mod 119315717514047)
```

As you can see, `a1` here is still _way_ too large to calculate `q`. However,
the `a1`s found in my input are two-digit numbers. It's easier to calculate
the inverse of the individual steps, and combine the inverses to get the inverse
of the input! We just have to combine the inverses in reverse order:
```
(f1 | f2 | f3 | f4)^-1 (n) = (f4^-1 | f3^-1 | f2^-1 | f1^-1)(n)
```

Now we can quickly have `F^-1` by calculating the inverse of each step in the
input and composing them in reverse order. But we are not done yet!

### Shuffling tons of times

The problem wants us to shuffle 101741582076661 times in a row. So the shuffling
functions is
```
G(n) = (F | F | F | F | ... | F)(n)
        -----------------------
         101741582076661 times
```
where `F` still denotes the composition of input steps. The answer we are
looking for is `G^-1(2020)`. `G^-1` can be written the same way:
```
G^-1(n) = (F^-1 | F^-1 | F^-1 | F^-1 | ... | F^-1)(n)
           --------------------------------------
                    101741582076661 times
```

Composing `F^-1` 101741582076661 times, one by one is way too slow, again.
Luckily, function composition is associative:
```
((f | g) | h)(n) = (f | (g | h))(n)
```
because both sides equal `h(g(f(n)))`. Having that, we can group chains of
`F^-1`s, compose the groups and work our way up from there:
```
I = F^-1

I_thousand = (I | I | ... | I | I)
              -------------------
                   1000 times

I_million = (I_thousand | I_thousand | ... | I_thousand)
             ------------------------------------------
                            1000 times

I_billion = 1000 times I_million // a billion

I_trillion = 1000 times I_billion // a trillion
```

Remember, each `I_...` up there is just a function with `a1` and `a0`
parameters. Composing 1000 functions at a time is not that time-consuming.
Of course we could go up 10 times at a time instead of 1000. There is a `times`
helper function on the `Polynom` type, that pipes the polynom the given times
into itself.

The full shuffle count is 101741582076661. With delimiters, it's
`101_741_582_076_661`. To arrive at `G^-1`:
```
G^-1 = (101 times I_trillion | 
        741 times I_billion |
        582 times I million |
        76 times I_thousand |
        661 times I)
```
Doing this way, every iteration count is less than 1000, so it's manageable for
the computer. So we can quickly have `G^-1`, and evaluate the resulting linear
function at 2020, ie. calculate `G^-1(2020)`.