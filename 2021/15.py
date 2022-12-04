#!/bin/python
"""Advent of Code: Day 15."""

import typer
from lib import aoc

SAMPLE = ["""\
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
"""]
InputType = dict[complex, int]


class Day15(aoc.Challenge):
    """Navigate through a maze of chiton, minimizing damage/cost."""

    TESTS = (
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=40),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=315),
    )

    def part1(self, parsed_input: InputType) -> int:
        """Return the lowest cost path from start to end."""
        return self.solve(parsed_input)

    def part2(self, parsed_input: InputType) -> int:
        """Return the lowest cost path from start to end ... with larger input."""
        graph = parsed_input
        width = graph.width
        height = graph.height

        # Dictionary comprehension is hard to read.
        # full_graph = {
        #     (x * width + point.real) + (y * height + point.imag) * 1j: (
        #         ((val + x + y - 1) % 9) + 1
        #     )
        #     for x in range(5) for y in range(5) for point, val in graph.items()
        # }

        full_graph = aoc.Board()
        for x in range(5):
            for y in range(5):
                for point, val in graph.items():
                    # Scale the point by x, y
                    point = (x * width + point.real) + (y * height + point.imag) * 1j
                    # Add +1 to the value for each shift. Modulus 9 so that 10 wraps around to 1.
                    val = ((val + x + y - 1) % 9) + 1
                    # Insert the point.
                    full_graph[point] = val

        return self.solve(full_graph)

    @staticmethod
    def solve(node_weights: InputType) -> int:
        """Return the lowest cost path from start to end with Djiksta's."""
        starting_point = complex(0)
        end_point = node_weights.max_point

        # Use Djiksta's to compute the cost from start to every node.
        cost = {starting_point: 0}
        visited = set()
        todo = set([starting_point])
        while todo:
            # Pop the lowest cost node.
            current = sorted(todo, key=lambda x: cost[x])[0]
            todo.remove(current)
            # Mark it visited.
            visited.add(current)
            # Update neighbors with min(existing cost, cost through current)
            for neighbor in node_weights.neighbors(current, diagonal=False):
                if neighbor in visited:
                    continue
                cost_through_current = cost[current] + node_weights[neighbor]
                if neighbor not in cost or cost[neighbor] > cost_through_current:
                    cost[neighbor] = cost_through_current
                    # Add unvisited neighbors to the todo list.
                    todo.add(neighbor)
        return cost[end_point]

    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        return aoc.Board.from_int_block(puzzle_input)


if __name__ == "__main__":
    typer.run(Day15().run)

# vim:expandtab:sw=4:ts=4
