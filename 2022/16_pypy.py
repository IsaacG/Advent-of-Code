#!/usr/bin/pypy3
"""Advent of Code, Day 15: Beacon Exclusion Zone. mypy benchmark version."""

import functools
import collections
import itertools
import re
import time

def add_to_tuple(t, *vals):
    return tuple(sorted(t + tuple(vals)))


def parse():
    t1 = time.perf_counter()

    RE = re.compile(r"Valve (.*) has flow rate=(\d+); tunnels? leads? to valves? (.*)")

    with open("data/16.txt") as f:
        parsed_input = [
            [int(i) if i.isdigit() else i for i in RE.match(line).groups()]
            for line in f
        ]
    t2 = time.perf_counter()
    print("Parse (ns):", int((t2 - t1) * 1000))
    return parsed_input

def solve(parsed_input) -> int:
    t1 = time.perf_counter()
    data = [
        [room, rate, leads_to.split(", ")]
        for room, rate, leads_to in parsed_input
    ]
    room_num = {room: i for i, (room, _, _) in enumerate(data)}
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

    for k in rooms:
        for i in rooms:
            for j in rooms:
                if k in dist[i] and j in dist[k]:
                    if j not in dist[i] or dist[i][j] > dist[i][k] + dist[k][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
    t2 = time.perf_counter()
    print("Setup (ns):", int((t2 - t1) * 1000))

    def releases(valve_order):
        turns = 26
        release = 0
        location = start_room
        for valve in valve_order:
            # move to valve
            turns -= dist[location][valve]
            # open valve
            turns -= 1
            if turns <= 0:
                break
            release += rates[valve] * turns
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

    def human_vs_elephant_valves():
        answer = 0
        for valve_count in range(0, 9):
            for human_valves in itertools.combinations(rooms_with_rates, valve_count):
                human_order = max(itertools.permutations(human_valves), key=releases)
                human_release = releases(human_order)
                elephant_valve_candidates = rooms_with_rates - set(human_valves)
                for elephant_valves in itertools.combinations(elephant_valve_candidates, min(len(elephant_valve_candidates), valve_count)):
                    elephant_order = max(itertools.permutations(elephant_valves), key=releases)
                    elephant_release = releases(elephant_order)
                    answer = max(answer, human_release + elephant_release)
        return answer

    def dijsktra():
        answer = 0
        priors = {}
        to_explore = set([tuple([0, start_room, start_room, tuple()])])
        seen_at_moves = {tuple([0, start_room, start_room, tuple()]): 25}
        while to_explore:
            p = max(to_explore)
            released, cur, ele, opened = p
            to_explore.remove(p)
            moves = seen_at_moves[p]

            if moves <= 1 or set(opened) == rooms_with_rates:
                if released > answer:
                    answer = released
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
                    options.append((new_released, cur, ele, new_open))
                # you open, ele moves
                else:
                    for loc in sorted(tunnels[ele], reverse=True, key=lambda x: 0 if x in opened else rates[x]):
                        new_released = released + rates[cur] * moves
                        new_open = add_to_tuple(opened, cur)
                        options.append((new_released, cur, loc, new_open))
            elif ele not in opened and ele in rooms_with_rates:
                # you move, ele opnes
                for loc in sorted(tunnels[cur], reverse=True, key=lambda x: 0 if x in opened else rates[x]):
                    new_released = released + rates[ele] * moves
                    new_open = add_to_tuple(opened, ele)
                    options.append((new_released, loc, ele, new_open))
            # both move
            else:
                for you_loc in sorted(tunnels[cur], reverse=True, key=lambda x: 0 if x in opened else rates[x]):
                    for ele_loc in sorted(tunnels[ele], reverse=True, key=lambda x: 0 if x in opened else rates[x]):
                        options.append((released, you_loc, ele_loc, opened))
            for option in options:
                if option[1] > option[2]:
                    option = tuple([option[0], option[2], option[1], option[3]])
                if seen_at_moves.get(option, -1) < moves - 1:
                    seen_at_moves[option] = moves - 1
                    to_explore.add(option)
        return answer

    a = [36, 18, 0, 30, 5, 3]
    b = [40, 4, 33, 38, 42]
    print(releases(a))
    print(releases(b))
    print(releases(a) + releases(b))
    return


    dij, hve, df = True, False, False
    if dij:
        t1 = time.perf_counter()
        answer = dijsktra()
        t2 = time.perf_counter()
        print(answer, "dijsktra", (t2 - t1) * 1000000)

    if hve:
        t1 = time.perf_counter()
        answer = human_vs_elephant_valves()
        t2 = time.perf_counter()
        print(answer, "human_vs_elephant_valves", (t2 - t1) * 1000000)

    if df:
        t1 = time.perf_counter()
        answer = dfs()
        t2 = time.perf_counter()
        print(answer, "dfs", (t2 - t1) * 1000000)
    
    
    assert answer > 2903
    return answer



if __name__ == "__main__":
    print(solve(parse()))

# vim:expandtab:sw=4:ts=4
