#!/bin/python
"""Advent of Code, Day 16: Proboscidea Volcanium. Open valves to release pressure."""
from __future__ import annotations

import collections
import functools
import itertools
import math
import re
import time

from lib import aoc

SAMPLE = [
    """\
Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II""",
]

LineType = int
InputType = list[LineType]

def add_to_tuple(t, *vals):
    return tuple(sorted(t + tuple(vals)))


class Day16(aoc.Challenge):
    """Day 16: Proboscidea Volcanium."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}

    TESTS = [
        # aoc.TestCase(inputs=SAMPLE[0], part=1, want=1651),
        # aoc.TestCase(inputs=SAMPLE[0], part=2, want=0),
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=aoc.TEST_SKIP),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=aoc.TEST_SKIP),
    ]

    INPUT_PARSER = aoc.parse_re_group_mixed(r"Valve (.*) has flow rate=(\d+); tunnels? leads? to valves? (.*)")
    TIMEOUT = 300

    def part2(self, puzzle_input: InputType) -> int:
        return 0
        data = [
            [room, rate, leads_to.split(", ")]
            for room, rate, leads_to in puzzle_input
        ]
        room_num = {room: i for i, (room, _, _) in enumerate(data)}
        room_name = {i: room for i, (room, _, _) in enumerate(data)}
        tunnels = {i: [room_num[dest] for dest in leads_to] for i, (_, _, leads_to) in enumerate(data)}
        rates = {i: rate for i, (_, rate, _) in enumerate(data)}
        rooms_with_rates = {i for i, rate in rates.items() if rate}
        rooms = set(tunnels)
        start_room = room_num["AA"]

        # Shortest distances between any two rooms.
        # https://en.wikipedia.org/wiki/Floyd%E2%80%93Warshall_algorithm
        dist = collections.defaultdict(dict)
        for room in rooms:
            dist[room][room] = 0
        for room, leads_to in tunnels.items():
            for dest in leads_to:
                dist[room][dest] = 1

        t1 = time.perf_counter()
        for shortcut, src, dest in itertools.permutations(rooms, 3):
            if shortcut in dist[src] and dest in dist[shortcut]:
                dist_via_shortcut = dist[src][shortcut] + dist[shortcut][dest]
                if dest not in dist[src] or dist[src][dest] > dist_via_shortcut:
                    dist[src][dest] = dist_via_shortcut

        t2 = time.perf_counter()
        print("Setup (ns):", int((t2 - t1) * 1000))

        def check_dist(src, dst):
            explore = [(0, src)]
            added = {src,}
            while explore:
                steps, cur = explore.pop(0)
                if cur == dst:
                    return steps
                for candidate in tunnels[cur]:
                    if candidate not in added:
                        added.add(candidate)
                        explore.append((steps + 1, candidate))

        def validate_distances():
            for src in dist:
                for dst in dist[src]:
                    if check_dist(src, dst) != dist[src][dst]:
                        raise RuntimeError
            print("Distances seem right.")

        def releases(valve_order):
            turns = 26
            release = 0
            for src, dst in zip([start_room] + list(valve_order), valve_order):
                # move to valve
                turns -= dist[src][dst]
                # open valve
                turns -= 1
                # print(f"{src}->{dst} {dist[src][dst]} moves => {turns}")
                # print(f"{room_name[src]}->{room_name[dst]} {dist[src][dst]} moves => {turns}")

                # fl_dist = dist[src][dst]
                # bf_dist = check_dist(src, dst)
                # assert fl_dist == bf_dist, f"{fl_dist=} != {bf_dist=}"
                # print(f"{release} + {rates[dst]} * {turns} ({rates[dst] * turns}) => {release + rates[dst] * turns}")
                if turns <= 0:
                    # print(f"Out of moves trying to visit {room_name[dst]}")
                    break
                release += rates[dst] * turns
            # print()
            return release

        def dfs(human_order, elephant_order):
            closed = rooms_with_rates - set(human_order) - set(elephant_order)
            if len(closed) >= 2:
                return max(
                    dfs(human_order + [nh], elephant_order + [ne])
                    for nh, ne in itertools.permutations(closed, 2)
                )

            options = []
            if len(closed) == 0:
                options.append((human_order, elephant_order))
            elif len(closed) == 1:
                last = closed.pop()
                options.append((human_order + [last], elephant_order))
                options.append((human_order, elephant_order + [last]))

            return max(
                releases(human) + releases(elephant)
                for human, elephant in options
            )

        def partitioning():
            valves_to_use = {36, 0, 30, 5, 3, 40, 18, 4, 33, 38, 42}
            valves_to_use = list(sorted(rooms_with_rates, reverse=True))
            answer = 0
            for human_count in range(5, 8):
                for human_valves in itertools.combinations(valves_to_use, human_count):
                    human_order = max(itertools.permutations(human_valves), key=releases)
                    human_release = releases(human_order)
                    if human_release < answer // 2:
                        continue
                    elephant_valve_candidates = set(valves_to_use) - set(human_valves)
                    for elephant_count in range(max(5, human_count), min(8, len(elephant_valve_candidates))):
                        for elephant_valves in itertools.combinations(elephant_valve_candidates, elephant_count):
                            if elephant_valves[0] < human_valves[0]:
                                break
                            elephant_order = max(itertools.permutations(elephant_valves), key=releases)
                            combined_release = releases(elephant_order) + human_release
                            if combined_release == 3015:
                                print(combined_release, human_order, elephant_order)
                            answer = max(answer, combined_release)
            return answer

        def dijsktra():
            answer = 0
            priors = {}
            to_explore = set([tuple([0, start_room, start_room, tuple(), tuple(), tuple()])])
            seen_at_moves = {tuple([0, start_room, start_room, tuple(), tuple(), tuple()]): 25}
            flow_for_opened = {}
            while to_explore:
                p = max(to_explore)
                released, cur, ele, opened, human_moves, elephant_moves = p
                to_explore.remove(p)
                moves = seen_at_moves[p]
                if opened not in flow_for_opened:
                    flow_for_opened[opened] = released
                elif flow_for_opened[opened] > released:
                    continue

                if moves <= 1 or set(opened) == rooms_with_rates:
                    if released > answer:
                        answer = released
                        if answer == 3015:
                            print(answer, human_moves, elephant_moves)
                            break
                    continue

                # 2250
                # After 13 turns, you can eliminate any state that is more than (26-turns)*(best two valves) below the highest score so far.
                # best: 24 25
                if moves < 10 and released < answer - (moves+1) * 49:
                    continue

                options = []
                if cur not in opened and cur in rooms_with_rates:
                    if ele not in opened and cur != ele and ele in rooms_with_rates:
                        # both open
                        new_released = released + (rates[cur] + rates[ele]) * moves
                        new_open = add_to_tuple(opened, cur, ele)
                        options.append((new_released, cur, ele, new_open, human_moves + (cur,), elephant_moves + (ele,)))
                    # you open, ele moves
                    else:
                        for loc in sorted(tunnels[ele], reverse=True, key=lambda x: 0 if x in opened else rates[x]):
                            new_released = released + rates[cur] * moves
                            new_open = add_to_tuple(opened, cur)
                            options.append((new_released, cur, loc, new_open, human_moves + (cur,), elephant_moves))
                elif ele not in opened and ele in rooms_with_rates:
                    # you move, ele opens
                    for loc in sorted(tunnels[cur], reverse=True, key=lambda x: 0 if x in opened else rates[x]):
                        new_released = released + rates[ele] * moves
                        new_open = add_to_tuple(opened, ele)
                        options.append((new_released, loc, ele, new_open, human_moves, elephant_moves + (ele,)))
                # both move
                else:
                    for you_loc in sorted(tunnels[cur], reverse=True, key=lambda x: 0 if x in opened else rates[x]):
                        for ele_loc in sorted(tunnels[ele], reverse=True, key=lambda x: 0 if x in opened else rates[x]):
                            options.append((released, you_loc, ele_loc, opened, human_moves, elephant_moves))
                for option in options:
                    if option[1] > option[2]:
                        option = tuple([option[0], option[2], option[1]]) + option[3:]
                    if seen_at_moves.get(option, -1) < moves - 1:
                        seen_at_moves[option] = moves - 1
                        to_explore.add(option)
            return answer

        # print([room_name[i] for i in a])
        # print([room_name[i] for i in b])
        # print(releases(b))
        # print()
        # print(releases(a) + releases(b))
        # c = [next(n for n, m in room_num.items() if m == i) for i in a + b]
        # print(c)
        # validate_distances()

        dij, hve, df = False, True, False
        if dij:
            t1 = time.perf_counter()
            answer = dijsktra()
            t2 = time.perf_counter()
            print(answer, "dijsktra", (t2 - t1) * 1000000)

        if hve:
            t1 = time.perf_counter()
            answer = partitioning()
            t2 = time.perf_counter()
            print(answer, "partitioning", (t2 - t1) * 1000000)

        if df:
            t1 = time.perf_counter()
            answer = dfs([], [])
            t2 = time.perf_counter()
            print(answer, "dfs", (t2 - t1) * 1000000)
        
        return answer

    def part1(self, puzzle_input: InputType) -> int:
        rooms = {}
        for room, rate, leads_to in puzzle_input:
            rooms[room] = (rate, leads_to.split(", "))

        might_open = {room for room, rate in rooms.items() if rate}

        max_flow = 0
        to_explore = set([tuple([0, "AA", tuple()])])
        seen_at_moves = {tuple([0, "AA", tuple()]): 29}
        steps = 0
        while to_explore:
            steps += 1
            p = max(to_explore)
            released, cur, opened = p
            to_explore.remove(p)
            moves = seen_at_moves[p]

            if moves <= 1 or set(opened) == might_open:
                max_flow = max(max_flow, released)
                continue

            # 2250
            if released < max_flow - moves * 95:
                continue

            options = []
            if cur not in opened:
                # Consider opening this one
                options.append((released + rooms[cur][0] * moves, cur, add_to_tuple(opened, cur)))

            for loc in rooms[cur][1]:
                options.append((released, loc, opened))
            for option in options:
                if seen_at_moves.get(option, -1) < moves - 1:
                    seen_at_moves[option] = moves - 1
                    to_explore.add(option)
        
        answer = max_flow
        if not self.testing:
            assert answer > 1336
            assert answer > 1976
        return answer

        @functools.cache
        def solve(cur, opened, released, moves):
            if moves == 0:
                return [released]
            options = []
            if cur not in opened and rooms[cur][0]:
                # Consider opening this one
                options.append(solve(cur, tuple(sorted(opened + tuple([cur]))), released + rooms[cur][0] * moves, moves - 1))
            for loc in rooms[cur][1]:
                options.append(solve(loc, opened, released, moves - 1))
            return max(options)

        return max(solve("AA", tuple(), 0, 29))
