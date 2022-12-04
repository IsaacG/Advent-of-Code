#!/usr/bin/env python
"""Day 19. Regex building."""

import typer
from lib import aoc
import re
from typing import Dict, List, Tuple

import data

SAMPLE = data.D19
TEXT_RE = re.compile(r'"(.*)"')


class Day19(aoc.Challenge):

  TESTS = (
    aoc.TestCase(inputs=SAMPLE[0], part=1, want=2),
    aoc.TestCase(inputs=SAMPLE[1], part=2, want=12),
  )

  def generate_regexes(self, raw_rules: Dict[int, str]) -> Dict[int, re.Pattern]:
    """Resolve the input data to a set of regexps."""
    regexps = {}
    raw_rules = dict(raw_rules)
    # Resolve rules until all done.
    while raw_rules:
      old_len = len(raw_rules)
      for rule_num, rule_txt in list(raw_rules.items()):
        # 1: "a"
        m = TEXT_RE.fullmatch(rule_txt)
        if m:
          regexps[rule_num] = m.group(1)
          del raw_rules[rule_num]
        # Check if all rule components have already been resolved.
        elif all(int(num) in regexps for part in rule_txt.split(' | ') for num in part.split(" ")):
          composed = []
          # 1: 2 3 | 4 5
          # Split on "|" and solve each part, rejoining with "|".
          # i.e. generate 23|45 with each number resolved to their rule.
          for part in rule_txt.split(' | '):
            composed.append("".join(regexps[int(num)] for num in part.split(" ")))
          regexps[rule_num] = '(?:' + '|'.join(composed) + ')'
          del raw_rules[rule_num]
      # Assert we're making progress, i.e. not in an infinite loop
      assert len(raw_rules) != old_len
    return {k: re.compile(v) for k, v in regexps.items()}

  def part2(self, data: Tuple[Dict[int, str], List[str]]) -> int:
    """Find the num of lines that match the regex-like rules.

    However, handle circular rules. Relevant rules:
    0: 8 11
    8: 42 | 42 8
    11: 42 31 | 42 11 31

    Note:
      r8  == r42+
      r11 == r42{n}r31{m}, n == m
      r0  == r42+r42{n}r31{n}
          == r42{n}r31{m}, n > m
      Manually generate a rule, (r42+)(r31+) and check if match_count(r42) > match_count(r31).
    """
    raw_rules, inputs = data
    # Drop these rules. We well hand-craft them.
    for i in (0, 8, 11):
      if i in raw_rules:
        del raw_rules[i]
    regexps = self.generate_regexes(raw_rules)

    r42 = regexps[42]
    r31 = regexps[31]
    r0 = re.compile(r'(%s{2,})(%s+)' % (r42.pattern, r31.pattern))

    matches = sum(
      True
      for inp in inputs
      if any(i.fullmatch(inp) for i in regexps.values())
    )
    # r0 needs to match r42{n}r31{m} where n>m
    r0_matches = 0
    for inp in inputs:
      # Prevent double counting? Not needed for this input.
      # If needed, we could skip prior-matching.
      m = r0.fullmatch(inp)
      if m:
        c1 = len(re.findall(r42, m.group(1)))
        c2 = len(re.findall(r31, m.group(2)))
        if c1 > c2:
          r0_matches += 1
    return matches + r0_matches

  def part1(self, data: Tuple[Dict[int, str], List[str]]) -> int:
    """Find the num of lines that match the regex-like rules."""
    raw_rules, inputs = data
    # Map input to regexps.
    regexps = self.generate_regexes(raw_rules).values()
    # Count the lines that match.
    return sum(
      True
      for inp in inputs
      if any(i.fullmatch(inp) for i in regexps)
    )

  def input_parser(self, puzzle_input: str):
    """Parse the two input blocks."""
    rules_raw, strings = puzzle_input.split('\n\n')
    rules = {int(line.split(': ')[0]): line.split(': ')[1] for line in rules_raw.split('\n')}
    return rules, strings.split('\n')


if __name__ == '__main__':
  typer.run(Day19().run)

# vim:ts=2:sw=2:expandtab
