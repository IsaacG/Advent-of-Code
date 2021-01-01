#!/usr/bin/env pypy

import asyncio
import collections
import functools
import math
import re
import typer
from typing import Any, Callable, Dict, List

import intcode
from lib import aoc


SAMPLE = ['1']


class Day09(intcode.Challenge):

  DEBUG = True

  TESTS = (
    aoc.TestCase(inputs=SAMPLE[0], part=1, want=0),
  )

  def part1(self, computer: intcode.Computer) -> int:
    return 0


if __name__ == '__main__':
  typer.run(Day09().run)

# vim:ts=2:sw=2:expandtab
