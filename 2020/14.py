#!/usr/bin/env pypy
"""Day 14. Write data to memory?"""

import typer
from lib import aoc
from typing import Callable, Dict, List, Tuple


SAMPLE = ["""\
mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0
""", """\
mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1
"""]


class Day14(aoc.Challenge):
  """Solve Day 14.

  Both parts do similar read, track mask, apply write.
  They only differ in how a "write" is applied.
  """

  TESTS = (
    aoc.TestCase(inputs=SAMPLE[0], part=1, want=165),
    aoc.TestCase(inputs=SAMPLE[1], part=2, want=208),
  )

  def part1(self, lines: List[Tuple[str, ...]]) -> int:
    return self.solve(lines, self.write1)

  def part2(self, lines: List[Tuple[str, ...]]) -> int:
    return self.solve(lines, self.write2)

  def solve(self, lines: List[Tuple[str, ...]], mem_writer: Callable[[str, int, int], None]) -> int:
    """Read input. Track mask. Apply writes with the mem_writer."""
    self.mem = {}  # type:Dict[int, int]
    mask = ''
    for (op, val) in lines:
      if op == 'mask':
        mask = val
      else:
        mem_writer(mask, int(op[4:-1]), int(val))
    return sum(self.mem.values())

  def write1(self, mask: str, address: int, value: int):
    """Use the mask to modify the value then write it to memory.

    Replace X=>0 then do a bool-OR to apply 1's
    Replace X=>0 then do a bool-OR to apply 1's
    """
    m0 = int(mask.replace('X', '0'), 2)
    m1 = int(mask.replace('X', '1'), 2)
    self.mem[address] = (value | m0) & m1

  def write2(self, mask: str, address: int, value: int):
    """Use the mask to generate multiple addresses to write the value to."""
    # 36-bit binary string of the address.
    padded_addr = f'{address:036b}'

    # Pass through address on mask=0, otherwise apply mask value.
    masked_addr = [b if a == '0' else a for a, b in zip(mask, padded_addr)]

    # If there are 3 X's, we need to write to 2^3 addresses, i.e.
    # there are 2^3 possible sunstitutes for those X's.
    # For each possible substitute for the X's,
    # make a binary string and replace the X's with the 0|1.
    count = sum(True for i in masked_addr if i == 'X')
    for i in range(2**count):
      # count-length binary string. 0 => 000 => [0, 0, 0]
      substitute = list(format(i, ('0%db' % count)))
      # Rebuild the address, replacing 'X' with a char from substitute.
      final_addr = [substitute.pop(0) if a == 'X' else a for a in masked_addr]
      addr = int("".join(final_addr), 2)
      self.mem[addr] = value

  def parse_input(self, puzzle_input: str) -> List[Tuple[str, ...]]:
    return [tuple(line.split(' = ')) for line in puzzle_input.split('\n')]


if __name__ == '__main__':
  typer.run(Day14().run)

# vim:ts=2:sw=2:expandtab
