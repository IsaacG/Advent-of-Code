#!/bin/python

import collections
import util
import re
from typing import List, Dict
Rules = Dict[str, Dict[str, int]]

RE_CONTENTS = re.compile('^([0-9]*) (.*) bags?')
TARGET = 'shiny gold'


def test():
  """Assert solution works."""
  rules = parse_rules(SAMPLE1.split("\n")[:-1])
  assert 4 == part1(rules)

  rules = parse_rules(SAMPLE2.split("\n")[:-1])
  assert 126 == part2(rules), part2(rules)


def parse_rules(data: List[str]) -> Rules:
  """Parse the input data into structured data."""
  rules = {}
  for line in data:
    # (red) bags contain (2 purple bags, 3 yellow bags.)
    outer, contains = line.split(' bags contain ')
    rules[outer] = {}
    # (red) bags contain (no other bags.)
    if contains == 'no other bags.':
      continue
    # (2 purple bags), (3 yellow bags.)
    for c in contains.split(', '):
      m = RE_CONTENTS.search(c)
      # rules['red'] = {'purple': 2, 'yellow': 3}
      rules[outer][m.group(2)] = int(m.group(1))
  return rules


def part1(rules: Rules) -> int:
  """How many colors can contain shiny gold bags?"""
  expanded = collections.defaultdict(set)
  for o, i in rules.items():
    if not i:
      continue
    queued = set(i.keys())
    while queued:
      j = queued.pop()
      if not j:
        continue
      expanded[o].add(j)
      if rules[j]:
        queued.update(rules[j])
  return len([i for i in expanded.values() if TARGET in i])


def part2(rules: Rules) -> int:
  """How many bags are inside a shiny gold bag?

  Dynamic programming!
  """
  cache = {}
  def num_inside(color):
    """How many bags do we have, starting at `color`?"""
    if color not in cache:
      # For each item inside this bag, sum the count (k) * [ 1 (for the bag self) + contends ]
      cache[color] = sum(k * (1 + num_inside(j)) for  j, k in rules[color].items())
    return cache[color]

  return num_inside(TARGET)


def main():
  test()
  data = util.load_data("\n")
  rules = parse_rules(data)
  print(part1(rules))
  print(part2(rules))


SAMPLE1 = """\
light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.
"""

SAMPLE2 = """\
shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags.
"""


if __name__ == '__main__':
  main()

# vim:ts=2:sw=2:expandtab