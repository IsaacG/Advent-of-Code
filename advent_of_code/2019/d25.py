#!/bin/python
"""Advent of Code, Cryostasis."""

import collections
import itertools
import re

import intcode
from lib import aoc

PARSER = str
OFFSETS = {"north": (0, 1), "south": (0, -1), "east": (1, 0), "west": (-1, 0)}
REV_DIR = {"north": "south", "south": "north", "east": "west", "west": "east"}
DO_NOT_TAKE = {"infinite loop", "giant electromagnet", "molten lava", "photons", "escape pod"}
CHECKPOINT = "Security Checkpoint"

def solve(data: str, part: int) -> int:
    c = intcode.Computer(data)
    prior_room = None

    connections = collections.defaultdict(dict)
    doors = {}
    description = {}
    position = {}
    inventory = set()

    def steps(src, dst):
        assert src in connections
        assert dst in connections
        q = collections.deque()
        seen = set()
        q.append((src, []))
        while q:
            r, path = q.popleft()
            if r == dst:
                return path
            for d, n in connections[r].items():
                q.append((n, path + [d]))
        print(f"Did not find a route, {src} -> {dst}")

    queued_commands = collections.deque()
    for _ in range(80):
        c.run()
        output = c.get_output().strip()
        extra_output = []
        for block in output.strip().split("\n\n"):
            lines = block.strip().splitlines()
            if not lines:
                continue
            if lines[0].startswith("== "):
                room = lines[0].strip("= ")
                if room not in connections:
                    if prior_room:
                        connections[prior_room][cmd] = room
                        connections[room][REV_DIR[cmd]] = prior_room
                    description[room] = lines[1]
            elif lines[0] == "Doors here lead:":
                doors[room] = [i.removeprefix("- ") for i in lines[1:]]
            elif lines[0] == "Items here:":
                for item in {i.removeprefix("- ") for i in lines[1:]} - DO_NOT_TAKE:
                    inventory.add(item)
                    queued_commands.appendleft(f"take {item}")
            elif lines[0] == "Command?":
                pass
            else:
                extra_output.append(f"==> {block}")
        # print(f"> {room} || {description[room]}")
        if extra_output:
            # print("\n".join(extra_output))
            pass
        if "You can't go that way." in extra_output:
            print("Invalid. Breaking.\n\n")
            break
        unopened = {r: set(doors[r]) - set(connections[r]) for r in doors if set(doors[r]) - set(connections[r])}
        if "Security Checkpoint" in unopened:
            del unopened["Security Checkpoint"]
        if False:
            if unopened.get(room):
                print(f"Unopened doors: {unopened[room] or "N/A"}")
            if connections[room]:
                print(f"Connections: {connections[room]}")
        prior_room = room
        cmd = ""
        if queued_commands:
            cmd = queued_commands.popleft()
            # print(f"Popped queued command, {cmd}")
        elif unopened.get(room):
            cmd = unopened[room].copy().pop()
            # print(f"Room {room} has an unopened door, {cmd}. Exploring.")
        else:
            goto_room = None
            for dst, unopened_door in unopened.items():
                if dst != "Security Checkpoint" and unopened_door:
                    goto_room = dst
                    break
            if goto_room:
                cmd, *rest = steps(room, dst)
                # print(f"Navigating from {room} to {dst} to explore unopened doors. {cmd=}, {rest=}")
                queued_commands.extend(rest)
        if cmd == "":
            if room == "Security Checkpoint":
                c.input_line("inv")
                c.run()
                output = c.get_output().strip()
                # print(output)
                break
            cmd, *rest = steps(room, "Security Checkpoint")
            queued_commands.extend(rest)
        # print("cmd =", cmd)
        c.input_line(cmd)

    # print(inventory)
    door = (set(doors["Security Checkpoint"]) - set(connections["Security Checkpoint"])).pop()
    for item in inventory:
        c.input_line(f"drop {item}")
        c.run()
        c.get_output()

    for i in range(len(inventory) + 1):
        for items in itertools.combinations(inventory, r=i):
            cmds = []
            for item in items:
                cmds.append(f"take {item}")
            cmds.append(door)
            for item in items:
                cmds.append(f"drop {item}")
            for cmd in cmds:
                c.input_line(cmd)
                c.run()
                got = c.get_output().strip()
                if cmd == door and "Alert!" not in got:
                    m = re.search(r"get in by typing (\d+) on the keypad", got)
                    assert m
                    return m.group(1)
    raise RuntimeError("Not solved.")


TESTS = []
# vim:expandtab:sw=4:ts=4
