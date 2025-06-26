#!/usr/bin/env python
"""Day 13: Care Package

Play the Pong arcade game.
"""

import asyncio
from typing import Dict, Tuple

import intcode


# Tiles
EMPTY = 0
WALL = 1
BLOCK = 2
PADDLE = 3
BALL = 4
SCORE = (-1, 0)

# Drawing the screen.
CHARS = {
  EMPTY: ' ',
  WALL: '█',
  BLOCK: '#',
  PADDLE: '=',
  BALL: 'O',
}


class Arcade:
  """The Arcade system."""

  def __init__(self, joystick: asyncio.Queue, video: asyncio.Queue, computer: intcode.Computer):
    self.video = video
    self.joystick = joystick
    self.screen = {}  # type: Dict[Tuple[int, int], int]
    self.computer = computer
    self.ball = (0, 0)
    self.paddle = (0, 0)

  async def draw(self):
    """Draw the screen. Size is hard coded because I'm lazy."""
    for y in range(20):
      for x in range(40):
        print(CHARS[self.screen[(x, y)]], end='')
      print()
    print()
    # For easier visualization,
    # await asyncio.sleep(.3)

  async def read_video(self):
    """Read one set of values from the video."""
    pos = (await self.video.get(), await self.video.get())
    tile_id = await self.video.get()
    self.screen[pos] = tile_id

    if tile_id == BALL:
      self.ball = pos
    if tile_id == PADDLE:
      self.paddle = pos

  def direction(self):
    """Follow the ball. Python2's cmp.

    1 if ball > paddle; -1 if ball < paddle; 0 if ball == paddle.
    """
    return (self.ball[0] > self.paddle[0]) - (self.ball[0] < self.paddle[0])

  async def run(self):
    """Run the arcade."""
    # The game waits for an input to start.
    await self.joystick.put(0)
    while self.computer.running or not self.video.empty():
      await self.read_video()
      if self.video.empty() and self.joystick.empty():
          await self.joystick.put(self.direction())
          # await self.draw()


class Day13(intcode.Challenge):

  def part2(self, computer: intcode.Computer) -> int:
    computer.memory[0] = 2
    return asyncio.run(self.arcade(computer)).screen[SCORE]

  def part1(self, computer: intcode.Computer) -> int:
    return sum(True for i in asyncio.run(self.arcade(computer)).screen.values() if i == BLOCK)

  async def arcade(self, computer: intcode.Computer) -> Arcade:
    """Run the arcade after hooking it up to the computer."""
    video = asyncio.Queue()  # type: asyncio.Queue
    joystick = asyncio.Queue(maxsize=1)  # type: asyncio.Queue
    arcade = Arcade(joystick, video, computer)

    await asyncio.gather(
      computer.run(io=(joystick, video)),
      arcade.run(),
    )
    return arcade
