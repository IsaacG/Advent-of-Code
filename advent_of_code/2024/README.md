# Advent of Code 2024 (Python)

## Stats for 2024.

```
      -------Part 1--------   --------Part 2--------   --------Delta---------
Day       Time  Rank  Score       Time   Rank  Score       Time   Rank  Score
 25   00:10:12    758      0   00:10:15    623      0   00:00:03   -135      0
 24   00:13:31    701      0   03:58:18   2222      0   03:44:47   1521      0
 23   00:05:20    429      0   00:23:57    947      0   00:18:37    518      0
 22   00:07:08    773      0   00:46:36   1647      0   00:39:28    874      0
 21   01:15:20    674      0   03:51:12   1640      0   02:35:52    966      0
 20   01:01:37   3293      0   01:25:30   2165      0   00:23:53  -1128      0
 19   00:10:00   1253      0   00:22:39   1836      0   00:12:39    583      0
 18   00:09:24    679      0   00:30:36   2419      0   00:21:12   1740      0
 17   00:17:56    870      0   14:14:20  10871      0   13:56:24  10001      0
 16   00:29:42   2059      0   00:40:09   1072      0   00:10:27   -987      0
 15   01:18:13   5802      0   02:05:10   3168      0   00:46:57  -2634      0
 14   00:48:27   5287      0   01:35:30   4671      0   00:47:03   -616      0
 13   00:19:58   1951      0   02:16:39   6040      0   01:56:41   4089      0
 12   00:10:32    783      0   01:02:31   2033      0   00:51:59   1250      0
 11   00:05:15    650      0   00:38:51   3188      0   00:33:36   2538      0
 10   00:14:46   1953      0   00:16:49   1558      0   00:02:03   -395      0
  9   00:10:04    419      0   00:27:18    489      0   00:17:14     70      0
  8   00:21:26   2767      0   00:25:53   2046      0   00:04:27   -721      0
  7   00:09:11   1296      0   00:11:46    977      0   00:02:35   -319      0
  6   00:09:24   1006      0   01:43:47   6522      0   01:34:23   5516      0
  5   00:21:08   4357      0   00:38:09   4201      0   00:17:01   -156      0
  4   00:05:01    544      0   00:08:49    289      0   00:03:48   -255      0
  3   00:05:08   1559      0   00:11:31   1417      0   00:06:23   -142      0
  2   00:07:00   1241      0   00:10:47    952      0   00:03:47   -289      0
  1   00:29:05   7757      0   00:31:56   6927      0   00:02:51   -830      0
```

## Auto Parsing

My auto-heuristic parsing handles most the inputs this year (after some work).
Auto-parsed days: 01, 02, 04, 06, 08, 10, 11, 12, 16, 18, 20, 21, 22.

I also introduced a new `aoc.CoordinateParser()` which returns an `aoc.Map`.
This was very handy this year and deprecated the old `Board` code.
Days using this new parser: 04, 06, 08, 10, 12, 15, 16, 20, 25

## Reflections

The prose felt a bit longer and more complicated this year.

### Day One

Good warm up.
Got to learn my tools again.
I managed to forget about AoC and started 15 minutes late.
I also forgot about `zip()` for transposing.

### Day Two

The `sign()` function is handy, similar to `cmp()`. It's a pity Python doesn't have these built in.

### Day Three

The input is split across lines, but the lines are not actually separate inputs.
My auto-parsing does not handle that well so this needed an explicit parsing.

Regex for the win for this day.

I initially solved this without realizing there was a constraint that numbers never exceed 3 digits.

### Day Four

Complex maps FTW.
THis is where I created a new Coord Parser which returns a set of complex coords for each character in the map.

### Day Five

I managed to solve this without realizing the graph has a loop in it.
I got lucky with my start point.
I also over complicated things by thinking a step could be missing.
`a|b b|c c|d` requires a then b then c; I thought a then c was valid.
(At least, there is nothing in the example to counter that understanding.)

My auto parsing doesn't touch multi-block inputs yet.

### Day Six

Complex values and my CoordinateParser win the day.
Reducing the loop check by only checking occasionally (eg when rotating) helped a whole lot!
10 minutes for part one, another 1.5 hours for part two!

### Day Seven

Someone on IRC noticed working from the end (right) you can prune much more aggresively, resulting in a significantly faster solution!
Two minute delta between parts.

### Day Eight

This is when I introduced the CoordinateParser and retrofitted it into prior days/years.
Four minute delta between parts.

### Day Nine

I felt there much be a better approach here with a `heapq` or `PriorityQueue` but wasn't able to figure it out myself.
I saw someone else had 9 `heapqs` groups by hole size and I was able to copy that idea, for large speed improvements.

### Day Ten

This day, I accidentally solved part two first.
Two minute delta between parts by undoing the last of my part one changes!

### Day Eleven

This one was rough until I worked out how to solve it with dynamic programming, then it became very simple!
DP also brough runtimes down from "ridiculous" to fast.

This might have been the day where I played around with using `len(str(x))` vs logarithms and decided logs are not worth using.

### Day Twelve

I found the hard way to solve this: walk the perimeter and count turns.
Implementing that correctly was rough.
I forgot about islands and needed to go back for that, too!
There are much, much simpler solutions, like _detecting_ corners (which I eventually used) or counting edges.

I created a flood-fill and partition helper function after this.

10 minutes for part one, 50 for part two.

### Day Thirteen

