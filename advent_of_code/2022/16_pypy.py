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
            # move to valve then open valve
            turns -= dist[src][dst]
            turns -= 1
            if turns <= 0:
                break
            release += rates[dst] * turns
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
    
    
    assert answer == 3015
    return answer



if __name__ == "__main__":
    print(solve(parse()))

# vim:expandtab:sw=4:ts=4
