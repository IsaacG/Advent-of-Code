#!/bin/python
"""Advent of Code: Day 15. Navigate through a maze of chiton, minimizing damage/cost."""
import typing
from lib import aoc


def solve(data: aoc.Map, part: int) -> int:
    """Return the lowest cost path from start to end."""
    graph = typing.cast(dict[tuple[int, int], int], data.chars)
    width = data.width
    height = data.height

    if part == 2:
        # Expand the graph.
        full_graph = {}
        for repeat_x in range(5):
            for repeat_y in range(5):
                repeat_offset = repeat_x + repeat_y
                for (p_x, p_y), val in graph.items():
                    # Scale the point by repeat_x, repeat_y
                    point = repeat_x * width + p_x, repeat_y * height + p_y
                    # Add +1 to the value for each shift. Modulus 9 so that 10 wraps around to 1.
                    val = ((val + repeat_offset - 1) % 9) + 1
                    # Insert the point.
                    full_graph[point] = val
        graph = full_graph

    return solve_graph(graph)


def solve_graph(node_weights: dict[tuple[int, int], int]) -> int:
    """Return the lowest cost path from start to end with Djiksta's."""
    starting_point = (0, 0)
    end_point = max(node_weights)

    # Use Djiksta's to compute the cost from start to every node.
    cost = {starting_point: 0}
    visited = set()
    todo = {starting_point}
    while todo:
        # Pop the lowest cost node.
        current = sorted(todo, key=lambda x: cost[x])[0]
        todo.remove(current)
        # Mark it visited.
        visited.add(current)
        # Update neighbors with min(existing cost, cost through current)
        for neighbor in aoc.t_neighbors4(current):
            if neighbor in visited or neighbor not in node_weights:
                continue
            ncost = node_weights[neighbor]
            cost_through_current = cost[current] + ncost
            if neighbor not in cost or cost[neighbor] > cost_through_current:
                cost[neighbor] = cost_through_current
                # Add unvisited neighbors to the todo list.
                todo.add(neighbor)
    return cost[end_point]


SAMPLE = """\
1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581
"""
TESTS = [(1, SAMPLE, 40), (2, SAMPLE, 315)]
