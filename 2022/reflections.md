# Day 1: Calorie Counting. Count how many calories the elves have.

I spend the first three minutes trying to create a file since my template generator was broken.

# Day 2: Rock Paper Scissors. Score a tournament.

# Day 3: Rucksack Reorganization. Find common elements across groupings.

# Day 4: Camp Cleanup. Detect overlapping ranges.

# Day 5: Supply Stacks. Move crates from stack to stack.

Medical emergency. I got to this an hour or two after it started.

# Day 6: Tuning Trouble. Parse data streams to find the start of messages.

I started out with a byte generator, but then switched to a `collections.dequeue` to support peeking.
This may be the first time I used a `dequeue`.

# Day 7: No Space Left On Device. Parse filesystem output info.

Initially I created a `DirEntry` which would store the children directories and filesizes of all nodes within each directory.
I used a `dict[pathlib.Path, DirEntry]` to traverse entries.
I later switched to a `dict[pathlib.Path, int]` and only stored sizes.
I also replaced the recursive directory size computation by updating parent directories every time a size was added.

This may be the first time I used Python's new `match case`.

# Day 8: Treetop Tree House.

I had Dijkstra on my mind, so when this puzzle dropped, I immediately tried to use Dijkstra.
That didn't work too well.
This resulted in my worst performance so far this year (of exercises I was able to start on immediately).
My idea was:

```python
visible = edges
todo = visible
while todo:
    for tree in todo:
        for tree.neighbors not in visible:
            if line of visible trees from neighbor to edge:
                add neighbor to todo
                add neighbor to visible
```

This algorithm would find visible trees ... that have only visible trees between it and the edge.

What is actually needed is much simpler.
I got there eventually.
I initially checked each tree in the map for a direct line of sight to the edge.
I later cleaned this up by walking the perimeter and "looking" into the forest along each row/column and recording what trees are visible.

## Library Changes

* New `aoc.Board.edges`

# Day 9: Rope Bridge. Track the movement of knots.

## Code

