#!/bin/python

import pathlib
import re
import sys
import util
from typing import List, Tuple


RE = re.compile('^([0-9]+)-([0-9]+) (.): (.*)$')


def parse(line: str) -> Tuple[int, int, str, str]:
   r = RE.match(line)
   mn, mx, char, passwd = r.groups()
   return int(mn), int(mx), char, passwd


def valid_a(line: str) -> bool:
   mn, mx, char, passwd = parse(line)
   match = len([1 for i in passwd if i == char])
   return mn <= match <= mx


def valid_b(line: str) -> bool:
   mn, mx, char, passwd = parse(line)
   return (passwd[mn - 1] == char) ^ (passwd[mx - 1] == char)
   return mn <= match <= mx


def part1(lines: List[str]) -> int:
  return len([1 for line in lines if valid_a(line)])


def part2(lines: List[str]) -> int:
  return len([1 for line in lines if valid_b(line)])


CONFIG = {
  'debug': False,
  'funcs': {1: part1, 2: part2},
  'tranform': str,
  'tests': (),
  'sep': '\n',
}


if __name__ == '__main__':
  util.run_day(CONFIG)

# vim:ts=2:sw=2:expandtab
