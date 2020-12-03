#!/bin/python

import util


def tree_count(grid, x_step, y_step) -> int:
  count = 0
  x = 0
  for y in range(0, len(grid), y_step):
    if grid[y][x % len(grid[0])] == '#':
      count += 1
    x += x_step
  return count


def main():
  grid = util.load_data()

  print(tree_count(grid, 3, 1))

  prod = 1
  for x_step, y_step in ((1,1), (3,1), (5,1), (7,1), (1,2)):
    prod *= tree_count(grid, x_step, y_step)
  print(prod)
    


if __name__ == '__main__':
  main()

# vim:ts=2:sw=2:expandtab
