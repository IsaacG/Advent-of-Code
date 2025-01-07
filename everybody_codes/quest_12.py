"""Everyone Codes Day N."""

LAUNCH_RANK = {"A": 1, "B": 2, "C": 3}


def solve(part: int, data: str) -> int:
    """Solve the parts."""
    if part == 3:
        return solve3(data)

    # Parse the input for parts 1, 2
    launchers = {}
    targets = {}
    ground = set()
    for y, line in enumerate(reversed(data.splitlines())):
        for x, char in enumerate(line):
            if char in "ABC":
                launchers[char] = complex(x, y)
            elif char in "=":
                ground.add(complex(x, y))
            elif char in "T":
                targets[complex(x, y)] = 1
            elif char in "H":
                targets[complex(x, y)] = 2

    total = 0
    while targets:
        # Find a target we can hit with minimal power.
        candidates = {t for t in targets if t + 1j not in targets}
        rank, target = get_rank_and_target(launchers, candidates)
        total += rank
        # Weaken/remove the target.
        targets[target] -= 1
        if targets[target] == 0:
            del targets[target]
    return total


def get_rank_and_target(launchers: dict[str, int], targets: set[complex]) -> tuple[int, complex]:
    """Return the minimum power/rank that can be used to hit a target, along with the target."""
    min_power = (min(t.real for t in targets) - max(l.real for l in launchers.values())) // 3
    max_power = (max(t.real for t in targets) - min(l.real for l in launchers.values())) // 2
    for power in range(int(min_power), int(max_power)):
        for launcher, pos in launchers.items():
            # Compute the location of the shot right before it starts dropping.
            shot = pos + 2 * power + power * 1j
            # Check if any target is diagonal from that position and will be hit.
            for target in targets:
                delta = target - shot
                if delta.real == -delta.imag:
                    return LAUNCH_RANK[launcher] * power, target


def solve3(data: str) -> int:
    """Solve part 3."""

    def min_power(launcher, meteor):
        # After time t, the height h(t) = meteor_y - t
        # At the maximum (or, any) wait, we need h(t) >= (meteor_x - t) / 2 in order to hit the meteor before it hits the ground.
        # meteor_y - t >= (meteor_x - t) / 2
        # 2 * (meteor_y - t) >= meteor_x - t
        # 2 * meteor_y >= meteor_x + t
        # t <= 2 * meteor_y - meteor_x
        max_wait = int(2 * meteor.imag - meteor.real)
        # The meteor needs a discrete collision. The x must be even to collide. This allows us to step by 2.
        if meteor.real % 2:
            meteor += complex(-1, -1)
        for wait in range(0, max_wait + 1, 2):
            # impact = (meteor + fall) / 2
            time_to_impact = (wait + meteor.real) // 2
            impact = meteor + time_to_impact * complex(-1, -1)
            distance_to_impact = int(impact.real)
            min_power = int(distance_to_impact // 3)

            for power in range(min_power, distance_to_impact + 1):
                shot_pos = launcher + complex(1, 1) * power
                time_left = distance_to_impact - power
                horiz = min(time_left, power)
                shot_pos += complex(1, 0) * horiz
                time_left -= horiz
                shot_pos += complex(1, -1) * time_left
                if shot_pos == impact:
                    return impact.imag, power
        return 0, 0

    launchers = [(-1, complex(0, 0)), (-2, complex(0, 1)), (-3, complex(0, 2))]
    
    total = 0
    for line in data.splitlines():
        options = []
        meteor = complex(*[int(i) for i in line.split()])
        for mult, launcher in launchers:
            height, power = min_power(launcher, meteor)
            if power:
                options.append((height, mult * power))

        total += max(options)[1]

    return -total



TEST_DATA = [
    """\
.............
.C...........
.B......T....
.A......T.T..
=============""",
    """\
.............
.C...........
.B......H....
.A......T.H..
=============""",
    """\
6 5
6 7
10 5""",
    "5 5",

]
TESTS = [
    (1, TEST_DATA[0], 13),
    (2, TEST_DATA[1], 22),
    (3, TEST_DATA[2], 11),
    (3, TEST_DATA[3], 2),
]
