"""FlipFlop Codes: N."""

import collections
import itertools
import more_itertools
import logging
from lib import helpers, parsers


def final_mass(blocks: list[str], loops=1) -> int:
    all_rules = []
    for data in blocks:
        above, main = data.replace("XX", "-1").splitlines()
        rule = {}
        for above, (left, src, right) in zip(above.strip().split(), more_itertools.chunked(main.strip().split(), 3)):
            rule[int(src)] = {complex(-1, 0): int(left), complex(0, 1): int(above), complex(1, 0): int(right)}
        all_rules.append(rule)

    alive = [
        {
            "name": str(i),
            "rules": rules,
            "stems": set(),
            "sprouts": {complex(i * 10, 0): 0},
            "age": 0,
        } for i, rules in enumerate(all_rules)
    ]
    dead = []
    dead_stems = set()
    dead_sprouts = set()

    for loop in range(loops):
        while alive:
            combined_stems = dead_stems.union(*[a["stems"] for a in alive])
            next_alive = []
            for tree in alive:
                tree["age"] += 1
                if tree["age"] > 5:
                    rules, stems, sprouts = (tree[i] for i in ["rules", "stems", "sprouts"])
                    exists = stems | set(sprouts)
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
                    if needed_energy <= harvested and tree["age"] <= 100:
                        next_alive.append(tree)
                    else:
                        # print(f"Tree {tree["name"]} runs out of energy at age {age}, mass={len(exists)}")
                        dead.append(tree)
                        dead_sprouts.update(tree["sprouts"])
                        dead_stems.update(tree["stems"])
                else:
                    next_alive.append(tree)
            alive = next_alive

            for tree in alive:
                rules, stems, sprouts = (tree[i] for i in ["rules", "stems", "sprouts"])
                combined_stems = dead_stems.union(*[a["stems"] for a in alive])
                combined_sprouts = dead_sprouts.union(*[set(a["sprouts"]) for a in alive])
                combined_mass = combined_stems | combined_sprouts
                exists = stems | set(sprouts)

                new_growths = {}
                for pos, val in sprouts.items():
                    for direction in {1, -1, 1j}:
                        neighbor = pos + direction
                        if neighbor in combined_mass:
                            continue
                        new_growths[neighbor] = max(new_growths.get(neighbor, -1), rules[val][direction])
                tree["stems"] |= set(sprouts)
                tree["sprouts"] = {pos: val for pos, val in new_growths.items() if val != -1}

        # Reset for the next loop
        if loop + 1 == loops:
            break

        new_sprouts = collections.defaultdict(list)
        for tree in dead:
            for sprout in tree["sprouts"]:
                new_sprouts[int(sprout.real)].append(
                    (
                        sprout.imag,
                        {
                            "name": tree["name"],
                            "rules": tree["rules"],
                            "stems": set(),
                            "sprouts": {complex(sprout.real, 0): 0},
                            "age": 0,
                        },
                    )
                )
        new_sprouts = {x: max(trees) for x, trees in new_sprouts.items()}
        alive = [tree for x, (y, tree) in sorted(new_sprouts.items())]
        dead = []
        dead_stems = set()
        dead_sprouts = set()



    mass = dead_stems | dead_sprouts
    for tree in alive:
        mass |= tree["stems"]
        mass |= set(tree["sprouts"])
    return len(mass)


def solve(part: int, data: str) -> int:
    """Solve the parts."""
    blocks = data.split("\n\n")
    if part == 1:
        return sum(final_mass([block]) for block in blocks)
    if part == 2:
        return final_mass(blocks)
    if part == 3:
        return final_mass(blocks, loops=3)


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
TESTS = [
    (1, TEST_DATA[0], 1224),
    (2, TEST_DATA[1], 1431),
    (3, TEST_DATA[1], 4122),
]

if __name__ == "__main__":
    helpers.run_solution(globals())
