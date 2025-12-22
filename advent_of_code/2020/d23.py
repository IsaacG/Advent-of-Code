#!/usr/bin/env python
"""Day 23.

Crab Cups.
The small crab challenges you to a game! The crab is going to mix up some cups,
and you have to predict where they'll end up.
https://adventofcode.com/2020/day/23
"""

from __future__ import annotations


class Cup:
    """Linked list node."""

    next = None    # type: Cup

    def __init__(self, val: int, prev: Cup | None):
        """Create a Cup."""
        self.val = val
        if prev:
            prev.next = self

    def nodes(self):
        """Generate all nodes starting at `self`."""
        yield self
        c = self.next
        while c != self:
            yield c
            c = c.next


def play_rounds(cups: list[int], rounds: int) -> Cup:
    """Solve the cups game.

    Use a list of labels as a starting point.
    Run for `rounds` iteration.
    Return the cup labeled "1".
    """
    # Build a linked list of Cups with a map from label to Cup.
    mapping = {}
    cur: Cup | None = None
    for i in cups:
        cur = Cup(i, cur)
        mapping[i] = cur

    # Link the last and first cups, making the list circular.
    assert cur is not None
    cur.next = mapping[cups[0]]

    # Start the game with the "first" Cup.
    cur = mapping[cups[0]]
    highest = max(cups)
    for _ in range(rounds):
        # Destination label cannot be current or next three labels.
        not_valid_dest = (cur.val, cur.next.val, cur.next.next.val, cur.next.next.next.val)
        dest = cur.val
        while dest in not_valid_dest:
            # Try one lower value - with circular counting.
            dest = (dest - 1) or highest

        # Move 3 Cups from cur to dest.
        other = mapping[dest]

        # Update the cups with the next three cups shifted.
        # C => (j k l) => x y z D => e
        # C: current cup. D: destination cup. j k l are the three to move.
        # Update C.next = x; l.next = e; D.next = j
        taken = cur.next
        taken_end = cur.next.next.next
        taken_next = cur.next.next.next.next
        dest_plus_one = other.next

        cur.next = taken_next
        other.next = taken
        taken_end.next = dest_plus_one

        # Move to the next Cup.
        cur = cur.next

    return mapping[1]


def solve(data: list[int], part: int) -> int:
    """Play some rounds."""
    if part == 1:
        # Play for 100 rounds, return the list of Cups.
        one = play_rounds(data, 100)
        vals = [i.val for i in one.nodes()]
        return int("".join(str(i) for i in vals[1:]))

    # Extend the cups through 1M. Play for 10M rounds.
    data.extend(range(10, int(1e6) + 1))
    one = play_rounds(data, int(1e7))
    return one.next.val * one.next.next.val


PARSER = lambda x: [int(i) for i in x]
TESTS = [
    (1, '389125467', 67384529),
    (2, '389125467', 149245887792),
]
