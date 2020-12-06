#!/bin/python

import util


def count2(r):
  """Part 2: count num of chars found on all lines."""
  records = r.split()
  s = set(records.pop())
  while records:
    s &= set(records.pop())
  return len(s)


def count1(r):
  """Part 1: count the unique chars, joining all lines."""
  return len(set(r.replace('\n', '')))


def test():
  """Assert translate works."""
  records = 'abc\n\na\nb\nc\n\nab\nac\n\na\na\na\na\n\nb\n'.split("\n\n")
  assert 11 == sum(count1(r) for r in records)

  records = "\nabc\n\na\nb\nc\n\nab\nac\n\na\na\na\na\n\nb\n".split("\n\n")
  assert 6 == sum(count2(r) for r in records)


def main():
  test()
  records = util.load_data("\n\n")
  print(sum(count1(r) for r in records))
  print(sum(count2(r) for r in records))


if __name__ == '__main__':
  main()

# vim:ts=2:sw=2:expandtab
