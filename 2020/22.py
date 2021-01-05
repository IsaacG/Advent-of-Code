#!/usr/bin/env pypy

import typer
import copy
from typing import List, Tuple
from lib import aoc

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
10
""", """
Player 1:
43
19

Player 2:
2
29
14
"""]


class Day22(aoc.Challenge):

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
    return sum((i + 1) * c for i, c in enumerate(winning_hand[::-1]))

  def part2(self, decks) -> int:
    """Play Recursive Combat."""
    winner, winning_hand = self.combat(copy.deepcopy(decks))
    # print(f'Winner: {winner}')
    return sum((i + 1) * c for i, c in enumerate(winning_hand[::-1]))

  def combat(self, hands) -> Tuple[int, List[int]]:
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
        if supercard > max(hands[1]) and supercard < sum(len(h) for h in hands):
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
    raise RuntimeError

  def parse_input(self, puzzle_input: str):
    """Split the input into two decks."""
    return [
      [int(line) for line in deck.split('\n')[1:]]
      for deck in puzzle_input.split('\n\n')
    ]


if __name__ == '__main__':
  typer.run(Day22().run)

# vim:ts=2:sw=2:expandtab