* [Initial rough solution](https://github.com/IsaacG/Advent-of-Code/blob/5ceeceb2a06c75d1eb11d9e7cc14e13e41faf008/2022/09.py)
* [Latest](https://github.com/IsaacG/Advent-of-Code/blob/main/2022/09.py)

## Library Changes

* Added `cmp(a, b)` which returns `-1 | 0 | 1` if `a < b | a == b | a > b`.

## Musings

Thankfully I had recently written a `DIRECTIONS` list with the four cardinal directions as complex numbers.
I ended up using a `case match` to map "RLUD" to complex directions but pulled the `DIRECTIONS` and diagonals from my library.
I later changed that to a `dict[str, complex]`.

Being able to check `if head - tail in DIRECTIONS + DIAGS` was helpful here to know if the tail needed to move.

Figuring out how to move the tail took a moment of thought; if the x-values differ, it moves along the x.
Same for y.
I ended up with a bunch of tests to generate the movements of `-1, 0, 1`.
Perl has a `a cmp b` (strings) and `a <=> b` which returns `-1, 0, 1` so I added `aoc.comp(a: float, b: float) -> int` which does that.
Now, the movement is `complex(cmp(a.real, b.real), cmp(a.imag, b.imag))`.

# Day 10: Cathode-Ray Tube. Emulate a simple CPU and program with a cycle counter.

## Code

* [Initial rough solution](https://github.com/IsaacG/Advent-of-Code/blob/691664c8409c98addeedab3de6cfbf8713377b12/2022/10.py)
* [Latest](https://github.com/IsaacG/Advent-of-Code/blob/main/2022/10.py)

## Musings

This was a tricky puzzle to solve.
My immediately approach to handling the cycles was to pre-process the inputs and translate `addx` instructions into `noop, addx` so I can treat each instruction as a single cycle.
This worked out quite well!

Part two involves pixel art, similar to 2021/13.
Last year, I shrugged it off.
This year, I used bitmaps from GitHub to build an "OCR" mapping.
([6x4 map](https://github.com/SizableShrimp/AdventOfCode2022/blob/main/src/util/java/me/sizableshrimp/adventofcode2022/helper/LetterParser.java#L44) for this year and [10x7 map](https://github.com/mstksg/advent-of-code-ocr/blob/main/src/Advent/OCR/LetterMap.hs#L210) for 2018.)
Rather than translating the `bool` values to on/off pixels, they can be converted to bits and constructed into a number.
This number can be used as a `dict[int, str]` key which maps bits to a letter.

I'm happy I finally have an AOC OCR!

## Library Changes

* New `aoc.OCR`

# Day 11: Monkey in the Middle.  Track items thrown between monkeys."""

## Code

* [Initial rough solution](https://github.com/IsaacG/Advent-of-Code/blob/390ef4ba4749638975fce78ff6bc9c01d8e29f17/2022/11.py)
* [Latest](https://github.com/IsaacG/Advent-of-Code/blob/main/2022/11.py)

## Musings

This exercise was very heavy on the input parsing.
I feel like Python and my skillset is typically up for that challenge.
However, I fell into a trap which took a long while to debug.
There were also quite a lot of details that needed to be accounted for.

Mistake: I fell into [the `lambda` late binding trap](https://medium.com/skiller-whale/late-binding-variables-its-a-trap-c17af980164f).
It took a lot of puzzling to realize my `lambda` functions were not functioning correctly.
I fixed the "Operation" `lambda` ... but the "Test" `lambda` still had that issue.
Once I fixed the second late binding issue, my code was in the clear.
When tidying up my code, I reverted the `functools.partial`s with `lambda`s and used "parameter default values" to bind values.

Adding dictionaries to the `dataclass` has a noticeable impact on performance.
Using `slots=True` has a noticeable improvement.

I don't usually use multi-line regexes, but for this exercise, I feel it's cleaner to do so.

# Day 12: Hill Climbing Algorithm.

## Musings

I managed to recognize this one pretty quickly as a BFS graph traversal problem.
For some reason I got it in my head that I need a PriorityQueue for this.
24 minutes in, I had to accept my code was not working, so I dropped my solution and restarted.
(See the rough code.)
Six minutes and rewriting it using a `set` and `min()`, and I got it to work.

Updates:

* Run BFS only once with multiple starting nodes.
* Replace `todo: set` with `todo: dequeue`.
* Move the diagonal setting in `aoc.Board` into the `__init__`.
* Change `aoc.Board.neighbors` from `list` to `dict`

# Day 13: Distress Signal. Sort packets of types int and nested lists.

Input parsing was simple with my parsing lib.
Originally I used `aoc.ParseBlocks([aoc.parse_one_str_per_line])` then ran the inputs through `eval()`.
When cleaning up, I switched to `aoc.ParseBlocks([aoc.ParseOneWordPerLine(json.loads)])` which does it all in one go.

Writing the `cmp()` code wasn't too bad.
I originally started with returning a `bool` before realizing I needed three return values.

When I saw part two, I realized I needed to use `sort(key=func)` which is supposed to return `True` when `a < b`.
To make that happen, I (incorrectly) attempted to switch all my `return <x>` to `return <x> == 1` (negating the logic).
I then didn't know how to make this work with `cmp` and a single value, but I thankfully found `sort(key=cmp_to_key)` which takes a `cmp(a, b)` function.
I switch to using `sort(key=cmp_to_key(cmp))` ... but forgot to revert from `bool` to `-1 | 0 | 1`.
I then spent 20-25 minutes trying to understand why `sort()` was not changing the list order, and trying to write a bubble sort (with the incorrect bool logic).
Once I realized that `cmp_to_key()` expects `-1 | 0 | 1`, the solution came quickly.

This got me wondering how `cmp_to_key()` even works and how I'm supposed to sort things.
I looks up [the `cmp_to_key()` source](https://github.com/python/cpython/blob/0e081a089ec969c9a34f5ff25886205616ef4dd3/Lib/functools.py#L206) and it's much simpler than I expected!
The "Sorting HOW TO" also suggests a [Decorate-Sort-Undecorate pattern](https://docs.python.org/3/howto/sorting.html#decorate-sort-undecorate).

# Day 14:

Fun little puzzle!
I got part one mostly working ... but I was getting the wrong results.
I spent a whole lot of time debugging and staring at outputs until I caught the bug.

```python
# What I meant to do:
while can_move and cur.imag < max_y:
    for d in directions:
        if cur + d not in rocks and (cur + d).imag < max_y:
            cur += d
            break
    else:
        can_move = False

# What I did do:
while can_move and cur.imag < max_y:
    for d in directions:
        if cur + d not in rocks and (cur + d).imag < max_y:
            cur += d
            break
        else:
            can_move = False
```

Todo:

* (DONE) Add point parsing to parser lib. `INPUT_PARSER = aoc.parse_re_findall_points`
* (DONE) Use backtracking to optimize speed. 88ms/2501ms to 38ms/109ms.


# Day 15: Beacon Exclusion Zone. Locate a beacon based on knowing where it is not.

I was hanging out with friends (lights in the park!) so I started this one 35-45 minutes late.
I solved both parts in roughly 45 minutes.

* Take 1, using the NUC and `dataclass` for the Sensor: 110s
* Take 2, using the NUC and a `tuple` for the Sensor, reducing function calls: 53s
* Take 3, same code as take 2 but on the desktop: 37s.
* Take 4, same code and hardware as take 3, switching cython for mypy3: 1.5s.

The distress beacon exists at a point either along the edge or just along the edge of the range of two sensors.
By finding sensors whose edges are 2 units apart, we can reduce the bounds which need checking from `(0, 4_000_000)^2` to a box bound by those sensors.
This optimization reduces my runtime from 56s to 5.0s (reducing just along the y-axis) or 4.7s (reducing along both axes).
Solving this "properly" would require adding checks to search the edges since the beacon may exist at an edge and not fenced in by four sensors.

Follow up: `W` solved this by intersecting diagonal lines formed by sensor detection edges.
What if I used the above sensor-pairs to form diagonals and then intersected just those?
Doing so gets me a near-instant result for part 2.

Approach:

* Store sensors as their coordinate `(x, y)` and a "sensor range", i.e. distance to beacon, yielding `tuple[int, int, int]`.
* Sensors can be sorted (on `x`) to process them from left to right.
* For each (sorted) sensor combination, check if their distance is one more than their combined range, i.e. they have space for exactly one width of space between them.
* Based on the relative `y` positions, this is either a 45 degree line up-and-right or down-and-right.
  The slope is either `+1` or `-1`.
  These lines can be stored as `y = mx + b` or just `b` if using two containers for the different slopes.
* For each combination of `m = +1` and `m = -1` lines, compute the intersection.
  Filter out intersections outside the bounding box, `(0, 4,000,000) x (0, 4,000,000)` (optional if there are multiple lines).
* The intersection gives the coordinates of the distress beacon.

I revisted part 1 to reduce the runtime.
Instead of tracking points, I opted to track ranges.
Initially, I attempted to update overlapping ranges on the fly, but latter ranges can replace multiple prior ranges and the code got tricky.
Instead, I collected all the ranges then sorted and walked the ranges to produce a flattened set of ranges.
This reduced my part 1 runtime to under 0ms.

# Day 16: Proboscidea Volcanium. Open valves to release pressure.

One of the harder days in a while. 

I spent about 2.5 hours trying to solve this using Dijkstra's.
When that did not bear fruit, I spent 2.5 hours working out a solution using DFS and combination-testing.
5 hours in, I revisited Dijkstra's and found a silly bug in my code (`added_release = rate[human_valve] * cycles + rate[elephant_valve]`).
Using some arbitrary pruning, I got this to eventually work with Dijkstra's.
Using the valves opened by Dijkstra's, I got the combination testing to work.
I'm still debugging the combination testing and trying to make it work with all the valves as input.
I found Floyd Warshall very useful for computing room distances, though I also wrote a DFS to validate the distances while debugging.

Todo:

* Clean code.
* Make combination testing work.

# Day 17: Pyroclastic Flow. Compute the height of a Tetris-like rock pile after rocks have landed.

Part one had a whole lot of bugs and off-by-ones.
I manually entered the rock sizes vs parsing them, thinking it would save me time.
I thought I was tracking the rock's top left corner but was tracking the bottom left corner, since I defined the rocks as starting at `(0, 0)` and sizing up, not down.
I had an off-by-one in my "add height" logic.
I had a whole slow of off by ones.

Part two, I realized pretty quickly I needed to find a cycle.
My input leads to occasionally "flat tops" which I can use as a nice break point, at which to check for a cycle.
I believe the example and other inputs do not have any flat tops, so my solution would not work for many other inputs.
This can be solved by looking for a solid non-flat top (assuming one exists) or using other heuristics to detect a "stable" top, e.g. hashing the landed blocks for the last N rows or checking the landing position of the last N rocks.
(N likely needs to be 10-50 or suchlike, based on discussions.)
Not relying on a flat top would allow detecting cycles sooner but require storing more state.

Some silly things I did:

* Confuse my loop counter `i` as the counter used for both the rock size and stream index.
  I actually thought I could use `(i % types_of_rocks, i % stream_length)` for my cycle counter.
  What is needed is `(rock_idx % types_of_rocks, stream_idx % stream_length)`.
* I used a loop to "add" cycles. I added cycles until *at least* `target` rocks have fallen, which took me too far.
* I add cycles, add a new flat top and then run the simulator until `target` rocks have fallen.
  Instead, I should save height values and just compute the height using prior cycle data.

Follow up:

* (DONE) do not continue the sim once a cycle is found; use cached height data.
* (DONE) parse rocks from image
* (DEBATING) fix the off-by-one that makes the corner (0, 1).
  The height 1 means the tower is 1 high after the last rock falls.
  I could shift everything right and make it (1,1) but I'm not sure that's better.
* (TODO) do not assume flat top; use landing position data for the last N cycles for cycle detection.

# Compute the surface area of 3D bubbles.

Relatively simple and straight forward puzzle.
However, I first solved for grouping points of lava into lava-groups of touching points.
I managed to solve part 1 with this grouping, but it was entirely unnecessary.
I attemted to use the grouping in part 2 to compute bubble interiors but the grouping did not check diagonals so that didn't work out.
Turns out, the brute-force flood fill approach works plenty fine in about 170ms.


# TODO

* Day 16

# Day 20: Grove Positioning System. Decrypt position data by doing list mixing.

Initially I started off with a list.
That quickly failed hard.
I quickly pivoted to a double linked list.
I spent two hours debugging part two.
I used a `dict[int, Node]` to map a node's value to the node, to find nodes quickly.
I failed to verify that the values are unique (which they aren't).
Once I got that working, I had a hard time with the off-by-one errors when nodes get moved one full loop.
The `self` location needs to be skipped when moving.
With modulo, it needs to use `movement %= len(list) - 1`.
That took a while to figure out.
Part two was easy enough with a working part one.


# Day 21

Solve for `humn`.
Part one was relatively simple and straight forward.
Part two was interesting.
For my initial solution, I resolved any equation which had all-numeric inputs.
Equations with non-numeric inputs were kept as strings but expanded.
I hand-reversed the resulting equation in `vim` to isolate `humn`.

Todo:

* Solve this in code. Linear interpolation, sympy or simply reversing all the operations.


# Day 22: Monkey Map. Wander a wrapped map to find a final location.

This was a wild ride.
Complex numbers proved useful again here.
Cut-out folded cubes also proved invaluable.
I initially hard coded the corners of each face and the face-to-face transitions.
I have changed the corner computation to be done in code.

Todo:

* Try to write code to compute face-to-face transitions.

# Day 23: Unstable Diffusion. Spread elves out across a field to plant trees.

Cellular automata day (Game of Life)!
I like these.
I started 55 minutes late (Peruvian dinner) but completed within about an hour.
I got slowed down because I missed the rule about elves without neighbors doing nothing.
Overall, relatively simple and straight forward.
It was a nice break after yesterday.

# Day 24: Blizzard Basin. Navigate across a basic, avoiding storms.

I kept the walls in my data, making the valid "edges" one less than normal, which introduced a bunch of off-by-one errors which took a while to debug.
I got my part two solution initially by repeatedly updating my code with the move count from the prior leg.
My runtime was pretty bad at 120s.
Switching a `set[complex]` with `min(key=...)` to a PriorityQueue changed my runtime to 5s.
