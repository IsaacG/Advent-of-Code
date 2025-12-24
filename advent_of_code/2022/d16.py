#!/bin/python
"""Advent of Code, Day 16: Proboscidea Volcanium. Open valves to release pressure."""

import collections
import functools
import itertools
import math
import re
import time

from lib import aoc

def input_parser(data: str) -> tuple[dict[str, int], dict[str, list[str]]]:
    rates = {}
    direct = {}
    patt = re.compile(r"Valve (.*) has flow rate=(\d+); tunnels? leads? to valves? (.*)")
    for line in data.splitlines():
        m = patt.match(line)
        assert m is not None
        src, rate, dsts = m.groups()
        rates[src] = int(rate)
        direct[src] = dsts.split(", ")
    return rates, direct


def complete_graph(direct: dict[str, list[str]], rates: dict[str, int]) -> dict[str, dict[str, int]]:
    start = time.perf_counter_ns()
    # Shortest distances between any two rooms.
    # https://en.wikipedia.org/wiki/Floyd%E2%80%93Warshall_algorithm
    distance = collections.defaultdict(dict)
    for src in direct:
        distance[src][src] = 0
    for src, dsts in direct.items():
        for dst in dsts:
            distance[src][dst] = 1

    for shortcut, src, dst in itertools.permutations(direct, 3):
        if shortcut in distance[src] and dst in distance[shortcut]:
            dist_via_shortcut = distance[src][shortcut] + distance[shortcut][dst]
            if dst not in distance[src] or distance[src][dst] > dist_via_shortcut:
                distance[src][dst] = dist_via_shortcut
    for src in distance:
        del distance[src][src]
    end = time.perf_counter_ns()
    # print(f"Floyd Warshall: {(end - start) / 1_000_000}ms")
    # Add one second each to account for opening the valve.
    return {
        src: {dst: dist + 1 for dst, dist in sorted(distance[src].items()) if rates[dst] > 0}
        for src in sorted(distance)
        if src == "AA" or rates[src] > 0
    }


def solve(data: tuple[dict[str, int], dict[str, list[str]]], part: int) -> int:
    rates, direct = data
    distance = complete_graph(direct, rates)
    # print(rates)
    # print(direct)
    # print(distance)
    max_time = 30 if part == 1 else 26

    @functools.cache
    def dp(position: str, time_left: int, remaining: frozenset[str]) -> int:
        most = 0
        dist = distance[position]
        for next_position, time_cost in distance[position].items():
            if time_cost >= time_left or next_position not in remaining:
                continue
            adjusted_time = time_left - time_cost
            additional_flow = adjusted_time * rates[next_position]
            downstream = dp(next_position, adjusted_time, frozenset(remaining - {next_position}))
            total_flow = additional_flow + downstream
            if total_flow > most:
                most = total_flow
        return most

    all_valves = frozenset(distance)
    if part == 1:
        return dp("AA", max_time, all_valves)

    most = 0
    for r in range(len(distance)):
        start = time.perf_counter_ns()
        for group_one in itertools.combinations(distance, r=r):
            g = frozenset(group_one)
            combined = dp("AA", max_time, g) + dp("AA", max_time, frozenset(all_valves - g))
            most = max(most, combined)
        end = time.perf_counter_ns()
        print(f"{r=}, {most=}, {(end - start) / 1_000_000_000}s")
    return most


SAMPLE = """\
Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II"""
TESTS = [(1, SAMPLE, 1651), (2, SAMPLE, 1707)]
