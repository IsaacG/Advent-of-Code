# Ranking

```
      --------Part 1--------   --------Part 2--------   --------Delta---------
Day       Time   Rank  Score       Time   Rank  Score       Time   Rank  Score
 25   02:42:34   2936      0   02:42:38   2459      0   00:00:04   -477      0
 24   00:25:28    319      0   02:19:06   1004      0   01:53:38    685      0
 23   01:19:01   2938      0   02:25:43   1748      0   01:06:42  -1190      0
 22   00:42:40    794      0   01:00:21    793      0   00:17:41     -1      0
 21   00:04:58    118      0   04:02:11   1936      0   03:57:13   1818      0
 20   00:30:18    247      0   01:28:04    953      0   00:57:46    706      0
 19   00:25:06   1169      0   01:19:51   1477      0   00:54:45    308      0
 18   00:05:29     20     81   01:45:17   2210      0   01:39:48   2190     81
 17   00:24:53    490      0   00:33:25    500      0   00:08:32     10      0
 16   00:41:23   2495      0   00:47:44   2137      0   00:06:21   -358      0
 15   00:24:49   6147      0   00:47:38   4075      0   00:22:49  -2072      0
 14   01:28:33   8040      0   01:49:10   4484      0   00:20:37  -3556      0
 13   00:15:12    533      0   00:44:15   1846      0   00:29:03   1313      0
 12       >24h  38449      0       >24h  25405      0       >24h -13044      0
 11   13:00:56  30912      0   14:55:17  31175      0   01:54:21    263      0
 10   01:24:19   5937      0   02:36:29   3515      0   01:12:10  -2422      0
  9   00:11:54   1705      0   00:15:56   1688      0   00:04:02    -17      0
  8   00:05:33    569      0   00:15:22    341      0   00:09:49   -228      0
  7   00:21:36   1160      0   00:29:15    776      0   00:07:39   -384      0
  6   00:06:17    955      0   00:08:02    606      0   00:01:45   -349      0
  5   00:12:41    416      0   01:15:01   2180      0   01:02:20   1764      0
  4   00:06:23   1299      0   00:11:05    494      0   00:04:42   -805      0
  3   00:18:24   1234      0   00:21:39    641      0   00:03:15   -593      0
  2   00:07:28    603      0   00:11:04    693      0   00:03:36     90      0
  1   00:03:08    769      0   00:31:34   3449      0   00:28:26   2680      0
```

* I managed to get day 18 part 1 in 20th place! My best ranking to date.
* I got under 500 seven times and under 1000 21 times -- almost half the time!

# Slow Days

```
2023/12 Part 2: PASS in   1.265  s!
2023/13 Part 2: PASS in   1.234  s!
2023/14 Part 2: PASS in   4.497  s!
2023/16 Part 2: PASS in   7.736  s!
2023/17 Part 1: PASS in   4.493  s!
2023/17 Part 2: PASS in  16.562  s!
2023/21 Part 2: PASS in   9.181  s!
2023/23 Part 1: PASS in   7.117  s!
2023/23 Part 2: PASS in  20.766  s!
2023/24 Part 2: PASS in  49.109  s!
2023/25 Part 1: PASS in  14.001  s!
```

* Day 14: Tilt the board and roll rocks around a lot of times.
* Day 16: Map a light beam across a board of reflectors, for all possible starts.
* Day 17: Find the route with the least heat loss with cart movement requirements.
  Uses Djisktra. A* doesn't help here.
* Day 21: Find the number of locations reachable after N steps. Lots and lots of steps.
* Day 23: Find the max length path. Not much room for optimization that I know of. Maybe networkx?
* Day 24: Hit astroids with one rock. Uses z3. No idea how to do better.
* Day 25: Find the min cut set of a graph.
  Can be done using networkx. Hard problem without a greats solution.

```
$ time ./runner.py --check --all-days
0m51.371s  # ProDesk
2m10.179s  # NUC
```

