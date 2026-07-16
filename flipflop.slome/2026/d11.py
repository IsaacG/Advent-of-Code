"""FlipFlop Codes: N."""

import collections
import itertools
import more_itertools
import logging
from lib import helpers, parsers


def final_mass(blocks: list[str]) -> int:
    all_rules = []
    for data in blocks:
        above, main = data.replace("XX", "-1").splitlines()
        rule = {}
        for above, (left, src, right) in zip(above.strip().split(), more_itertools.chunked(main.strip().split(), 3)):
            rule[int(src)] = {complex(-1, 0): int(left), complex(0, 1): int(above), complex(1, 0): int(right)}
        all_rules.append(rule)

    all_stems = [set() for _ in all_rules]
    all_sprouts = [{complex(i * 10, 0): 0} for i in range(len(all_rules))]
    alive = [True] * len(all_rules)

    for age in range(100):
        combined_stems = set().union(*all_stems)
        for idx in range(len(all_rules)):
            if not alive[idx]:
                continue
            stems = all_stems[idx]
            sprouts = all_sprouts[idx]
            rules = all_rules[idx]
            exists = stems | set(sprouts)
            if age >= 5:
                needed_energy = 3 * len(exists)
                harvested = 0
                for stem in stems:
                    height = min(10, int(stem.imag) + 1)
                    above = 0
                    for i in range(1, 110):
                        if stem + i * 1j in combined_stems:
                            above += 1
                            if above == 3:
                                break
                    mult = 3 - above
                    harvested += height * mult
                if needed_energy > harvested:
                    # print(f"Tree {idx + 1} runs out of energy at age {age}, mass={len(exists)}")
                    alive[idx] = False

        for idx in range(len(all_rules)):
            combined_stems = set().union(*all_stems)
            combined_sprouts = set().union(*[set(i) for i in all_sprouts])
            combined_mass = combined_stems | combined_sprouts
            if not alive[idx]:
                continue
            stems = all_stems[idx]
            sprouts = all_sprouts[idx]
            rules = all_rules[idx]
            exists = stems | set(sprouts)

            new_growths = {}
            for pos, val in sprouts.items():
                for direction in {1, -1, 1j}:
                    neighbor = pos + direction
                    if neighbor in combined_mass:
                        continue
                    new_growths[neighbor] = max(new_growths.get(neighbor, -1), rules[val][direction])
            stems |= set(sprouts)
            sprouts = {pos: val for pos, val in new_growths.items() if val != -1}
            all_stems[idx] = stems
            all_sprouts[idx] = sprouts

        if age <= 12 and False:
            combined_stems = set().union(*all_stems)
            combined_sprouts = set().union(*[set(i) for i in all_sprouts])
            combined_mass = combined_stems | combined_sprouts
            min_x = int(min(i.real for i in combined_mass))
            max_x = int(max(i.real for i in combined_mass))
            print("Year: ", age)
            for y in range(age + 1, -1, -1):
                print("".join("@" if complex(x, y) in combined_sprouts else "#" if complex(x, y) in combined_stems else " " for x in range(min_x, max_x + 1)))
            print()


    mass = set()
    for stems in all_stems:
        mass |= stems
    for sprouts in all_sprouts:
        mass |= set(sprouts)
    return len(mass)


def solve(part: int, data: str) -> int:
    """Solve the parts."""
    blocks = data.split("\n\n")
    if part == 1:
        return sum(final_mass([block]) for block in blocks)
    if part == 2:
        return final_mass(blocks)


WANT = [1224, 1431]
PARSER = parsers.parse_one_str
TEST_DATA = ["""\
    02          XX          00
01  00  XX  01  01  02  XX  02  XX""",
    """\
    01          XX          XX
02  00  XX  XX  01  00  02  02  XX

    02          XX          00
01  00  XX  01  01  02  XX  02  XX""",
]
TESTS = [(i + 1, TEST_DATA[i], want) for i, want in enumerate(WANT)]
# TESTS = [
#     (1, TEST_DATA[0], None),
#     (2, TEST_DATA[1], None),
#     (3, TEST_DATA[2], None),
# ]

if __name__ == "__main__":
    helpers.run_solution(globals())
