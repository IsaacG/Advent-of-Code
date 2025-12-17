# Advent of Code 2025 (Python)

## Stats

Ranking is +/-5 as the data is giving in groups of 10.

```
Day   Part 1   Rank    Part 2   Rank    Delta
-----------------------------------------------
 1   00:02:16   160   00:05:18   170   00:03:02
 2   00:02:16   160   00:05:18  8470   00:01:44
 3   00:02:16   240   00:05:18   210   00:03:39
 4   00:02:16   540   00:05:18   400   00:01:56
 5   00:02:16   940   00:05:18   840   00:06:51
 6   00:02:16  1380   00:05:18   680   00:10:23
 7   00:02:16   650   00:05:18   470   00:04:23
 8   00:02:16  1650   00:05:18  1430   00:04:04
 9   00:02:16   220   00:05:18  1850   01:25:05
10   00:02:16  1190   00:05:18   750   00:40:18
11   00:02:16   350   00:05:18   940   00:16:59
12   00:02:16  1790   00:05:18  1550   00:00:09
```

## Musings

2025 saw AoC reduced from 25 days to 12 days.
I solved each puzzle in both Python and Go (and some even in awk).

## Day 01

Solving part 2 without brute force is surprisingly (and frustratingly) challenging!
Thankfully brute force works perfectly well here.

## Day 02

Fun, interesting little puzzle.
The regex solution is simple, but fairly slow.
A non-regex solution could be used to make part 1 significantly slower.
Go's regex library doesn't support back references.
The 3rd party regex library is about as slow as Python!

## Day 03

This puzzle is relatively straight forward.
Part 2 requires some consideration but it wasn't too bad.

## Day 04

This feels like a classic AoC puzzle.
My automatic `Map` parser is lovely for puzzles like these.
Part 2 felt pretty simple.

## Day 05

Another relatively simple puzzle.
Reasoning about overlapping ranges is always tricky!

## Day 06

Part two was tricky in a refreshingly different way.
This largely because a parsing and string handling exercise.

## Day 07

Antoehr relatively straight forward puzzle where I appreciated having my `Map`.

## Day 08

A fun challenge.
I'm told this is [Kruskal's algorithm](https://en.wikipedia.org/wiki/Kruskal%27s_algorithm).
This exercise gave me an excuse to implement Disjoint Set Unions (DSU), though I didn't use the full thing.
I played with `heapq` here, too, which is not something I use much.

## Day 09

This is where things got challening.
`shapely` is apparently a popular tool for this exercise, as is coordinate compression.
I took the easy way out and solved for the "nice" case initially.
I circled back later with some line scanning to write a solution which can handle any evil inputs.

## Day 10

Parsing this one correctly was hard on me; I kept parsing the lights in reverse.

I initially solved this using z3, which is good because [integer linear programming](https://en.wikipedia.org/wiki/Integer_programming) is apparently hard.
I then learned about [the "bifurcate" method on Reddit][bifurcate] which doesn't require z3.
I implemented that solution ([pypy](https://github.com/IsaacG/Advent-of-Code/blob/main/advent_of_code/2025/d10.pypy) and Go), though it's a bit slower.
I didn't set up z3 for Go so it's nice to have options.

## Day 11

A classic dynamic programming/graph traversal.

## Day 12

A classic way to go out.
[Bin packing](https://en.wikipedia.org/wiki/Bin_packing_problem), an NP-complete problem.
Thankfully, you don't need to actually solve it, though this did leave me frustrated.


[bifurcate]: https://www.reddit.com/r/adventofcode/comments/1pk87hl/2025_day_10_part_2_bifurcate_your_way_to_victory/