# Day 01

The exercise: scan lines to find the first and last number on each line.
Part two: expand the words "one", "two", ... "nine" and repeat the above.
Catch: words like "twone" and "eightwo" need to be expanded to two numbers.

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

## Solution

I solved this by iterating over each line and collecting numbers in a new list.
Then I pull the first and last from the new list.
For each line, I iterate over index position and check for digits or word at that position.

# Day 02

The exercise: a handful of colored marbles are pulled from a bucket.
Assuming a per-color maximum, count invalid hands.
Part two: given the hands, determine the required minimum of each color in the bucket.
This is simply the max value of each color.

# Day 03

The exercise: parse a parts diagram, identifying multi-character numbers which are adjacent to parts symbols.
This is largely a parsing problem, mapping numbers to a location span.

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

The exercise: given a bunch of cards with numbers and corresponding numbers drawn, count the number of wins.
Part two: each time a card wins, consecutive cards are counted multiple times.

Relatively straight forward day.
Part two took a bit of squinting to understand what was being asked but the example helped.

## Approach

For part two, it could be tempting to replicate card data, but that tends to go poorly.
Instead, based on prior experience, I maintain a count/multiplication dict which is applies to each card total.

# Day 05

The exercise: given a number of translation rules which are applied to ranges, and a set of starting values, apply the translations in order.
Part two: same as part one but the starting set is actually a range.
The twist: the number of values is very large and managing it as a set of values is not viable.
Instead, the algorithm must handle ranges of values.
This requires applying range rules to ranges, potentially splitting ranges into multiple ranges (range overlaps).

That was a ride!
I managed to rank 416/2180.
At first I couldn't even parse right, as I used `split("\n\n\n)` which had an extra newline!
I tried a few approaches until I got a working algorithm for part 2.
I then had a bug where I assumed when an input range exceeded the translation range, the excess would be copied over directly without change; what needed to happen was to preserve that excess for processing by other translation rules.
Once that was fixed, I was failing to pass tests, because I changed variables around but failed to update the `return mix(...)` line.
I spent a bunch of time going over the example, line by line, until I realized that error.

## Approach

I initally solved part one using a set of values and part two using ranges.
I later updates part one to also use ranges so it can reuse the same code as part two.

One tricky bit here was handling range overlaps.
Given a translation rule which impacts `[3..5]` and an input range of `[2..7]`,
* the pre-overlap `[2]` is copied verbatim,
* the overlap `[3..5]` is translated, and
* the post-overlap `[6..7]` needs to be put back into the queue to potentially match future rules.
The last part of requeuing part of the overlap was easy to overloop and handle incorrectly.

# Day 06

The exercise: given a fixed amount of time to win a race, where the time is used to first charge the car then drive the car, determine the ways to split the charge then drive such that the car drives past a certain distance.
Part two: solve this with larger values.

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

The exercise: score multiple hands of cards based on Poker-like ordering. `J` is a Jack, sorted between `Q` and `T`.
Part two: `J` is a Joker, to be replaced with whatever yields the highest score.

I'm very glad I wrote a Python sort function in the past!
Figuring that out on the fly would have been challenging.

1. First mistake. For a short while I was passing the part one example but getting the wrong result for the real input.
   When I ordered hands of same rank, I was using `10 ** position` for adding up the card orders.
   However, there are more than 10 cards and that makes a difference!
   My logic was putting `2A` (value 10 + 13) ahead of `32` (20 + 1).
2. I was worried about handling ties and that my result might be wrong due to a draw.
   I added code to check for a draw (duplicate hands).
   However, those don't appear to exist in my input so I later removed it.

## Approach

