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
Auto-parsed days: 01, 02, 04, 06, 08, 10, 11

I also introduced a new `aoc.CoordinateParser()` which returns an `aoc.Map`.
This was very handy this year and deprecated the old `Board` code.
Days using this new parser: 04, 06, 08, 10

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

### Day Seven

Someone on IRC noticed working from the end (right) you can prune much more aggresively, resulting in a significantly faster solution!

### Day Eight

This is when I introduced the CoordinateParser and retrofitted it into prior days/years.

### Day Nine

I felt there much be a better approach here with a `heapq` or `PriorityQueue` but wasn't able to figure it out myself.
I saw someone else had 9 `heapqs` groups by hole size and I was able to copy that idea, for large speed improvements.

### Day Ten

This day, I accidentally solved part two first.

### Day Eleven

This one was rough until I worked out how to solve it with dynamic programming, then it became very simple!
DP also brough runtimes down from "ridiculous" to fast.

### Day N
