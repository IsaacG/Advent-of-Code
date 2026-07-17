"""FlipFlop Codes: N."""

import collections
import itertools
import more_itertools
import sys
import logging
from lib import helpers, parsers

DIRECTIONS = [complex(-1), complex(0, 1), complex(1)]


def parse_rules(data: list[str]) -> list[dict[int, dict[complex, int]]]:
    """Parse the text-based rules into a dict."""
    rules = []
    for datum in data:
        rule = {}
        above, main = datum.replace("XX", "-1").splitlines()
        for above, (left, src, right) in zip(above.strip().split(), more_itertools.chunked(main.strip().split(), 3)):
            rule[int(src)] = {k: v for k, v in zip(DIRECTIONS, (int(i) for i in [left, above, right])) if v != -1}
        rules.append(rule)
    return rules


def survives(age, tree, all_stems):
    if age < 5:
        return True

    rules, stems, sprouts = (tree[i] for i in ["rules", "stems", "sprouts"])
    exists = stems | set(sprouts)
    needed_energy = 3 * len(exists)
    harvested = 0
    for stem in stems:
        height = min(10, int(stem.imag) + 1)
        above = min(3, sum(1 for i in all_stems[stem.real] if i > stem.imag))
        mult = 3 - above
        harvested += height * mult
    return needed_energy <= harvested


def simulate_generation(alive):
    dead = []
    all_stems = collections.defaultdict(set)
    all_matter = {sprout for tree in alive for sprout in tree["sprouts"]}

    for age in range(100):
        next_alive = []
        for tree in alive:
            if survives(age, tree, all_stems):
                next_alive.append(tree)
            else:
                dead.append(tree)
        alive = next_alive

        for tree in alive:
            new_growths = {}
            for pos, val in tree["sprouts"].items():
                for direction in DIRECTIONS:
                    neighbor = pos + direction
                    if neighbor not in all_matter and direction in tree["rules"][val]:
                        new_growths[neighbor] = max(new_growths.get(neighbor, -1), tree["rules"][val][direction])

            new_stems = tree["sprouts"]
            tree["stems"].update(new_stems)
            for stem in new_stems:
                all_stems[stem.real].add(stem.imag)

            tree["sprouts"] = new_growths
            all_matter.update(new_growths)

    return dead + alive


def collect_seeds(dead):
    # Collect all the seeds, grouped by x position.
    new_sprouts = collections.defaultdict(list)
    for tree in dead:
        for sprout in tree["sprouts"]:
            new_sprouts[int(sprout.real)].append(
                (
                    sprout.imag,
                    {
                        "rules": tree["rules"],
                        "stems": set(),
                        "sprouts": {complex(sprout.real, 0): 0},
                        "age": 0,
                    },
                )
            )
    # Take only the highest seed per x position.
    new_sprouts = {x: max(trees) for x, trees in new_sprouts.items()}
    # Sort seeds by x position.
    return [tree for x, (y, tree) in sorted(new_sprouts.items())]


def final_mass(blocks: list[str], loops=1) -> int:
    """Compute the growth of trees."""
    all_rules = parse_rules(blocks)
    new_sprouts = [
        {
            "rules": rules,
            "stems": set(),
            "sprouts": {complex(i * 10, 0): 0},
        } for i, rules in enumerate(all_rules)
    ]

    for loop in range(loops):
        dead = simulate_generation(new_sprouts)
        new_sprouts = collect_seeds(dead)

    return len({i for tree in dead for i in tree["stems"] | set(tree["sprouts"])})


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
