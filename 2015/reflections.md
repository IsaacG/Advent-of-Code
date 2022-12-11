# Day 1: Not Quite Lisp. Count Santa's floor level.

First day of AoC this year!
I forgot to set up my files and my template generator was broken.
That cost me 3 minutes.
This exercise was straight forward.

# Day 2: I Was Told There Would Be No Math. Compute wrapping materials.

Thank goodness for `itertools`, though I always take a couple of moments to figure out `combinations()` vs `permutations()` vs `products()`.

# Day 3: Perfectly Spherical Houses in a Vacuum. Track which houses get presents.

Tracking positions on a map.
Using complex numbers always makes my life so easy.

# Day 4: The Ideal Stocking Stuffer. MD5 mine for a good hash.

This was a bit slow to run since I did not optimize it, but it still ran fast enough.
Then I realized that the Python `hashlib` allows you to reuse partial hashes, which helped things along.

# Day 17: No Such Thing as Too Much. Count ways to fill containers.

`itertools.combinations()` made this exercise relatively trivial.
There was nothing too exciting here.

# Day 18: Like a GIF For Your Yard. Conway's Game of Life.

Thoughts:

* I should add maps to the parsing lib.
* This was relatively straight forward.
* It took me a while to realize I wasn't turning on the corners in the last case.
