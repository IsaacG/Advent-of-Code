#!/bin/pypy3

import aoc
import collections
import functools
import math
import re
from typing import Any, Callable, Dict, List

SAMPLE = ["""\
0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb
""","""
42: 9 14 | 10 1
9: 14 27 | 1 26
10: 23 14 | 28 1
1: "a"
11: 42 31
5: 1 14 | 15 1
19: 14 1 | 14 14
12: 24 14 | 19 1
16: 15 1 | 14 14
31: 14 17 | 1 13
6: 14 14 | 1 14
2: 1 24 | 14 4
0: 8 11
13: 14 3 | 1 12
15: 1 | 14
17: 14 2 | 1 7
23: 25 1 | 22 14
28: 16 1
4: 1 1
20: 14 14 | 1 15
3: 5 14 | 16 1
27: 1 6 | 14 18
14: "b"
21: 14 1 | 1 14
25: 1 1 | 1 14
22: 14 14
8: 42
26: 14 22 | 1 20
18: 15 15
7: 14 5 | 1 21
24: 14 1

abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
bbabbbbaabaabba
babbbbaabbbbbabbbbbbaabaaabaaa
aaabbbbbbaaaabaababaabababbabaaabbababababaaa
bbbbbbbaaaabbbbaaabbabaaa
bbbababbbbaaaaaaaabbababaaababaabab
ababaaaaaabaaab
ababaaaaabbbaba
baabbaaaabbaaaababbaababb
abbbbabbbbaaaababbbbbbaaaababb
aaaaabbaabaaaaababaa
aaaabbaaaabbaaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
babaaabbbaaabaababbaabababaaab
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba
"""]


class Day19(aoc.Challenge):

  TRANSFORM = str
  SEP = '\n\n'

  TESTS = (
    # aoc.TestCase(inputs=SAMPLE[0], part=1, want=2),
    aoc.TestCase(inputs=SAMPLE[1], part=2, want=12),
  )

  def part2(self, lines: List[str]) -> int:
    rules = set(lines[0].split('\n'))
    rules.remove('8: 42')
    rules.remove('11: 42 31')
    rules.add('8: 42 | 42 8')
    rules.add('11: 42 31 | 42 11 31')
    rd = {}
    while len(rules) > 3:
      l = len(rules)
      new_matches = set()

      for i in rules:
        n, v = i.split(": ")
        if v[0] == '"' and v[2] == '"':
          rd[n] = v[1]
          new_matches.add(i)
        elif all(rn in rd for part in v.split(' | ') for rn in part.split(" ")):
          composed = []
          c = ""
          for  part in v.split(' | '):
            composed.append("".join(rd[rn] for rn in part.split(" ")))
          rd[n] = '(?:' + '|'.join(composed) + ')'
          new_matches.add(i)
      rules = rules - new_matches
      assert len(rules) != l, rules

    ext = '^(%s{2,})(%s+)$' % (rd['42'], rd['31'])

    matchs = [
      inp
      for inp in set(lines[1].split('\n'))
      if any(re.match('^%s$' % i, inp) for i in rd.values())
    ]
    ec = 0
    for inp in set(lines[1].split('\n')):
      if inp in matchs:
        continue
      m = re.match(ext, inp)
      if m:
        c1 = len(m.group(1)) / len(rd['42'])
        c2 = len(m.group(2)) / len(rd['31'])
        if c1 > c2:
          ec += 1
    return len(matchs) + ec
        

  def part1(self, lines: List[str]) -> int:
    rules = set(lines[0].split('\n'))
    rd = {}
    while rules:
      l = len(rules)
      new_matches = set()

      for i in rules:
        n, v = i.split(": ")
        if v[0] == '"' and v[2] == '"':
          rd[n] = v[1]
          new_matches.add(i)
        elif all(rn in rd for part in v.split(' | ') for rn in part.split(" ")):
          composed = []
          c = ""
          for  part in v.split(' | '):
            composed.append("".join(rd[rn] for rn in part.split(" ")))
          rd[n] = '(' + '|'.join(composed) + ')'
          new_matches.add(i)
      rules = rules - new_matches
      assert len(rules) != l, l
    
    return sum(
      True
      for inp in set(lines[1].split('\n'))
      if any(re.match('^%s$' % i, inp) for i in rd.values())
    )

    


  def preparse_input(self, x):
    return x


if __name__ == '__main__':
  Day19().run()

# vim:ts=2:sw=2:expandtab
