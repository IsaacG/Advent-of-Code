"""FlipFlop Codes, Puzzle 4: Magic Flowerstalk."""

import itertools
from lib import helpers, parsers


def solve(part: int, data: str) -> int:
    """Solve the parts."""
    # Remove the head and soil. Convert to L, R or empty.
    stalk = ["L" if "o-|" in line else "R" if "|-o" in line else "" for line in  data[3:-1]]

    if part == 1:
        # We only consider until 8/400 from the bottom.
        cut = 8 if len(stalk) == 16 else 400
        # Count leaves.
        return sum(leaf != "" for leaf in stalk[:-cut])

    # Compress the stalk, dropping empty segments.
    stalk = [i for i in stalk if i]

    # Part three: keep climbing the stalk while there are leaves.
    for worker_passes in itertools.count(start=1):
        current_side = ""
        side_switches = 0
        remaining = []
        for idx, leaf in enumerate(stalk):
            # On the first leaf or when switching sides...
            if not current_side or current_side != leaf:
                current_side = leaf
                side_switches += 1
            else:
                remaining.append(leaf)
        # Part two: stop after one pass and report switches, not including the first one.
        if part == 2:
            return side_switches - 1
        stalk = remaining
        if not stalk:
            return worker_passes


TEST_DATA = """\
 \\|/
 -@-
 /|\\
  |-o
o-|
o-|
  |-o
  |
o-|
  |-o
  |-o
o-|
o-|
  |
o-|
o-|
  |
o-|
  |-o
#####"""
WANT = [7, 6, 5]
TESTS = [(i, TEST_DATA, want) for i, want in enumerate(WANT, start=1)]

if __name__ == "__main__":
    helpers.run_solution(globals())