I had a very hard time with this one.
I eventually gave up and used `z3` to solve this.
Linear Diophantine equations were mentioned, which I used to detect which combinations have a solution (later removing that).
I tried to use `scipy` but didn't get that to work.
After AoC was over, I eventually returned to this and solved it using linear algebra and a system of two equations, using substitution.
The linear equation solution is much, much simpler, though it does have some rounding issues.

20 minutes for part one, 2 hours for part two.

This uses the block parser.

### Day Fourteen

This was a tricky one.
I initially tried paging through frames, but that was a lot of clicking and squinting, trying to figure out if a squiggle counted as a tree.
I noticed _some_ grouping/pattern happening every so often but failed to nail down the pattern.
Eventually I let it run at full speed and saw the tree.
Once I knew _exactly_ what I was looking for, I was able to write code to detect it.

### Day Fifteen

I found this one to be quite fun!
I thought the complex types were quite helpful.

### Day Sixteen

Initially I forgot to include the "E" in the possible locations where the reindeer could move and had a very hard time figuring out why my algorithm wasn't reaching the end!
I debugging this by checking the algoirthm's (A\*) state one step at a time, which was very slow.
I should have checked the first few steps then skipped ahead a whole lot towards the expected end.
I implemented a NetworkX solver for this, too, though I'm not sure if I'd use NetworkX often.
I enjoyed this one.

10 minute delta.

### Day Seventeen

This part two was a hard one.
I ended up solving it the next day (14 hours later).
This is the only puzzle I didn't solve within 4 hours of the release time.

Brute force wasn't going to cut it.
Understanding the specific input and the program behavior was essential to cracking this one.
The first few times I tried to convert the program to code, I kept incorrectly using a combo literal where it was supposed to be a literal.

Each output digit is composed on the right-most (3 bit) byte, `int_one`, and a second byte, `int_two`.
The `int_two` is found (`int_one ^ 7`) bits from the right.
For instance, `0b101_010_101` has `int_one = 101 = 5`.
`int_two` is located `101 ^ 7 = 101 ^ 111 = 010 = 2` bits to the left.
Shifting by two gives `10_1 = 101 = 5` as int_two.
The output is `3 ^ int_one ^ int_two`.
This function brute forces by trying all possible values for `int_one`.
Given `int_one`, we can brute force `int_two` by setting `int_two = digit ^ 3 ^ int_one`.
After shifting `int_two` over and adding it to the number, we need to ensure `int_one` wasn't overwritten.

As an optimization, the preserve bits are used to track which bits are "set" and should
not be updated/overwritten to compute over digits.

### Day Eighteen

I read the problem and immediately assumed I would have to compute the maze with pieces falling on each step.
Part two can be solved in a bunch of interesting ways.
I took the simple route of trying to see if the maze could be completed after N fallen pieces.
I tried to be clever by using a binary search to select N but I managed to mess up binary search repeatedly.
I tried to use `(a - b) / 2` to get a midpoint (average) and was flumoxed by why that didn't work.
I took forever to figure out how to correctly update the high and low.
It was rough.

I eventually opted to swap from `complex` to a `tuple[int, int]` and added some tuple-based helper functions.

### Day Nineteen

I tried to be smart by using the longest towel first, and subtracting it from both ends, which ended up biting me hard in part two where that led to double counting.

### Day Twenty

I attempted to compute all possible cheat offsets by using `itertools.product(FOUR_DIRECTIONS, repeat=20)` which ... is a lot.
I assumed my maze logic was slow but it turns out that one call was hanging my program for minutes.
Switching to a much simpler set of nested ranged made things reasonable and reminded me to add debug logging which shows each step.
This time I remembered to add the end to the available spaces (unlike the camel race).
I originally assumed I would need to test the value of each "cheat" by combining the distance from the "S" to the cheat start and the distance from the cheat end to the "E" (with a Dijkstra distance map).
It took some convincing but I finally realized I only need the distance-to-end map.

### Day Twenty One

This puzzle took me a long time to crack -- nearly four hours.
My initial solution ignored the "null" requirement; I thought it wouldn't make a difference, but I was very wrong.
Another day for dynamic programming combined with recursion.
Memoizing `A -> button -> A` with a depth makes this run fast.
The key here was to realize how each `A -> button -> A` (at any given level) is indepedent and can be cached.
The "A" parts don't even need tracking!

### Day Twenty Two

I initially wrote this as a bunch of small functions to help keep things straight and avoid confusing variables.
I played around a bunch with the "fingerprint" to detect loops.
It turns out that getting clever didn't help much here.
Computing the deltas and reusing that data did help.

Storing and only testing seen fingerprints (vs all possible combinations) make a huge difference!

### Day Twenty Three

I thought this was fairly simple, though my solution didn't feel super elegant.
Brute forcing, looking for a clique of size N, working from the largest group size N and down, seemed to make this plenty fast (vs trying to get the max of all possible cliques).

### Day Twelve Four

Another really challenging puzzle!
It took nearly 4 hours for part two.
I gave up, asked for help, and went the `dot` graphiv route with much reluctance.
I did a bunch of node analysis to rename nodes and make the diagram easier to read.
After AoC was over, I circled back and wrote a pretty decent solver.

### Day Twenty Five

Python's `zip()` for transpose was helpful here.
The off-by-one size in the description was confusing.
I originally counted and added.
At first, I thought the key much be an exact match, not a loose match.

I later switched to a coord map and used set operations to solve this (much simpler solution!).
