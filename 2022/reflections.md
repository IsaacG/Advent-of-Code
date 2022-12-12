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

Todo:

* Run BFS only once with multiple starting nodes.
* Replace `todo: set` with `todo: dequeue`.
* Move the diagonal setting in `aoc.Board` into the `__init__`.
* Change `aoc.Board.neighbors` from `list` to `dict`