This can be solved by writing a Python sort ranking function.
Hands can be described by a series of rules, encoded as the largest count of a card and the number of pairs.
`(5, 0)` is five of a kind. `(3, 1)` is three of a kind and one pair -- a full house.
Ties are broken by card valuesk in the order they appear.
Combined, this provides a mechanism for scoring any hand in a sort order.
For part two, `J` can be replaced by whichever card appears the most times (ties broken by card value), defaulting to `A` (eg for all Jokers).

# Day 08

The exercise: walk a ordered graph from start to end following cyclic L/R instructions and count steps.
Part two: given multiple starts and ends, figure out how many steps it takes to get from being at all starts to being at all ends.

## Approach

Assume each start-to-end count is cyclic.
Solve each start-to-end count then take the lowest common multiple.

## Part 2 data assumptions

The part two solution using LCM assumes that:
* `first_terminal_node == second_terminal_node`
* `distance(start_location, first_terminal_node) == distance(first_terminal_node, second_terminal_node)`
* `distance(start_location, first_terminal_node) == n * length(instruction)``

I added `pre_run()` logic to validate these assumptions.

## Issues

1. I wasted some time since I forgot to reset steps=0 inside my `foreach start` loop.
2. The instructions in part 2 has example nodes with digits in the name, which threw me for a loop.
   For part 1 I assumed the node names were all alpha.
   And they are!
   The example is just odd.

# Day 09

The exercise: given a sequence of numbers, use the iterative first-different approach to compute the next value.
This is how derivatives in math works.
Part two: extend the above to solve for test prior value as well as the following value.

I instantly recognized this as requiring solving a polynomial and describing the first differences approach.
However, I am not sufficiently familiar with numpy or other math libraries to leverage those.
I was also battling internet issues this night.

## Approach

I solved this using the recursive approach described in the exercise.
This was more of a "implement this algorithm" than "figure out how to solve this".
That said, using a math solver library would probably be less code and more efficient.

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

The exercise: walk an ASCII loop path around a map with odd corner symbols.
Count the steps to the midway point.
Part two: compute the area enclosed by the loop.

## Approach

I used three maps to figure things out.
The first is used to walk the loop and rotate at corners.
The latter two are used to replace the "S" start location with the appropriate pipe symbol.
Replacing the "S" symbol allows me to look at the pipe to compute the interior size.

* Corner symbol and input direction to an output direction (for rotating).
* Direction and value "pipe continues" symbols to test which sides of the start square are pipe continuations.
* A pair of start-neighboring continuation symbols to what the start symbol ought to be.

Walking the pipe is simple enough.
1. Start at the start location.
2. Pick a valid direction.
3. Walk the pipe, rotating at corners, until we get back to the start.
4. Return half the loop length.

Computing the interior is a bit more tricky.

The shoelace formula apparently makes it trivial.
That's not what I did!
First, I consider any part of the board which is not part of the loop as \"empty\".
Next, I did the \"ray crossing\" approach; if you start from outside the loop and draw a straight line, every time you cross a pipe you alternate from being outside the loop to being inside the loop.
When inside the loop, any empty space is tallied up.
Finally, add the loop itself.

Figuring out the crossing isn't always straight forward, though!
Crossing a `|` is a clear crossover; `F--7` or `L--J` is not a crossover; `F--J` or `L--7` is a crossover!
My initial approach was to track the start-end and to differentiate `F--J` from `F--7`.

It was then pointed out to me that we could consider the `F7` to be in the lower half of the cell and the `LJ` to be in the upper half of the cell.
Imagine the ray is only travelling in the upper half of the cell.
`LJ` are crossovers and `F7` are ignored.
`L--J` would be a cross-in then cross-out without any empty interior.
`L--7` and `F--J` would have a single cross-over.
`F7` doesn't register.
This makes the code a bit cleaner.

Note: I started 60 minutes late.

# Day 11

The exercise: sum the distance between all pairs of galaxies on the map.
Twist: any empty row or column counts as two empty rows or columns.
Part two: any empty row or column counts as 1000000 empty rows or columns.

## Approach

Always having everything as a `set[complex]` helped a whole lot here!
I was able to find empty rows/columns, assign each row/column an offset based on empty rows/columns and update all objects in the set.

I got hit hard by an off by one.
In part one, I added `1` to the offset on empty rows/columns.
For part two, I changed the `1` to `1000000`.
That ought to be `1` and `1000000 - 1` or `2` and `1000000`.

Once I resolved the off-by-one, this was pretty straight forward.

# Day 12

Exercise: count how many ways the unknowns can be resolved into a spring or gap to make the needed groups.
Part two: the input is larger.

I explored a number of approaches the proved futile.
I didn't solve this until five days later on my third approach.
My failed approaches tried too hard to be too clever and preemptively prune.
They were all riddled with errors and the pruning proved unneeded.
See the git history for all the ways I failed to solve this.

## Approach

# Day 13

Exercise: locate the horizontal and vertical lines around which the map is reflected.
Part two: assuming exactly one reflected cell needs to be toggled, find the reflection lines.

## Approach

Pick every possible line.
For every line, check if both sides matched a reflection of the other side.

I used a `set[complex]` here, as I do everywhere.
Using a `Sequence` might have made things easier as I could check if `data[i:j] == data[k:j - 1:-1]`.
On the other hand, sparse sets are faster than dense sequences.

TODO: try to solve this using a `Sequence`.

For part two, I just brute forced part one with each cell toggled.
Doing part two, I noticed my part one only checked reflections in one direction, which works so long as the reflection line is on one half but not on the other.
This cased incorrect part two results until corrected.

# Day 14

Exercise: given rolling and stationary rocks on a map, tilt the plane so the rolling rocks all roll until stopped.
Compute a value based on rock position.
Part two: repeat this process a large number of times.
Twist: that large number is too large to reasonably simulate.

## Approach

For part one, I just simulate things.
There are clever approaches using Sequences; this may be another day where `set[complex]` is not the best structure.

For part two, I track prior states and look for a cyclic pattern.
If the rocks finish in the same location after $cycle_a$ and $cycle_b$ rotations, then they will also finish in that location after $k * (cycle_b - cycle_a) + cycle_a$ cycles.
To compute the finish pattern after a large number of cycles, $number$,

```math
cycle_len = cycle_b - cycle_a
remainder = (number - cycle_a) % cycle_len
cycle_number = cycle_(a + remainder)
```

## Notes

This was one of those days with a lot of issues getting variable names correct, accounting for off-by-ones and other programmer errors.

Delayed start.

## Future improvements

I can deduplicate the 4-directions code by using the north code in a loop by rotating the grid 90 degrees between rotations.
However, that seems to slow things down by 50%.
It would be nice to find a fast way to dedupe that code.

# Day 15

Reading and understanding the ask today was a challenge.

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

# Day 21

## Part 1

Ranked 112.

## Part 2

Another hard one, solved for this specific input!

Key observations here:

* The garden is the same width as length, which are odd values (131).
* The starting position is in the dead center of the garden (65, 65).
* There is a direct path (no blocking stones) from the starting position to all four edges.
* The total number of steps is `(distance to garden edge) + 2 * k * (garden size)`.

The ramifications of the above:

* After 65 steps, the elf can reach the edges of the garden.
* After every `garden size` steps, the reachable steps expands in a semi-uniform pattern.
* If we consider every `2 * garden size` steps, the expansion pattern is even more uniform!
  The pattern alternates a bit every `garden size` steps so considering every `2 * garden size` makes the pattern more uniform.

I had not realized the pattern alternated which bit me pretty hard.
Eventually, I ran the thing and printed it out every `65 + k * garden size` steps for a few values of `k`.
The output can be visualized by chunking the map into 131x131 blocks and printing the number of reachable locations in each block as a grid output, i.e. displaying the diamond pattern.
It is also handy to print the number of each count.

```
Expansion 2
    0 |  964 | 5756 |  965 |    0
  964 | 6703 | 7650 | 6690 |  965
 5764 | 7650 | 7637 | 7650 | 5747
  984 | 6698 | 7650 | 6694 |  964
    0 |  984 | 5755 |  964 |    0
