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

## Day 08

I wasted some time since I forgot to reset steps=0 inside my `foreach start` loop. And then I used `/[A-Z]/` in p2 and apparent there are numbers in some node names :(
Though I'm not convinced my algorithm is right. Even if it does yield the right answer.
I was thinking I need to compute cycles to first (1)Z then all the step cycles from (1)Z to (n)Z for each start then try to find where those overlap
But ... hey! If each starting (1)A->(1)Z has exactly one path from (1)Z->(2)Z where both Z nodes are the same and are aligned with the instruction code and is the same length as (1)A->(1)Z then that works?

