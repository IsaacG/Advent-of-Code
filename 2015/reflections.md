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
* Tracking every cell is slow; switch to just tracking the lights which are on.
  That brings runtime down from 12s to 2s.

Library changes:

* New `BitmapParser`
* New `Board.corners`
* New `Board.neighbor_vals`

# Day 19: Medicine for Rudolph.

For part 1, it's simple enough to use sets and simply brute force it.

Part 2 has me stumped.

# Day 20: Infinite Elves and Infinite Houses.

I first attempted to generate the first million primes and use those to generate all the factors of every house.
By taking all combinations of factors, multiplying then summing, you can derive the number of items at a house.

That approach wasn't working great so I switched to something akin to the [Sieve of Eratosthenes](https://en.wikipedia.org/wiki/Sieve_of_Eratosthenes) which solves part 1 is 5.8s and part 2 in 2.9s using arbitrary upper limits.

Todo: [read this Reddit comment](https://www.reddit.com/r/adventofcode/comments/po1zel/comment/hd1esc2/) for a faster approach.
Maybe read other comments on that post for other ideas.

# Day 21: RPG Simulator 20XX. Compute the costs to win a battle.

This exercise was relatively straight forward.
It involved simply trying all combinations of items.
The hardest bit might be parsing the items or figuring out how to add "None" items.

# Day 22: Wizard Simulator 20XX. Pick the best spells to cast to beat the boss.

Part one was fun and slightly challenging but not too bad.
Part two gave me a very rough time.
I ended up asking for help and glguy noticed my `valid_moves` had a bug.
I was checking if effects timers are zero to exclude certain spells.
However, if the timer is at 1, the timer will become 0 at the start of the turn and the spell would be a valid move!

I also naively assumed states aren't likely to repeat.
leftylink questioned that assumption, which I failed to do.
Adding state checking reduced solve times from 8s/18ms to 500ms/750ms!
State checking didn't even require a whole lot of code change.

# Day 23: Opening the Turing Lock. Emulate a simple CPU.

Pretty straight forward.
`match case` is handy for this.
Part 2 held nothing surprising.

# Balance numbers into groups with contraints.

Relatively straight forward, asking for a `combinations()` which meets constraints.
The only tricky bit might be to increment the group sizes sequentially.