[(0, 4), (964, 4), (965, 2), (984, 2), (5747, 1), (5755, 1), (5756, 1), (5764, 1), (6690, 1), (6694, 1), (6698, 1), (6703, 1), (7637, 1), (7650, 4)]
[(5747, 1), (5755, 1), (5756, 1), (5764, 1), (6690, 1), (6694, 1), (6698, 1), (6703, 1), (7637, 1), (965, 2), (984, 2), (0, 4), (964, 4), (7650, 4)]

Expansion 4
    0 |    0 |    0 |  964 | 5756 |  965 |    0 |    0 |    0
    0 |    0 |  964 | 6703 | 7650 | 6690 |  965 |    0 |    0
    0 |  964 | 6703 | 7650 | 7637 | 7650 | 6690 |  965 |    0
  964 | 6703 | 7650 | 7637 | 7650 | 7637 | 7650 | 6690 |  965
 5764 | 7650 | 7637 | 7650 | 7637 | 7650 | 7637 | 7650 | 5747
  984 | 6698 | 7650 | 7637 | 7650 | 7637 | 7650 | 6694 |  964
    0 |  984 | 6698 | 7650 | 7637 | 7650 | 6694 |  964 |    0
    0 |    0 |  984 | 6698 | 7650 | 6694 |  964 |    0 |    0
    0 |    0 |    0 |  984 | 5755 |  964 |    0 |    0 |    0
