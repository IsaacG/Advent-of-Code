TODO
====

Comuter logic is shared across days 12, 23, 25. Should be shared code.

Day 19
======

Brute force does not work well here for large numbers.
For smaller numbers, it works just fine!

```python
for starting_size in range(1, 100):
    size = starting_size
    circle = list(range(size))
    cur = 0
    for step in range(parsed_input - 1):
        target = (cur + size // 2) % size
        del circle[target]
        size -= 1
        if target > cur:
            cur += 1
        if cur == size:
            cur = 0
    got = circle[0] + 1
    print(f"{starting_size}: {got}")
```

Looking at the results for smaller numbers, there is a clear pattern.
Showing the starting circle size and the winner:

```python
1: 1
2: 1
3: 3
4: 1   # Restart from 1, count by 1
5: 2
6: 3   # When M == N / 2, switch to counting by 2
7: 5
8: 7
9: 9   # Restart when M == N
10: 1  # Start over, count by 1
11: 2
...   
17: 8
18: 9  # Until M == N/2, then switch to counting by 2
19: 11
20: 13
...
26: 25
27: 27 # When M == N, restart.
28: 1
```

While it is not very pretty, it is quite fast!

```python
def part2(self, parsed_input: InputType) -> int:
    stop = parsed_input - 1
    size = 1
    while True:
        counter = 1
        while counter <= size // 2:
            if size == stop:
                return counter
            size += 1
            counter += 1
        while counter <= size + 1:
            if size == stop:
                return counter
            size += 1
            counter += 2
```
