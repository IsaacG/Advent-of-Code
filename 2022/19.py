#!/bin/python
"""Advent of Code, Day 19: Not Enough Minerals."""

import re

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

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=33),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=56 * 62),
    ]
    TIMEOUT = 300

    def simulator(self, parsed_input: InputType, minutes: int) -> int:
        scores = []
        for idx, blueprint in enumerate(parsed_input, start=1):
            self.debug(f"Testing blueprint {idx}")
            max_spend = {rock: max(cost[rock] for cost in blueprint.values()) for rock in (ORE, CLAY, OBSIDIAN)}
            seen = set()
            todo = {(-minutes, 0, 0, 0, 0, 0, 0, 1, 0)}
            turns_to_bots = {1: -minutes}
            highest = 0
            while todo:
                cur = max(todo)
                todo.remove(cur)
                turns, rg, ig, rb, ib, rc, ic, rr, ir = cur
                if turns == 0:
                    highest = max(highest, ig)
                    continue

                # never build more robots than can be spent on a single turn
                # stop early if we haven't built enough geode robots to reach our goal before time limit (highest seen so far)
                # stop early if we haven't built enough obsidian robots to reach our goal of geode robots before we need to switch to making only geode robots (as many as we need to hit our geode goal)
                # didn't do the stop early's exactly, just close enough to ensure super dead branches weren't explored. some dead branches still got through but not very many (eg assume we have resources to make a geode bot each minute, assume that we'll have the full output of the obsidian miners in the whole 30 minutes at the time we start building geode bots)

                if ig + rg * -turns + (turns * (turns + 1)) // 2 < highest:
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
            self.debug(f"{idx} scores {highest}")
            scores.append(highest)
        return scores

    def part1(self, parsed_input: InputType) -> int:
        scores = self.simulator(parsed_input, 24)
        return sum(idx * score for idx, score in enumerate(scores, start=1))

    def part2(self, parsed_input: InputType) -> int:
        return self.mult(self.simulator(parsed_input[:3], 32))

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
