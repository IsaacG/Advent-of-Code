#!/bin/python
"""Advent of Code, Day 22."""
import collections
PARSER = str.splitlines


def solve(data: list[str], part: int, testing: bool) -> int:
    """Return a card after shuffling."""
    return (part1 if part == 1 else part2)(data, testing)


def part1(data: list[str], testing: bool) -> int:
    """Track the position of a card through some shuffles."""
    want_card = 0 if testing else 2019
    deck_size = 10 if testing else 10007
    # cards = collections.deque(range(deck_size))
    # position = list(cards).index(want_card)
    position = want_card
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


def part2(data: list[str], testing: bool) -> int:
    """Perform many shuffles.

    Code taken from https://github.com/Dementophobia/advent-of-code-2019/blob/master/2019_22_p2.py

    See also,
    https://www.reddit.com/r/adventofcode/comments/ee0rqi/comment/fbwp0r0/
    https://www.reddit.com/r/adventofcode/comments/ee0rqi/comment/fbnkaju/
    https://www.reddit.com/r/adventofcode/comments/ee0rqi/comment/fbnifwk/
    """
    del testing
    position = 2020
    size = 119315717514047
    iterations = 101741582076661

    addi, multi = 0, 1
    for operation in data:
        if operation == "deal into new stack":
            multi *= -1
            addi  += multi
        elif operation.startswith("cut"):
            n = int(operation.split()[-1])
            addi  += n * multi
        elif operation.startswith("deal with increment"):
            n = int(operation.split()[-1])
            multi *= pow(n, -1, size)

    all_multi = pow(multi, iterations, size)
    all_addi = addi * (1 - pow(multi, iterations, size)) * pow(1 - multi, -1, size)

    return (position * all_multi + all_addi) % size


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
    (1, SAMPLE[1], 1),
    (1, SAMPLE[2], 2),
    (1, SAMPLE[3], 7),
]
