#!/bin/python

import pathlib
import sys
from typing import Set


def prod_of_pair(pair_sum: int, data: Set[int]) -> int:
  vals = [i for i in data if (pair_sum - i) in data]
  if not vals:
    return 0
  if len(vals) == 2:
    return vals[0] * vals[1]
  raise ValueError(f'Found too many matches.')


def main():
  datafile = pathlib.Path(sys.argv[1])
  data = set(int(i) for i in datafile.read_text().split())
  print(prod_of_pair(2020, data))

  for n in data:
    subset = list(data)
    subset.remove(n)
    prod = prod_of_pair(2020 - n, subset)
    if prod:
      prod *= n
      print(prod)
      break
    
  

if __name__ == '__main__':
  main()
