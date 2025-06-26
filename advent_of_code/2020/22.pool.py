#!/bin/python3

import pathlib

import d22


class Day22(d22.Day22):
  pass


if __name__ == '__main__':
  day = Day22()
  data = pathlib.Path('data/22.pool.txt').read_text().strip()
  hands = data.split('\n\n')
  inputs = [[int(i) for i in h.strip().split('\n')[1:]] for h in hands]
  res = [day.part2(inputs[i * 2:i * 2 + 2]) for i in range(15)]
  print(res)


# vim:ts=2:sw=2:expandtab
