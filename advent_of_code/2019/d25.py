#!/bin/python
"""Advent of Code, Cryostasis."""

import collections
import itertools
import re
import intcode

OFFSETS = {"north": (0, 1), "south": (0, -1), "east": (1, 0), "west": (-1, 0)}
REV_DIR = {"north": "south", "south": "north", "east": "west", "west": "east"}
DO_NOT_TAKE = {"infinite loop", "giant electromagnet", "molten lava", "photons", "escape pod"}
CHECKPOINT = "Security Checkpoint"


class Explorer:
    """Explorer is a droid used to explore the spaceship."""

    def __init__(self, program: str):
        self.c = intcode.Computer(program)

        self.connections = collections.defaultdict[str, dict[str, str]](dict)
        self.doors = dict[str, list[str]]()
        self.description = dict[str, str]()
        self.inventory = set[str]()
        self.current_room = ""

    @property
    def unopened(self) -> dict[str, set[str]]:
        """Return doors which have not yet been opened."""
        return {
            room: set(self.doors[room]) - set(self.connections[room])
            for room in self.doors
            if room != CHECKPOINT and set(self.doors[room]) - set(self.connections[room])
        }

    def run(self, cmd: str | None = None) -> str:
        """Run a droid command and return the output."""
        if cmd:
            self.c.input_line(cmd)
        self.c.run()
        return self.c.get_output().strip()

    def explore_room(self, cmd: str | None = None):
        """Enter a room, look around, and parse the output."""
        extra_output = []
        for block in self.run(cmd).split("\n\n"):
            lines = block.splitlines()
            if not lines:
                continue
            if lines[0].startswith("== "):
                room = lines[0].strip("= ")
                if room not in self.connections:
                    if self.current_room != "" and cmd:
                        self.connections[self.current_room][cmd] = room
                        self.connections[room][REV_DIR[cmd]] = self.current_room
                    self.description[room] = lines[1]
            elif lines[0] == "Doors here lead:":
                self.doors[room] = [i.removeprefix("- ") for i in lines[1:]]
            elif lines[0] == "Items here:":
                for item in {i.removeprefix("- ") for i in lines[1:]} - DO_NOT_TAKE:
                    self.inventory.add(item)
                    self.run(f"take {item}")
            elif lines[0] == "Command?":
                pass
            else:
                extra_output.append(f"==> {block}")
        self.current_room = room

    def steps(self, target_room: str | None) -> list[str]:
        """Return the steps needed to get through an unopened door or to a target room."""
        q = collections.deque[tuple[str, list[str]]]()
        seen = {self.current_room, }
        q.append((self.current_room, []))
        while q:
            room, path = q.popleft()
            if room == target_room:
                return path
            for direction in self.doors[room]:
                if (next_room := self.connections[room].get(direction)) is None:
                    if room == CHECKPOINT:
                        continue
                    return path + [direction]
                if next_room not in seen:
                    q.append((next_room, path + [direction]))
                    seen.add(next_room)
        raise ValueError("Did not find an unopened door.")

    def explore_ship(self) -> None:
        """Wander the ship until all doors are open."""
        self.explore_room(None)
        while self.unopened:
            *steps, final_step = self.steps(None)
            for step in steps:
                self.run(step)
                self.current_room = self.connections[self.current_room][step]
            self.explore_room(final_step)
        assert 'Pressure-Sensitive Floor' not in self.connections[CHECKPOINT].values()

    def pass_checkpoint(self):
        """Brute force our way through the checkpoint."""
        for item in self.inventory:
            self.run(f"drop {item}")

        door = (set(self.doors[CHECKPOINT]) - set(self.connections[CHECKPOINT])).pop()
        holding = set()
        for r in range(4, 5):
            for items in itertools.combinations(self.inventory, r=r):
                for item in holding - set(items):
                    self.run(f"drop {item}")
                for item in set(items) - holding:
                    self.run(f"take {item}")
                holding = set(items)
                got = self.run(door)
                if "Alert!" not in got:
                    m = re.search(r"get in by typing (\d+) on the keypad", got)
                    return m.group(1)
        raise RuntimeError("Not solved.")


def solve(data: str, part: int) -> int:
    """Find the code to open the ship."""
    del part
    e = Explorer(data)
    e.explore_ship()
    for step in e.steps(CHECKPOINT):
        e.explore_room(step)
    got = e.pass_checkpoint()
    return got


TESTS = list[tuple[int, int, int]]()
# vim:expandtab:sw=4:ts=4