[(0, 24), (964, 8), (965, 4), (984, 4), (5747, 1), (5755, 1), (5756, 1), (5764, 1), (6690, 3), (6694, 3), (6698, 3), (6703, 3), (7637, 9), (7650, 16)]
[(5747, 1), (5755, 1), (5756, 1), (5764, 1), (6690, 3), (6694, 3), (6698, 3), (6703, 3), (965, 4), (984, 4), (964, 8), (7637, 9), (7650, 16), (0, 24)]

Expansion 6
    0 |    0 |    0 |    0 |    0 |  964 | 5756 |  965 |    0 |    0 |    0 |    0 |    0
    0 |    0 |    0 |    0 |  964 | 6703 | 7650 | 6690 |  965 |    0 |    0 |    0 |    0
    0 |    0 |    0 |  964 | 6703 | 7650 | 7637 | 7650 | 6690 |  965 |    0 |    0 |    0
    0 |    0 |  964 | 6703 | 7650 | 7637 | 7650 | 7637 | 7650 | 6690 |  965 |    0 |    0
    0 |  964 | 6703 | 7650 | 7637 | 7650 | 7637 | 7650 | 7637 | 7650 | 6690 |  965 |    0
  964 | 6703 | 7650 | 7637 | 7650 | 7637 | 7650 | 7637 | 7650 | 7637 | 7650 | 6690 |  965
 5764 | 7650 | 7637 | 7650 | 7637 | 7650 | 7637 | 7650 | 7637 | 7650 | 7637 | 7650 | 5747
  984 | 6698 | 7650 | 7637 | 7650 | 7637 | 7650 | 7637 | 7650 | 7637 | 7650 | 6694 |  964
    0 |  984 | 6698 | 7650 | 7637 | 7650 | 7637 | 7650 | 7637 | 7650 | 6694 |  964 |    0
    0 |    0 |  984 | 6698 | 7650 | 7637 | 7650 | 7637 | 7650 | 6694 |  964 |    0 |    0
    0 |    0 |    0 |  984 | 6698 | 7650 | 7637 | 7650 | 6694 |  964 |    0 |    0 |    0
    0 |    0 |    0 |    0 |  984 | 6698 | 7650 | 6694 |  964 |    0 |    0 |    0 |    0
    0 |    0 |    0 |    0 |    0 |  984 | 5755 |  964 |    0 |    0 |    0 |    0 |    0
