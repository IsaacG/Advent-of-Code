# Day 01

## Issue One
I decided it would be good to use the faster desktop this year.
The exercise starts and I instantly realize my desktop doesn't have cookies set up to download the data.
Close that all down and switch to the server!

## Issue Two
Instead of adding `total += number[0] * 10 + number[-1]` I added `total += number[0] + number[-1]`.
Thankfully I fixed that pretty quickly to solve part 1.

## Issue Three

Those pesky overlapping values!
To handle the overlapping, it occurs to me that I can reverse the string and try scan-and-replace words with digits in both directions.
`eightwo` would become `8wo` when expanded from the left and `eigh2` when expanded from the right.
I store the line in a temp variable, expand from left, copy the temp and expand from the right.
Then I can add up the first from the left and last from the right.

```python
original = line
for word, digit ...: ... line = line.replace(word, digit)
line2 = line[::1]
for word, digit ...: ... line2 = line2.replace(word[::-1], digit)
total += first_digit(line) * 10 + first_digit(line2)
```

Alas, too many variables and too easy to confuse them. `line2 = line[::-1]` is using the mutated line and not `original`.
I only discovered this after abandoning ship and writing my new solution.

# Day 02

Not much to see here.

# Day 03

## Approach

The parsing and mapping for this was a bit tricky.
I used a regex to find all the numbers on each line then used the `match.span()` to find the start and end position of each number.
This allowed me to find each coordinate with a digit and map those coordinates to the coordinate where each number starts.
Having a unique coordinate for each number makes it easy to identify unique adjacent numbers.

This produced three maps:
* start positions of numbers to the numeric values,
* digit coordinate to the number's start coordinate, and
* engine coordinate to symbol.

Using these three maps made the rest of the exercise relatively simple, once I corrected my off-by-one error.

## Issue One
I used regex to find number start and end position of each number, then used `x in range(start, end + 1)` to map each digit to the number's start coordinate.
However, the `re.match.span()` already adds +1 to the end so I was extending digits too far by one.
This managed to work with the example input but not my real input.
That cost me at least 5 minutes.

# Day 04

Relatively straight forward day.
Part two took a bit of squinting to understand what was being asked but the example helped.

# Day 05

That was a ride!
I managed to rank 416/2180.
At first I couldn't even parse right, as I used `split("\n\n\n)` which had an extra newline!
I tried a few approaches until I got a working algorithm for part 2.
I then had a bug where I assumed when an input range exceeded the translation range, the excess would be copied over directly without change; what needed to happen was to preserve that excess for processing by other translation rules.
Once that was fixed, I was failing to pass tests, because I changed variables around but failed to update the `return mix(...)` line.
I spent a bunch of time going over the example, line by line, until I realized that error.

# Day 06

Pretty simple day.

1. I initially wrote `time - i * i` to calculate distance.
   I was very confused when my ways to win was 0.
   Converting that to `(time - i) * i` helped.
2. My framework assumes all parts use the same parser.
   Having to parse things differently messes with that base assumption.
   I was able to work around that with `int("".join(str(i) for i in numbers)` but that makes me sad.

## Optimization

The brute force solution:

```python
return math.prod(
    sum(
        (time - i) * i > distance
        for i in range(time + 1)
    )
    for time, distance in zip(times, distances)
)
```

Note the inequality:

```
(time - i) * i > distance
-1 * x * x + time * x - distance > 0
# Quadratic equation!
x = (-b +/- sqrt(b**2 - 4 * a * c)) / (2 * a)
x = (-time +/- math.sqrt(time**2 - 4 * distance)) / (-2)
x = (time +/- math.sqrt(time**2 - 4 * distance)) / 2
```

The inequality is `> 0` which means `x` sets the thresholds of the interval, but it is an open interval, i.e. `x` itself is not included.
I solve this by solving for the x values and taking the "inner" integer values (`ceil(x1), floor(x2)`).
If those inner values match `x` exactly, they need to be shifted inwards by one.

# Day 07

I'm very glad I wrote a Python sort function in the past!
Figuring that out on the fly would have been challenging.

1. First mistake. For a short while I was passing the part one example but getting the wrong result for the real input.
   When I ordered hands of same rank, I was using `10 ** position` for adding up the card orders.
   However, there are more than 10 cards and that makes a difference!
   My logic was putting `2A` (value 10 + 13) ahead of `32` (20 + 1).
2. I was worried about handling ties and that my result might be wrong due to a draw.
   I added code to check for a draw (duplicate hands).
   However, those don't appear to exist in my input so I later removed it.

# Day 08

1. I wasted some time since I forgot to reset steps=0 inside my `foreach start` loop.
2. The instructions in part 2 has example nodes with digits in the name, which threw me for a loop.
   For part 1 I assumed the node names were all alpha.
   And they are!
   The example is just odd.

