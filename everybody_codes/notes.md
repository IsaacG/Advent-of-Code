# Notes

## Event 2025 Quest 8

### Optimize part 3: cumulative chords.

Part 3 has 256 nails (n) and ~4100 lines.
Finding the most cuts does require testing `n*n/2` possible cuts.
The brute force approach of iterating through every line for every cut is slow (~20 seconds): `O(n*n/2*lines)`.
A much faster approach is to compute the cumulative strings starting at every nail. This lets us test roughly `O(n*n/2*n/2)` cases.
`lines / (n/2) ~= 32` for 32x faster.

For any cut `a-b`, we can measure the lines cut by considering all the lines that start at nail `i` between `a` and `b` and cross to the other side of `a` and `b` to nail `j`.
Rather than repeatedly summing up all the lines starting at `i` and ending at all values of `j`, we can instead count the cumulative lines starting at nail `i` and ending at nails `[i+1, i+2, ..., a, ..., b]`.
We can then use the cumulative lines `cumulative[i][b] - cumulative[i][a+1]` to compute how many lines start at `i` and end on the other side of the `a-b` line.
