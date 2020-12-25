#!/bin/pypy3
"""Brute force solve Diffie Hellman key exchange."""

import aoc
import typer
from typing import List

MODULO = 20201227


class Day25(aoc.Challenge):
  """Day 25. Brute force solve Diffie Hellman key exchange."""

  TRANSFORM = int

  TESTS = (
    aoc.TestCase(inputs="5764801\n17807724\n", part=1, want=14897079),
  )

  def transform(self, subject: int, loop_counter: int) -> int:
    """Apply the transform function."""
    num = 1
    for i in range(loop_counter):
      num = (num * subject) % MODULO
    return num

  def force(self, w0, w1):
    """Brute force the loop_counter to "solve" Diffie Hellman."""
    attempt = 0
    num = 1
    while num != w0 and num != w1:
      attempt += 1
      num = (num * 7) % MODULO
    return attempt, 0 if num == w0 else 1

  def part1(self, pubkeys: List[str]) -> int:
    """Brute force the key.

    Brute force both public keys to find the smaller loop counter.
    Use the loop counter to transform the *other* public key.
    """
    loop_counter, key_index = self.force(*pubkeys)
    return self.transform(pubkeys[1 - key_index], loop_counter)

  def part2(self, pubkeys: List[str]) -> int:
    """No part 2."""
    return 0


if __name__ == '__main__':
  typer.run(Day25().run)

# vim:ts=2:sw=2:expandtab