## Part 2 data assumptions

The part two solution using LCM assumes that:
* `first_terminal_node == second_terminal_node`
* `distance(start_location, first_terminal_node) == distance(first_terminal_node, second_terminal_node)`
* `distance(start_location, first_terminal_node) == n * length(instruction)``

I added `pre_run()` logic to validate these assumptions.

# Day 09

I instantly recognized this as requiring solving a polynomial and describing the first differences approach.
However, I am not sufficiently familiar with numpy or other math libraries to leverage those.
I was also battling internet issues this night.

This code could be made more efficient (by roughly 10%) by reducing the recursion limit by one.

```python
# Sticking true to the AoC described algorithm, I used this.
if all(i == 0 for i in diffs):
    prior = following = 0
# A more efficient approach is as follows.
if len(set(diffs)) == 1:
    prior = following = diffs[0]
```

# Day 10

Started 60 minutes late.

# Day 12

I solved this 5 days later on my 3rd attempt.
I wrote a bunch of approaches and then deleted them.
See git history.

# Day 14

Delayed start.

I can deduplicate the 4-directions code by using the north code in a loop by rotating the grid 90 degrees between rotations.
However, that seems to slow things down by 50%.

# Day 16

My part 1 solution was decently fast to pass the example.
However, it took me the longest time to figure out why it failed the real input.
I seeded my data with a beam at `(0, 0) RIGHT` then loop where I examine the next time.
This was fine in the example with `(0, 0)` is empty but the real data has a reflector at `(0, 0)` which I skipped.

The massive logic block could be changed to a dictionary lookup but that bumps runtime from 8s to 11s.

```python
# Out direction(s) based on in direction.
DIR_IN_TO_OUT = {
    "#":  {direction: {} for direction in aoc.FOUR_DIRECTIONS},
    ".":  {direction: {direction} for direction in aoc.FOUR_DIRECTIONS},
    "|":  {UP: {UP}, DOWN: {DOWN}, RIGHT: {UP, DOWN}, LEFT: {UP, DOWN}},
    "-":  {RIGHT: {RIGHT}, LEFT: {LEFT}, UP: {RIGHT, LEFT}, DOWN: {RIGHT, LEFT}},
    "/":  {RIGHT: {UP}, LEFT: {DOWN}, UP: {RIGHT}, DOWN: {LEFT}},
    "\\": {RIGHT: {DOWN}, LEFT: {UP}, UP: {LEFT}, DOWN: {RIGHT}},
}
```

It might be possible to speed things up by memoizing energized cells starting from a specific element but I had difficulties making that work.

# Day 17

* `PriorityQueue` and `complex` don't mix so I had to scramble slightly to rewrite everything from `complex` to `tuple[int, int]`.
* I initially used A\* with the Manhatten distance as the heuristic but it seems to not actually help.

# Day 18

For part 1, I used a flood fill for the interior and added up the perimeter as I explored it.

## Part 2

I realized pretty quickly that I'd need a scanline here.
I thought I could order by start/end y-coordinates and collect active ranges, but I confused myself then decided not to bother.
Instead, I went the slower route of computing all the y-changes and, for each y-value, I computed which lines are relevant.
The line count was small enough that this was fine.
I got most the way to the end but got stuck for a good long while trying to figure out how to properly account for the perimeter.

# Day 19

I had a silly mistake in part two that took me a good half hour or so to figure out.

Compare,

```python
# Bad code
if target == "A":
    accepted_contraints.append(constraints + [(attr, op, val)])
elif target == "R":
    rejected_contraints.append(constraints + [(attr, op, val)])
else:
    recurse(constraints + [(attr, op, val)], rules[target])
    recurse(constraints + [reverse(attr, op, val)], tests[1:])

# Working code
if target == "A":
    accepted_contraints.append(constraints + [(attr, op, val)])
elif target == "R":
    rejected_contraints.append(constraints + [(attr, op, val)])
else:
    recurse(constraints + [(attr, op, val)], rules[target])
recurse(constraints + [reverse(attr, op, val)], tests[1:])
```

# Day 20

## Part 2

This part required manual analysis and solving.
Here is a snippet of my input.

```
&pg -> gf
&qs -> gf
&sp -> gf
&sv -> gf
&gf -> rx
```

`rx` needs to receive a LOW from `gf`.
`gf` will send a LOW on a cycle when it gets HIGH from all its four inputs, `pg, qa, sp, sv`.
When I run for a whole lot of cycles, I noticed that those four modules all output a HIGH cyclically, that is, every `n_i * k` cycles for k in `1..(infinite)` and i in `pg, qa, sp, sv`.
If those `n_i` are all co-primes, then they will output HIGH on `product(n_pg, n_qs, n_sp, n_sv)`.
I verified they are co-prime and I submitted the product for my solution.
