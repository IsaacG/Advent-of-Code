"""The Overflowing Cistern

You are managing a series of water tanks in a castle.
There are n tanks arranged in a row, each with a known capacity (integer).
Initially, each tank contains some water (non-negative integer, not exceeding capacity).
Each day, you pour a fixed amount of water into the leftmost tank (tank 0).
The water flows according to these rules:

* Pour the entire day's amount into tank 0.
* Then, starting from leftmost to rightmost, check each tank: if its water level exceeds its capacity, the excess is transferred immediately to the tank to its right.
  If there is no tank to the right, the excess is lost.
  Because we process left to right, any overflow caused by a transfer will be handled when we reach that tank later in the same pass.
  No further passes are needed.

After the day's water distribution settles, record the water levels of all tanks as that day's state.

Your task: Given an array heights (initial water levels), an array caps (capacities), and an array pours (list of amounts poured each day, in order), simulate the process and return the history of states:

Return an object { "n": n, "frames": [...] } where frames is a flat array of all states concatenated in order: first the initial state (before any pours), then state after day 1, after day 2, etc.
Each state is a block of n integers (tank water levels).
The total number of frames is 1 + len(pours).
All values are integers.

Constraints: 3 <= n <= 8, capacities 1..20, initial heights <= capacity, each pour 0..20, number of pours <= 10.
"""

def waterTanks(heights, caps, pours):
    """Return {"n": ..., "frames": [...]}."""
    frames = heights.copy()
    first_available = 0
    num_tanks = len(heights)
    for pour in pours:
        while pour and  first_available < num_tanks:
            amount = min(caps[first_available] - heights[first_available], pour)
            heights[first_available] += amount
            pour -= amount
            if caps[first_available] == heights[first_available]:
                first_available += 1
        frames.extend(heights)
    return {"n": num_tanks, "frames": frames}

assert waterTanks([0, 0, 0], [5, 3, 4], [4, 2, 1]) == {"n": 3, "frames": [0, 0, 0, 4, 0, 0, 5, 1, 0, 5, 2, 0]}
assert waterTanks([1, 2, 3, 4, 5], [5, 5, 5, 5, 5], []) == {"n": 5, "frames": [1, 2, 3, 4, 5]}
assert waterTanks([0, 0, 0, 0, 0, 0], [2, 2, 2, 2, 2, 2], [3, 3, 3, 3, 3]) == {"n": 6, "frames": [0, 0, 0, 0, 0, 0, 2, 1, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 2, 2, 2, 2, 1, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]}
assert waterTanks([0, 0, 0, 0], [2, 2, 2, 9], [9]) == {"n": 4, "frames": [0, 0, 0, 0, 2, 2, 2, 3]}