[(0, 60), (964, 12), (965, 6), (984, 6), (5747, 1), (5755, 1), (5756, 1), (5764, 1), (6690, 5), (6694, 5), (6698, 5), (6703, 5), (7637, 25), (7650, 36)]
[(5747, 1), (5755, 1), (5756, 1), (5764, 1), (6690, 5), (6694, 5), (6698, 5), (6703, 5), (965, 6), (984, 6), (964, 12), (7637, 25), (7650, 36), (0, 60)]
```

Note how the number of unique cell values does not change after four expansions.
Only the count changes.
We can run the algorithm for four expansions then use the output to capture the cell values.

The non-zero cells include:

* The four tips/points.
* The four diagonals which include alternating more full (inner) and less full (outer) cells.
* The alternating interior cells.

All that is needed at this point is to count how many of each is expected after `k` expansions and sum them up.

* There are always exactly one set of tips.
* The diagonals grow linearly (`expansions` and `expansions - 1`).
* The interior cells grow quadratically (`expansions ^ 2` and `(expansions - 1) ^ 2`).

### Follow up

Simulating `65 + 131 + 131` steps to get all the garden block values is very slow as the growth is exponential.
It would be faster to compute each of those garden blocks independently as a single, non-repeating garden, with a known set of start points and step counts.
Using the above knowledge, we can compute the size of those unique garden cells in isolation by feeding in the correct start locations.

# Day 22

Some data checks that made me feel better.

```python
assert all(x1 < 10 and y2 < 10 and x2 < 10 and y2 < 10 for x1, y1, z1, x2, y2, z2 in bricks.values())
assert all(x1 <= x2 and y1 <= y2 and z1 <= z2 for x1, y1, z1, x2, y2, z2 in bricks.values())
```

The mapping of bricks to footprints and `(x, y)` columns to bricks is a bit tedious.
But it is also `O(n * 3 * 100)` or so, which is `O(n)`.
I tried being smarter about finding brick overlaps, but it was much slower, being `O(n^2 / 2)`.

```python
potential_supports = collections.defaultdict(set)
for idx, brick in enumerate(landing_order):
    start_x, start_y, _, end_x, end_y, _ = bricks[brick]
    for other in landing_order[:idx]:
        other_start_x, other_start_y, _, other_end_x, other_end_y, _ = bricks[other]
        if not (
            other_end_x < start_x or other_start_x > end_x
            or other_end_y < start_y or other_start_y > end_y
        ):
            potential_supports[brick].add(other)
```

# Day 23

## Part 2

Optimizations

* Using a `collection.queue()` and DFS runs 3-6x faster than using a `set` or `PriorityQueue`.
  Using a `list` is just as fast, too!
* Tracking the best value at each `(node: Node, seen: set[Node])` takes up too much memory.
* Detecting if a given path can reach the end or is cut off seems to take 5% more time.
* Computing `sum(max(steps into node) for reachable unvisited nodes)` as an upper bound and pruning when `steps + upper bound < max steps seen so far` improves speed by roughly 30%.

# Day 24

## Part 1

I was embarrassed at how much geometry I had forgotten.
I needed to look up how to compute line intersections on Wikipedia.
I also took a while to debug my `px, py, pz, vx, vy, vy = line` bug!
Yet with all that, I still managed to rank under 500!

# Part 2

Apparently it's the day of constraint solvers, which makes for a very, very unsatisfying solution.
Some people are figuring out how to solve this more directly, but it seems most the people that solved it in the first four hours used z3 or similar.

# Day 25

I briefly considered `networkx` but I couldn't find an algorithm at a quick glance so I assumed it wouldn't have what I needed.
I was very wrong.
I tried a bunch of approaches (see messy commits) until I found something that worked for me.
