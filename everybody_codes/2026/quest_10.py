"""Everyone Codes Event 2026 Day 10."""

import collections
import itertools
from lib import helpers

ARROW_DIRECTIONS = helpers.ARROW_DIRECTIONS_T
rotate = helpers.rotate_counterclockwise


def solve(part: int, data: str, testing) -> int:
    """Solve the parts."""
    spaces = {pos for pos, char in data.chars.items() if char in set(ARROW_DIRECTIONS) | {"."}}
    ghosts = [
        (idx, pos, ARROW_DIRECTIONS[direction], 10000 if part == 2 else 1000000000000)
        for idx, (pos, direction) in enumerate(data.chars.items())
        if direction in ARROW_DIRECTIONS
    ]
    collisions = 0
    seen = {}
    skipped_rounds = 0

    for game_round in itertools.count(1):
        # Move ghosts one step.
        next_ghosts = []
        for gid, pos, direction, hp in ghosts:
            npos = pos[0] + direction[0], pos[1] + direction[1]
            # Wall collision
            if npos not in spaces:
                direction = rotate(*direction)
                npos = pos
                collisions += 1
                hp -= 1
            if hp > 0:
                next_ghosts.append((gid, npos, direction, hp))
        ghosts = next_ghosts

        # Ghost-on-ghost collisions
        shared = collections.Counter(pos for gid, pos, _, _ in ghosts)
        next_ghosts = []
        for gid, pos, direction, hp in ghosts:
            if shared[pos] > 1:
                collisions += 1
                direction = (-direction[0], -direction[1])  # double rotate
                hp -= 1
            if hp > 0:
                next_ghosts.append((gid, pos, direction, hp))
        ghosts = next_ghosts

        # End state check.
        if part == 1 and game_round == 10:
            return collisions
        if not ghosts:
            return game_round + skipped_rounds

        # Cycle detection
        fp = tuple(i for idx, pos, direction, hp in ghosts for i in (*pos, *direction))
        hitpoints = [hp for idx, pos, direction, hp in ghosts]
        if fp in seen:
            prior_round, prior_hps = seen[fp]
            # game rounds since this cycled
            rnd_stride = game_round - prior_round
            # number of cycles until a ghost vanishes
            steps = min(
                (current_hp - 1) // (prior_hp - current_hp)
                for current_hp, prior_hp in zip(hitpoints, prior_hps)
                if current_hp != prior_hp
            )
            # record a bunch of rounds skipped
            skipped_rounds += rnd_stride * steps
            # update ghost hp
            ghosts = [
                (idx, pos, direction, hp - (prior_hp - hp) * steps)
                for (idx, pos, direction, hp), prior_hp in zip(ghosts, prior_hps)
            ]
            # since the number of ghosts is about to change, the prior cache values can be flushed
            seen = {}

        seen[fp] = (game_round, hitpoints)


TEST_DATA = [
    """\
###########
#####.#####
###.....###
##.......##
##.>>.<<.##
#v...>...v#
##...v...##
##.......##
###.....###
#####.#####
###########""",
    """\
###########
#####.#####
###.....###
##.......##
##.>>.<<.##
#v...>...v#
##...v...##
##.......##
###.....###
#####.#####
###########""",
    """\
#######################
###########.###########
#######.^>.^.<^.#######
#####..<.>.v^>>^^<#####
####..v<^v.>.>v..^.####
###.................###
###.................###
##.......<...<.<....>##
##...v....>....v.v<.^##
##........###........##
##v......#####.......##
#.<......#####......>.#
##.......#####.......##
##........###........##
##...................##
##...................##
###.................###
###.................###
####...............####
#####.............#####
#######....v....#######
###########.###########
#######################""",
]
TESTS = [
    (1, TEST_DATA[0], 29),
    (2, TEST_DATA[1], 50000),
    (3, TEST_DATA[2], 13314695352588),
]

if __name__ == "__main__":
    helpers.run_solution(globals())
