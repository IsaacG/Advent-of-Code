#!/bin/python
"""Advent of Code, Day 22."""
# https://www.reddit.com/r/adventofcode/comments/ee0rqi/comment/fbwp0r0/

import collections
PARSER = str.splitlines


def solve(data: list[str], part: int, testing: bool) -> int:
    """Return a card after shuffling."""
    want_card = 0 if testing else 2019 if part == 1 else 2020
    deck_size = 10 if testing else 10007 if part == 1 else 119315717514047
    # cards = collections.deque(range(deck_size))
    # position = list(cards).index(want_card)
    position = want_card
    for _ in range(1 if part == 1 else 101741582076661):
        for cmd in data:
            if cmd == "deal into new stack":
                # cards.reverse()
                position = deck_size - 1 - position
            elif cmd.startswith("cut"):
                n = int(cmd.split()[-1])
                # cards.rotate(-n)
                position = (position - n) % deck_size
            elif cmd.startswith("deal with increment"):
                n = int(cmd.split()[-1])
                # new_cards = [0] * deck_size
                # for i, card in enumerate(cards):
                #     new_cards[(i * n) % deck_size] = card
                # cards = collections.deque(new_cards)
                position = (position * n) % deck_size

    return position


SAMPLE = [
    """\
deal with increment 7
deal into new stack
deal into new stack""",
    """\
cut 6
deal with increment 7
deal into new stack""",
    """\
deal with increment 7
deal with increment 9
cut -2""",
    """\
deal into new stack
cut -2
deal with increment 7
cut 8
cut -4
deal with increment 7
cut 3
deal with increment 9
deal with increment 3
cut -1""",
]
TESTS = [
    (1, SAMPLE[0], 0),
    (1, SAMPLE[1], 3),
    (1, SAMPLE[2], 6),
    (1, SAMPLE[3], 9),
]
