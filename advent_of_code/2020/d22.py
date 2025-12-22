#!/usr/bin/env python
"""AoC Day 22: Crab Combat."""


def solve(data: list[str], part: int) -> int:
    """Return the outcome of combat."""
    return (part1 if part == 1 else part2)(data)


def part1(decks) -> int:
    """Simple Combat."""
    hands = decks
    # Keep playing while everyone has cards in hand.
    while all(hands):
        # Everyone plays a card.
        cards_played = [h.pop(0) for h in hands]
        # Find the player who played the highest card.
        winner = [i for i in (0, 1) if cards_played[i] == max(cards_played)][0]
        # Add the cards to hand, highest first.
        hands[winner].extend(sorted(cards_played, reverse=True))
    winning_hand = [h for h in hands if h][0]
    return sum((i + 1) * c for i, c in enumerate(winning_hand[::-1]))


def part2(decks) -> int:
    """Play Recursive Combat."""
    _, winning_hand = combat(decks)
    return sum((i + 1) * c for i, c in enumerate(winning_hand[::-1]))


def combat(hands) -> tuple[int, list[int]]:
    """Return the winner and the winning deck."""
    seen_f = set()
    seen = set()
    while all(hands):
        # This block is the most important line in this file in terms of runtime.
        combined = (hands[0][0], hands[0][-1], len(hands[0]), hands[1][0], hands[1][-1])
        full = 0
        # Needed for correctness for a few specific inputs but kills runtime.
        # full = tuple(hands[0] + [0] + hands[1])
        if combined in seen:
            if full in seen_f:
                return 0, hands[0]
        seen.add(combined)
        seen_f.add(full)

        # All cards have a unique value. Ties are not an issue.
        cards_played = [h.pop(0) for h in hands]

        if not all(len(h) >= c for h, c in zip(hands, cards_played)):
            # Not enough cards for recurse; use simple rules - highest card wins.
            winner = [i for i in (0, 1) if cards_played[i] == max(cards_played)][0]
        else:
            supercard = max(hands[0])
            if max(hands[1]) < supercard < sum(len(h) for h in hands):
                # jle`s supercard optimization.
                # Has major impact (~15x) on some inputs, very little on others.
                winner = 1
            else:
                # Recursive battle. Recurse when hand have enough cards.
                sub_hands = tuple(h[:c] for h, c in zip(hands, cards_played))
                winner = combat(sub_hands)[0]

        # Add the cards to the winner's hand. Make use of 0/1 as bool()s to
        # determine if the card order needs to be reversed.
        hands[winner].extend(reversed(cards_played) if winner else cards_played)

    # Assume either p1 ^ p2 is always true.
    for player, hand in enumerate(hands):
        if hand:
            return player, hand
    raise RuntimeError


def input_parser(puzzle_input: str):
    """Split the input into two decks."""
    return [
        [int(line) for line in deck.splitlines()[1:]]
        for deck in puzzle_input.split('\n\n')
    ]


SAMPLE = [
    """\
Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10""", """\
Player 1:
43
19

Player 2:
2
29
14"""]
TESTS = [
    (1, SAMPLE[0], 306),
    (2, SAMPLE[0], 291),
    (2, SAMPLE[1], 105),
]
