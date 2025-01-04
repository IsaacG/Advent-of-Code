"""Everyone Codes Day N."""

LAUNCH_RANK = {"A": 1, "B": 2, "C": 3}


def solve(part: int, data: str, testing: bool) -> int:
    """Solve the parts."""
    if part == 3:
        return solve3(data, testing)

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

    ranking = 0
    while targets:
        candidates = {t for t in targets if t + 1j not in targets}
        rank, target = get_rank(launchers, candidates)
        assert target
        ranking += rank
        targets[target] -= 1
        if targets[target] == 0:
            del targets[target]
    return ranking


def get_rank(launchers, targets):
    min_power = (min(t.real for t in targets) - max(l.real for l in launchers.values())) // 4
    max_power = (max(t.real for t in targets) - min(l.real for l in launchers.values())) // 2
    for power in range(int(min_power), int(max_power)):
        for launcher, pos in launchers.items():
            shot = pos + 2 * power + power * 1j
            for target in targets:
                delta = target - shot
                if delta.real == -delta.imag:
                    return LAUNCH_RANK[launcher] * power, target


def solve3(data: str, testing: bool) -> int:
    total = 0
    fall = complex(-1, -1)

    def min_power(launcher, meteor):
        max_wait = int(min(min(meteor.real, meteor.imag), 2 * meteor.imag - meteor.real))
        for wait in range(max_wait + 1):
            meteor_after_wait = meteor + wait * fall
            if meteor_after_wait.real % 2 == 1:
                continue
            if meteor_after_wait.real < 0:
                continue
            impact_time = meteor_after_wait.real // 2
            impact = meteor_after_wait + impact_time * fall
            min_power = max(0, int(min((impact.real // 3) - 3, impact.imag - 3)))
            max_power = int(impact_time)

            for power in range(min_power, max_power + 1):
                time_left = impact_time
                shot_pos = launcher + complex(1, 1) * power
                time_left -= power
                horiz = min(time_left, power)
                shot_pos += complex(1, 0) * horiz
                time_left -= horiz
                down = time_left
                shot_pos += complex(1, -1) * down
                if shot_pos == impact:
                    # print(f"{launcher} {power=} will hit {meteor} with {wait=} at {impact}")
                    if meteor == complex(3981, 2517):
                        print(impact, power)
                    return impact.imag, power
        return 0, 0

    launchers = [(-1, complex(0, 0)), (-2, complex(0, 1)), (-3, complex(0, 2))]
    
    for line in data.splitlines():
        options = []
        meteor = complex(*[int(i) for i in line.split()])
        for mult, launcher in launchers:
            height, power = min_power(launcher, meteor)
            if power:
                options.append((height, mult * power))

        if not options:
            print(line, options)
        total += max(options)[1]

    got = int(-total)
    if not testing:
        assert len(str(got)) == 6
        assert got // 100000 != 4
    return got



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
