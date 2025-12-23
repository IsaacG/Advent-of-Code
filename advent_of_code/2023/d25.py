#!/bin/python
"""Advent of Code, Day 25: Snowverload."""
import collections
import random


def solve(data: dict[int, set[int]], part: int) -> int:
    del part
    graph = data
    graph_list = {src: list(dsts) for src, dsts in graph.items()}
    nodes = list(graph)
    node_count = len(nodes)
    counts = collections.Counter[tuple[int, ...]]()

    for _ in range(200):
        for i in range(50):
            # Randomly wander the graph from start until we find end. Record edges traversed.
            start = random.choice(nodes)
            end = random.choice(nodes)
            cur = start
            edges = set[tuple[int, ...]]()
            while cur != end:
                neighbor = random.choice(graph_list[cur])
                edges.add(tuple(sorted([cur, neighbor])))
                cur = neighbor
            counts.update(edges)

        # See if removing the most commonly traversed three edges results in a split graph.
        candidates = [i for i, _ in counts.most_common(3)]
        for a, b in candidates:
            graph[a].remove(b)
            graph[b].remove(a)

        todo = {nodes[0]}
        group = set()
        while todo:
            cur = todo.pop()
            group.add(cur)
            for neighbor in graph[cur]:
                if neighbor not in group:
                    todo.add(neighbor)
        if len(group) != node_count:
            return len(group) * (node_count - len(group))
        for a, b in candidates:
            graph[a].add(b)
            graph[b].add(a)
    raise RuntimeError("Not solved.")


def input_parser(data: str) -> dict[int, set[int]]:
    """Parse the input data."""
    connected = collections.defaultdict(set)
    for line in data.splitlines():
        src, dsts = line.split(": ")
        for dst in dsts.split():
            connected[src].add(dst)
            connected[dst].add(src)
    labels = {val: idx for idx, val in enumerate(connected)}
    # Relabel the nodes using index numbers vs strings.
    return {labels[src]: {labels[dst] for dst in dsts} for src, dsts in connected.items()}


SAMPLE = """\
jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr"""
TESTS = [(1, SAMPLE, 54)]
# vim:expandtab:sw=4:ts=4
