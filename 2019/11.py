#!/usr/bin/env python
"""Day 11: Space Police

Implement a robot with inputs/outputs that connects to an Intcode Computer.
This robot got camera inputs and motor outputs (paint, turn, move).
"""

import asyncio
import collections

from typing import Set
import intcode


BLACK, WHITE = 0, 1


class HullPaintingRobot:
  """Hull Painting Robot.

  Driven by an Intcode computer. Sends camera signals to the computer
  and receives motor instructions from the computer.
  """

  # Polar rotation. 0 for 90deg CCW. 1 for 90deg CW.
  ROT = {0: 1j, 1: -1j}

  def __init__(self, start_color: int, camera: asyncio.Queue, motors: asyncio.Queue):
    self.camera = camera
    self.motors = motors
    self.pos = 0 + 0j
    self.direction = 1j  # up
    self.hull_color = collections.defaultdict(lambda: BLACK)
    self.tiles_painted = set()  # type: Set[complex]
    self.hull_color[self.pos] = start_color

  async def run(self):
    """Run the robot forever, or until cancelled."""
    while True:
      # Input the current tile color to the camera.
      await self.camera.put(self.hull_color[self.pos])
      # Read the color to paint the current tile.
      new_color = await self.motors.get()
      self.hull_color[self.pos] = new_color
      self.tiles_painted.add(self.pos)
      # Read the turn direction. Update and move.
      turn = await self.motors.get()
      self.direction *= self.ROT[turn]
      self.pos += self.direction


class Day11(intcode.Challenge):

  TESTS = ()

  async def run_bot(self, computer: intcode.Computer, start_color: int) -> HullPaintingRobot:
    """Run a robot with the computer."""
    camera = asyncio.Queue()  # type: asyncio.Queue
    motors = asyncio.Queue()  # type: asyncio.Queue
    # Create and run (async) a robot with the IO.
    bot = HullPaintingRobot(start_color, camera, motors)
    bot_task = asyncio.create_task(bot.run())
    # Run a computer with the same IO. Wait for completion.
    await computer.run(io=(camera, motors))
    # Kill the bot and return it.
    bot_task.cancel()
    return bot

  def part1(self, computer: intcode.Computer) -> int:
    bot = asyncio.run(self.run_bot(computer, BLACK))
    return len(bot.tiles_painted)

  def part2(self, computer: intcode.Computer) -> int:
    bot = asyncio.run(self.run_bot(computer, WHITE))

    # Convert the hull tiles to an image.
    hull = bot.hull_color
    x_vals = [int(pos.real) for pos in hull]
    y_vals = [int(pos.imag) for pos in hull]

    image = []
    for y in range(max(y_vals), min(y_vals) - 1, -1):
      row = ''
      for x in range(min(x_vals), max(x_vals) + 1):
        row += ' ' if hull[x + y * 1j] == BLACK else '█'
      image.append(row)

    # Displays the actual solution.
    # print('\n'.join(image))
    # Meaningless number to use in the solutions file.
    return self.mult(sum(True for c in row if c != ' ') for row in image)
