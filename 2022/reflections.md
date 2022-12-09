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

# Day 9: Rope Bridge. Track the movement of knots.

Code:

* [Initial rough solution](https://github.com/IsaacG/Advent-of-Code/blob/5ceeceb2a06c75d1eb11d9e7cc14e13e41faf008/2022/09.py)
* [Latest](https://github.com/IsaacG/Advent-of-Code/blob/main/2022/09.py)

Thankfully I had recently written a `DIRECTIONS` list with the four cardinal directions as complex numbers.
I ended up using a `case match` to map "RLUD" to complex directions but pulled the `DIRECTIONS` and diagonals from my library.
I later changed that to a `dict[str, complex]`.

Being able to check `if head - tail in DIRECTIONS + DIAGS` was helpful here to know if the tail needed to move.

Figuring out how to move the tail took a moment of thought; if the x-values differ, it moves along the x.
Same for y.
I ended up with a bunch of tests to generate the movements of `-1, 0, 1`.
Perl has a `a cmp b` (strings) and `a <=> b` which returns `-1, 0, 1` so I added `aoc.comp(a: float, b: float) -> int` which does that.
Now, the movement is `complex(cmp(a.real, b.real), cmp(a.imag, b.imag))`.
