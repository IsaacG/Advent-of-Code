"""Everyone Codes Day N.

Part three. Solve for the specific input.
The source plants with free branches all have exactly two output branches.
The thickness of the output branches are either both positive or both negative.
We can solve for optimal/maximal output by turning off plants with negative output branches and turning on the others.
"""

import collections
import re
from lib import helpers
from lib import parsers


class Garden:
    """Garden holds plant data."""

    def __init__(self, plant_data: str):
        """Parse the input plant data."""
        # input_plants: plants with one free branch, with input energy of 0 or 1.
        self.input_plants = set()
        # plant_in: branches leading into this plant; input energy.
        # Stores a tuple, the source plant ID and branch thickness.
        self.plant_in = collections.defaultdict(list)
        # plant_out: branches out of this plant; downstream energy. Stored branch thickness.
        self.plant_out = collections.defaultdict(list)
        # thickness: thickness of a plant.
        self.thickness = {}

        for chunk in plant_data.split("\n\n"):
            plant_str, *branches = chunk.splitlines()
            m = re.match(r"Plant (\d+) with thickness (-?\d+):", plant_str)
            assert m
            plant, thick = [int(i) for i in m.groups()]
            self.thickness[plant] = thick
            for branch in branches:
                if branch == "- free branch with thickness 1":
                    self.input_plants.add(plant)
                else:
                    m = re.match(r"- branch to Plant (\d+) with thickness (-?\d+)", branch)
                    assert m
                    branch_in, thick = [int(i) for i in m.groups()]
                    self.plant_in[plant].append((branch_in, thick))
                    self.plant_out[branch_in].append(thick)
        self.num_inputs = len(self.input_plants)
        self.target = (set(self.thickness) - set(self.plant_out)).pop()

    def solve_for(self, solved: dict[int, int]) -> int:
        """Return the energy at target, given a set of starting energies."""
        todo = set(self.plant_in)
        while True:
            # Find a plant with all the inputs already known.
            plant = next(plant for plant in todo if all(branch in solved for branch, _ in self.plant_in[plant]))
            todo.remove(plant)
            incoming = sum(thick * solved[branch_in] for branch_in, thick in self.plant_in[plant])
            solved[plant] = 0 if incoming < self.thickness[plant] else incoming
            if plant == self.target:
                return solved[plant]


def solve(part: int, data: str) -> int:
    """Solve the parts."""
    chunks = data.split("\n\n\n")
    garden = Garden(chunks[0])

    if part == 1:
        chunks.append(" ".join(["1"] * garden.num_inputs))

    schemas = [[int(i) for i in line.split()] for line in chunks[1].splitlines()]

    # Compute the target energy for each schema.
    results = [garden.solve_for(dict(enumerate(schema, 1))) for schema in schemas]
    if part < 3:
        return sum(results)

    # Solve for maximal energy by setting input values based on their output branch sign.
    most = garden.solve_for({plant: 1 if garden.plant_out[plant][0] > 0 else 0 for plant in garden.input_plants})

    return sum(most - result for result in results if result)


PARSER = parsers.parse_one_str
TEST_DATA = [
    """\
Plant 1 with thickness 1:
- free branch with thickness 1

Plant 2 with thickness 1:
- free branch with thickness 1

Plant 3 with thickness 1:
- free branch with thickness 1

Plant 4 with thickness 17:
- branch to Plant 1 with thickness 15
- branch to Plant 2 with thickness 3

Plant 5 with thickness 24:
- branch to Plant 2 with thickness 11
- branch to Plant 3 with thickness 13

Plant 6 with thickness 15:
- branch to Plant 3 with thickness 14

Plant 7 with thickness 10:
- branch to Plant 4 with thickness 15
- branch to Plant 5 with thickness 21
- branch to Plant 6 with thickness 34""",
    """\
Plant 1 with thickness 1:
- free branch with thickness 1

Plant 2 with thickness 1:
- free branch with thickness 1

Plant 3 with thickness 1:
- free branch with thickness 1

Plant 4 with thickness 10:
- branch to Plant 1 with thickness -25
- branch to Plant 2 with thickness 17
- branch to Plant 3 with thickness 12

Plant 5 with thickness 14:
- branch to Plant 1 with thickness 14
- branch to Plant 2 with thickness -26
- branch to Plant 3 with thickness 15

Plant 6 with thickness 150:
- branch to Plant 4 with thickness 5
- branch to Plant 5 with thickness 6


1 0 1
0 0 1
0 1 1""",
    """\
Plant 1 with thickness 1:
- free branch with thickness 1

Plant 2 with thickness 1:
- free branch with thickness 1

Plant 3 with thickness 1:
- free branch with thickness 1

Plant 4 with thickness 1:
- free branch with thickness 1

Plant 5 with thickness 8:
- branch to Plant 1 with thickness -8
- branch to Plant 2 with thickness 11
- branch to Plant 3 with thickness 13
- branch to Plant 4 with thickness -7

Plant 6 with thickness 7:
- branch to Plant 1 with thickness 14
- branch to Plant 2 with thickness -9
- branch to Plant 3 with thickness 12
- branch to Plant 4 with thickness 9

Plant 7 with thickness 23:
- branch to Plant 5 with thickness 17
- branch to Plant 6 with thickness 18


0 1 0 0
0 1 0 1
0 1 1 1
1 1 0 1""",
]
TESTS = [
    (1, TEST_DATA[0], 774),
    (2, TEST_DATA[1], 324),
    # (3, TEST_DATA[2], 946),
]

if __name__ == "__main__":
    helpers.run_solution(globals())
