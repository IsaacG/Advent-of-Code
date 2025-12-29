#!/bin/python
"""Advent of Code, Day 13: Care Package. Play paddle ball."""
import intcode

# Tiles
BLOCK = 2
PADDLE = 3
BALL = 4
SCORE = (-1, 0)


def solve(data: str, part: int) -> int:
    """Play the game by moving the paddle to follow the ball."""
    computer = intcode.Computer(data)
    if part == 2:
        computer.memory[0] = 2  # start the game without tokens

    paddle, ball, score = 0, 0, 0
    while not computer.stopped:
        computer.run()
        # Read all the video output
        blocks = set()
        while computer.output:
            x, y, tile = (computer.output.popleft() for _ in range(3))
            if tile == PADDLE:
                paddle = x
            elif tile == BALL:
                ball = x
            elif tile == BLOCK:
                blocks.add((x, y))
            elif (x, y) == SCORE:
                score = tile
        if part == 1:
            return len(blocks)

        # Move the joystick.
        if paddle > ball:
            direction = -1
        elif paddle < ball:
            direction = 1
        else:
            direction = 0
        computer.input.append(direction)
    return score


TESTS = list[tuple[int, int, int]]()
