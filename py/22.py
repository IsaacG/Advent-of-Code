#!/bin/pypy3

import aoc
import collections
import copy
import functools
import math
import re
from typing import Any, Callable, Dict, List, Tuple

SAMPLE = ["""\
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
10
""","""
Player 1:
43
19

Player 2:
2
29
14
"""]

class Day22(aoc.Challenge):

  SEP = '\n\n'
  TIMER_ITERATIONS = (1, 3)

  TESTS = (
    aoc.TestCase(inputs=SAMPLE[0], part=1, want=306),
    aoc.TestCase(inputs=SAMPLE[0], part=2, want=291),
    aoc.TestCase(inputs=SAMPLE[1], part=2, want=105),
  )

  def part1(self, decks) -> int:
    """Simple Combat."""
    hands = copy.deepcopy(decks)
    # Keep playing while everyone has cards in hand.
    while all(hands):
      # Everyone plays a card.
      cards_played = [h.pop(0) for h in hands]
      # Find the player who played the highest card.
      winner = [i for i in (0, 1) if cards_played[i] == max(cards_played)][0]
      # Add the cards to hand, highest first.
      hands[winner].extend(sorted(cards_played, reverse=True))
    winning_hand = [h for h in hands if h][0]
    return sum((i+1) * c for i, c in enumerate(winning_hand[::-1]))

  def part2(self, decks) -> int:
    """Play Recursive Combat."""
    winning_hand = self.combat(copy.deepcopy(decks))[1]
    return sum((i+1) * c for i, c in enumerate(winning_hand[::-1]))

  def combat(self, hands) -> Tuple[int, List[int]]:
    """Return the winner and the winning deck."""
    seen = set()
    while all(hands):
      # This line is the most important line in this file in terms of runtime.
      # We could just store the full list, but runtime suffers terribly.
      # This value seems to give the right results in good time, though I do not know
      # it necessarily works for all inputs.
      combined = (hands[0][0], hands[0][-1], len(hands[0]), hands[1][0], hands[1][-1])
      if combined in seen:
        return 0, hands[0]
      seen.add(combined)

      # All cards have a unique value. Ties are not an issue.
      cards_played = [h.pop(0) for h in hands]

      if not all(len(h) >= c for h, c in zip(hands, cards_played)):
        # Not enough cards for recurse; use simple rules - highest card wins.
        winner = [i for i in (0, 1) if cards_played[i] == max(cards_played)][0]
      else:
        supercard = max(hands[0])
        if supercard > max(hands[1]):
          # jle`s supercard optimization.
          # Has major impact (~15x) on some inputs, very little on others.
          winner = 1
        else:
          # Recursive battle. Recurse when hand have enough cards.
          sub_hands = tuple(h[:c] for h, c in zip(hands, cards_played))
          winner = self.combat(sub_hands)[0]

      # Add the cards to the winner's hand. Make use of 0/1 as bool()s to
      # determine if the card order needs to be reversed.
      hands[winner].extend(reversed(cards_played) if winner else cards_played)

    # Assume either p1 ^ p2 is always true.
    for player, hand in enumerate(hands):
      if hand:
        return player, hand

  def preparse_input(self, decks):
    """Split the input into two decks."""
    return [
      [int(l) for l in deck.split('\n')[1:]]
      for deck in decks
    ]


if __name__ == '__main__':
  Day22().run()

# vim:ts=2:sw=2:expandtab