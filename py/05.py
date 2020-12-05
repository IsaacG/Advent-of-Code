#!/bin/python

import util


# Translate F to 0, B to 1, L to 0 and R to 1.
transmap = str.maketrans('FBLR', '0101')


def translate(s: str) -> int:
  """Translate to binary string then to int."""
  return int(s.translate(transmap), 2)


def test():
  """Assert translate works."""
  data = (
    ('BFFFBBFRRR', 567),
    ('FFFBBBFRRR', 119),
    ('BBFFBBFRLL', 820),
  )
  for a, b in data:
    assert translate(a) == b


def main():
  records = util.load_data()
  test()

  seats = {translate(r) for r in records}
  # Part one: max seat number
  print(max(seats))

  # Part two: find a gap of one between two seats.
  for s in seats:
    if (s + 1) not in seats and (s + 2) in seats:
      print(s+1)


if __name__ == '__main__':
  main()

# vim:ts=2:sw=2:expandtab
