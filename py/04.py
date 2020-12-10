#!/bin/python

import sys
import util
import re

from typing import List

REQUIRED_FIELDS = {
  'byr',
  'iyr',
  'eyr',
  'hgt',
  'hcl',
  'ecl',
  'pid',
  # 'cid',
}
YEAR_CHECKS = {
  ('byr', 1920, 2002),
  ('iyr', 2010, 2020),
  ('eyr', 2020, 2030),
}
HEIGHT_IN_RE = re.compile('^([0-9]+)in$')
HEIGHT_CM_RE = re.compile('^([0-9]+)cm$')
HAIR_RE = re.compile('^#[0-9a-f]{6}$')
PID_RE = re.compile('^[0-9]{9}$')
EYE_CLRS = {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'}


def valid1(record):
  fields = {f.split(':', 1)[0] for f in record.split()}
  return fields >= REQUIRED_FIELDS

def part1(lines: List[str]) -> int:
  """Check the record has all the required fields."""
  return len([1 for i in lines if valid1(i)])


def range_check(s: str, mn: int, mx: int) -> bool:
  """Check a numeric str in in a range."""
  return mn <= int(s) <= mx


def valid2(record) -> bool:
  """Validate all the fields.

  byr (Birth Year) - four digits; at least 1920 and at most 2002.
  iyr (Issue Year) - four digits; at least 2010 and at most 2020.
  eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
  hgt (Height) - a number followed by either cm or in:
  If cm, the number must be at least 150 and at most 193.
  If in, the number must be at least 59 and at most 76.
  hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
  ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
  pid (Passport ID) - a nine-digit number, including leading zeroes.
  cid (Country ID) - ignored, missing or not.
  """
  if not valid1(record):
    return False

  data = {f.split(':', 1)[0]: f.split(':', 1)[1] for f in record.split()}

  for k, mn, mx in YEAR_CHECKS:
    if not range_check(data[k], mn, mx):
      return False

  if (m := HEIGHT_IN_RE.match(data['hgt'])) and range_check(m.group(1), 59, 76):
    pass
  elif (m := HEIGHT_CM_RE.match(data['hgt'])) and range_check(m.group(1), 150, 193):
    pass
  else:
    return False

  if not HAIR_RE.match(data['hcl']):
    return False

  if not PID_RE.match(data['pid']):
    return False

  if not data['ecl'] in EYE_CLRS:
    return False

  return True


def part2(lines: List[str]) -> int:
  return len([1 for i in lines if valid2(i)])


CONFIG = {
  'debug': False,
  'funcs': {1: part1, 2: part2},
  'tranform': str,
  'tests': (),
  'sep': '\n\n',
}


if __name__ == '__main__':
  util.run_day(CONFIG)

# vim:ts=2:sw=2:expandtab
