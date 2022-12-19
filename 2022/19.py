#!/bin/python
"""Advent of Code, Day 19: Not Enough Minerals."""
from __future__ import annotations

import collections
import functools
import itertools
import math
import re

import typer
from lib import aoc

SAMPLE = [
    """\
Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.""", # 0
]

LineType = int
InputType = list[LineType]

ORE = 0
CLAY = 1
OBSIDIAN = 2
GEODE = 3
ROCKS = [ORE, CLAY, OBSIDIAN, GEODE]
TYPES = {
    "ore": ORE,
    "clay": CLAY,
    "obsidian": OBSIDIAN,
    "geode": GEODE,
}

class Day19(aoc.Challenge):
    """Day 19: Not Enough Minerals."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}
    # PARAMETERIZED_INPUTS = [5, 50]

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=aoc.TEST_SKIP),
        # aoc.TestCase(inputs=SAMPLE[0], part=1, want=33),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=56 * 62),
    ]

    def part1(self, parsed_input: InputType) -> int:
        return 1
        score = 0
        for idx, blueprint in enumerate(parsed_input, start=1):
            print(f"Testing blueprint {idx}")
            # turns, robots, inventory
            seen = set()
            todo = {(-24, 0, 0, 0, 0, 0, 0, 1, 0)}
            highest = 0
            highest_rg_at_step = {i: 0 for i in range(-24, 1)}
            highest_ig_at_step = {i: 0 for i in range(-24, 1)}
            while todo:
                cur = max(todo)
                if len(seen) % 50000 == 0:
                    print(f"{highest=} {len(seen)=} {len(todo)=} {cur=}")
                todo.remove(cur)
                turns, rg, ig, rb, ib, rc, ic, rr, ir = cur
                if turns == 0:
                    highest = max(highest, ig)
                    continue
                elif turns > 0:
                    raise RuntimeError

                if rg + 1 < highest_rg_at_step[turns] and ig + 1 < highest_ig_at_step[turns]:
                    continue

                highest_ig_at_step[turns] = max(highest_ig_at_step[turns], ig)
                highest_rg_at_step[turns] = max(highest_rg_at_step[turns], rg)
                # Build possibly
                for robotype in (3, 2, 1, 0):
                    cb, cc, cr = blueprint[robotype]
                    if cr <= ir and cc <= ic and cb <= ib:
                        nrr, nrc, nrb, nrg = rr, rc, rb, rg
                        if robotype == ORE: nrr += 1
                        elif robotype == CLAY: nrc += 1
                        elif robotype == OBSIDIAN: nrb += 1
                        elif robotype == GEODE: nrg += 1
                        next_state = (
                            turns + 1,
                            nrg, ig + rg,
                            nrb, ib + rb - cb,
                            nrc, ic + rc - cc,
                            nrr, ir + rr - cr,
                        )
                        if next_state not in seen:
                            seen.add(next_state)
                            todo.add(next_state)
                # Produce ore
                next_state = (
                    turns + 1,
                    rg, ig + rg,
                    rb, ib + rb,
                    rc, ic + rc,
                    rr, ir + rr,
                )
                if next_state not in seen:
                    seen.add(next_state)
                    todo.add(next_state)
            print(f"{idx} scores {highest}")
            score += idx * highest
        return score

    def part2(self, parsed_input: InputType) -> int:
        """
        score = 1
        STEPS = 32

        for idx, blueprint in [(2, parsed_input[1])]:

            max_prodution = {rock: {} for rock in ROCKS}

            for material in ORE, CLAY, OBSIDIAN, GEODE:
                if material == ORE:
                    todo = set(STEPS, 0, 1)
                    
                for nturn in range(turns, 0):
                    max_prodution[ore] = cur_i
                    cur_i += cur_r
                    cur_r += 1
                    


        return
        """

        score = 1
        for idx, blueprint in enumerate(parsed_input[:3], start=1):
            print(f"Testing blueprint {idx}")
            max_spend = {rock: max(cost[rock] for cost in blueprint.values()) for rock in (ORE, CLAY, OBSIDIAN)}
            # turns, robots, inventory
            seen = set()
            todo = {(-32, 0, 0, 0, 0, 0, 0, 1, 0)}
            turns_to_bots = {1: -32}
            highest = 0
            while todo:
                cur = max(todo)
                if len(seen) % 500000 == 0:
                    print(f"{highest=} {len(seen)=} {len(todo)=} {cur=}")
                todo.remove(cur)
                turns, rg, ig, rb, ib, rc, ic, rr, ir = cur
                if turns == 0:
                    highest = max(highest, ig)
                    continue

                # never build more robots than can be spent on a single turn
                # stop early if we haven't built enough geode robots to reach our goal before time limit (highest seen so far)
                # stop early if we haven't built enough obsidian robots to reach our goal of geode robots before we need to switch to making only geode robots (as many as we need to hit our geode goal)
                # didn't do the stop early's exactly, just close enough to ensure super dead branches weren't explored. some dead branches still got through but not very many (eg assume we have resources to make a geode bot each minute, assume that we'll have the full output of the obsidian miners in the whole 30 minutes at the time we start building geode bots)

                if ig + rg * -turns + sum(range(-turns)) < highest:
                    continue

                candidates = []

                if blueprint[GEODE][ORE] <= ir and blueprint[GEODE][OBSIDIAN] <= ib:
                    candidates.append((
                        True,
                        turns + 1,
                        rg + 1, ig + rg,
                        rb    , ib + rb - blueprint[GEODE][OBSIDIAN],
                        rc    , ic + rc,
                        rr    , ir + rr - blueprint[GEODE][ORE],
                    ))
                else:
                    max_obs_used = blueprint[GEODE][OBSIDIAN] * (-turns - 1)
                    min_obs_avail = ib + rb * (-turns - 1)
                    if rb < max_spend[OBSIDIAN] and blueprint[OBSIDIAN][ORE] <= ir and blueprint[OBSIDIAN][CLAY] <= ic and max_obs_used > min_obs_avail:
                            candidates.append((
                                True,
                                turns + 1,
                                rg    , ig + rg,
                                rb + 1, ib + rb,
                                rc    , ic + rc - blueprint[OBSIDIAN][CLAY],
                                rr    , ir + rr - blueprint[OBSIDIAN][ORE],
                            ))
                    max_clay_used = blueprint[OBSIDIAN][CLAY] * (-turns - 1)
                    min_clay_avail = ic + rc * (-turns - 1)
                    if rc < max_spend[CLAY] and blueprint[CLAY][ORE] <= ir and blueprint[CLAY][ORE] and max_clay_used > min_clay_avail:
                        candidates.append((
                            True,
                            turns + 1,
                            rg    , ig + rg,
                            rb    , ib + rb,
                            rc + 1, ic + rc,
                            rr    , ir + rr - blueprint[CLAY][ORE],
                        ))
                    if rr < max_spend[ORE] and blueprint[ORE][ORE] <= ir and blueprint[ORE][ORE] < -turns:
                        candidates.append((
                            True,
                            turns + 1,
                            rg    , ig + rg,
                            rb    , ib + rb,
                            rc    , ic + rc,
                            rr + 1, ir + rr - blueprint[ORE][ORE],
                        ))
                    candidates.append((
                        False,
                        turns + 1,
                        rg, ig + rg,
                        rb, ib + rb,
                        rc, ic + rc,
                        rr, ir + rr,
                    ))
                for next_state in candidates:
                    building = next_state[0]
                    next_state = next_state[1:]
                    bots = 0
                    for i in (1, 3, 5, 7):
                        bots <<= 5
                        bots |= next_state[i]
                    hsh = (bots << 7) | -next_state[0]
                    for i in (2, 4, 6, 8):
                        hsh <<= 9
                        hsh |= next_state[i]
                    if hsh in seen:
                        continue
                    if building and bots in turns_to_bots:
                        if turns_to_bots[bots] < next_state[0]:
                            continue
                    turns_to_bots[bots] = next_state[0]

                    seen.add(hsh)
                    todo.add(next_state)
            print(f"{idx} scores {highest}")
            score *= highest
        return score

    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        blueprints = []
        RE = re.compile("Each (.*) robot costs (.*)")
        base_costs = {t: 0 for t in TYPES.values()}
        for line in puzzle_input.splitlines():
            blueprint = {}
            _, line = line.split(": ")
            for sentence in line.removesuffix(".").split(". "):
                costs = base_costs.copy()
                out, ins = RE.match(sentence).groups()
                for a in ins.split(" and "):
                    num, ore = a.split()
                    costs[TYPES[ore]] = int(num)
                blueprint[TYPES[out]] = tuple(costs[i] for i in (ORE, CLAY, OBSIDIAN))
            blueprints.append(blueprint)
        return blueprints


if __name__ == "__main__":
    typer.run(Day19().run)

# vim:expandtab:sw=4:ts=4
