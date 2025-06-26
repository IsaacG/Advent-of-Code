#!/bin/python
"""Advent of Code: Day 15."""

from lib import aoc

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


class Day15(aoc.Challenge):
    """Navigate through a maze of chiton, minimizing damage/cost."""

    TESTS = (
        aoc.TestCase(inputs=SAMPLE, part=1, want=40),
        aoc.TestCase(inputs=SAMPLE, part=2, want=315),
    )
    TIMEOUT = 90

    def part1(self, puzzle_input: aoc.Map) -> int:
        """Return the lowest cost path from start to end."""
        return self.solve(puzzle_input)

    def part2(self, puzzle_input: aoc.Map) -> int:
        """Return the lowest cost path from start to end ... with larger input."""
        graph = puzzle_input
        width = graph.width
        height = graph.height

        full_graph = {}
        for x in range(5):
            for y in range(5):
                repeat_offset = x + y
                for point, val in graph.chars.items():
                    # Scale the point by x, y
                    point = (x * width + point.real) + (y * height + point.imag) * 1j
                    # Add +1 to the value for each shift. Modulus 9 so that 10 wraps around to 1.
                    val = ((val + repeat_offset - 1) % 9) + 1
                    # Insert the point.
                    full_graph[point] = val

        rows = [
            "".join(
                str(full_graph[complex(x, y)])
                for x in range(graph.width * 5)
            )
            for y in range(graph.height * 5)
        ]
        graph = aoc.CoordinatesParser().parse("\n".join(rows))
        return self.solve(graph)

    @staticmethod
    def solve(node_weights: aoc.Map) -> int:
        """Return the lowest cost path from start to end with Djiksta's."""
        starting_point = complex(0)
        end_point = complex(node_weights.max_x, node_weights.max_y)

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
            for neighbor, ncost in node_weights.neighbors(current).items():
                if neighbor in visited:
                    continue
                cost_through_current = cost[current] + ncost
                if neighbor not in cost or cost[neighbor] > cost_through_current:
                    cost[neighbor] = cost_through_current
                    # Add unvisited neighbors to the todo list.
                    todo.add(neighbor)
        return cost[end_point]
