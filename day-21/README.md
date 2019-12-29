# Day 21

https://adventofcode.com/2019/day/21

The code itself only provides ASCII input and output for the Intcode program. The solutions
were manual tweaking of the spring scripts.

## Part 1

I started with just a simple WALK instruction, and worked my way through one by one on each
scenario the springdroid could not handle. I stumbled upon these four scenarios:

1. 
    ```
    .................
    .................
    @................
    #####.###########
    ```
2. 
    ```
    .................
    .................
    @................
    #####..#.########
    ```
3. 
    ```
    .................
    .................
    @................
    #####...#########
    ```
4. 
    ```
    .................
    .................
    @................
    #####.#..########
    ```

The following logical expression jumped over all of these:
```
J = D * (!A + !B + !C)
```

`*` is the logical `AND`, `+` is the logical `OR` and `!` is to logical `NOT` operator.

`D * (...)` is there to only jump if the robot landed on ground, not on a hole. 
`(!A + !B + !C)` means jump if there is a hole in 1, 2 or 3 steps ahead.

Implementing that in springscript:
```
Input instructions:
> NOT A J
> NOT B T
> OR T J
> NOT C T
> OR T J
> AND D J
> WALK

Walking...

19354392
```

## Part 2

Using the springscript from part 1, and changing `WALK` to `RUN`, the following scenario beat the droid:

```
.................
.................
@................
#####.#.#..######
```

The droid stepped into the hole after jumping to the first "lonely" ground:
```
.................
.................
......@..........
#####.#.#..######
```

The jump was triggered by the `!C` part of the expression, even though the droid should have
waited until the last step before the hole to jump and land on the second "lonely" ground,
and jump further from there.

Using the new sensors, I modified the `!C` part to only trigger if the droid can jump further from
the landing ground (8 steps away, using the sensor `H`) or it can step further (5 steps away, using
sensor `E`). So the `!C` part changes to `!C * (E + H)`. Given the instruction set and only one temp
register, I felt it is hard to do the `!C * (...)` part, so I used [De Morgan's law](https://en.wikipedia.org/wiki/De_Morgan%27s_laws)
to change the expression into `!(C + !(E+H))`. Thus the final expression looks like:
```
J = D * (!A + !B + !(C + !(E + H)))
```

In springscript:
```
Input instructions:
> NOT A J
> NOT B T
> OR T J
> NOT E T  # This two lines are essentially
> NOT T T  # T = E, or SET E T, that is not part of the instruction set
> OR H T
> NOT T T
> OR C T
> NOT T T
> OR T J
> AND D J
> RUN

Running...

1139528802
```

This is 11 lines of springscript, that fits into the droid's memory, and was able 
to handle all of the holes of my input.