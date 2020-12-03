#!/bin/python

import pathlib
import re
import sys
from typing import Tuple


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


def main():
  datafile = pathlib.Path(sys.argv[1])
  data = datafile.read_text().split('\n')[:-1]
  print(len([1 for line in data if valid_a(line)]))
  print(len([1 for line in data if valid_b(line)]))


if __name__ == '__main__':
  main()

# vim:ts=2:sw=2:expandtab
