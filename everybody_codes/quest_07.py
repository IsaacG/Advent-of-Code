import collections.abc
import itertools


TRACK2 = {
    True: """\
S+===
-   +
=+=-+""",
    False: """\
S-=++=-==++=++=-=+=-=+=+=--=-=++=-==++=-+=-=+=-=+=+=++=-+==++=++=-=-=--
-                                                                     -
=                                                                     =
+                                                                     +
=                                                                     +
+                                                                     =
=                                                                     =
-                                                                     -
--==++++==+=+++-=+=-=+=-+-=+-=+-=+=-=+=--=+++=++=+++==++==--=+=++==+++-""",
}

TRACK3 = """\
S+= +=-== +=++=     =+=+=--=    =-= ++=     +=-  =+=++=-+==+ =++=-=-=--
- + +   + =   =     =      =   == = - -     - =  =         =-=        -
= + + +-- =-= ==-==-= --++ +  == == = +     - =  =    ==++=    =++=-=++
+ + + =     +         =  + + == == ++ =     = =  ==   =   = =++=
= = + + +== +==     =++ == =+=  =  +  +==-=++ =   =++ --= + =
+ ==- = + =   = =+= =   =       ++--          +     =   = = =--= ==++==
=     ==- ==+-- = = = ++= +=--      ==+ ==--= +--+=-= ==- ==   =+=    =
-               = = = =   +  +  ==+ = = +   =        ++    =          -
-               = + + =   +  -  = + = = +   =        +     =          -
--==++++==+=+++-= =-= =-+-=  =+-= =-= =--   +=++=+++==     -=+=++==+++-"""


def track(diagram: str) -> list[str]:
    """Parse a track into a list of actions."""
    # Convert the track to a coord map.
    chars = {}
    for y, line in enumerate(diagram.splitlines()):
        for x, char in enumerate(line):
            if char == " ":
                continue
            chars[complex(x, y)] = char
            if char == "S":
                pos = complex(x, y)
    # Walk the track from S to S.
    rotations = [1j, -1j]
    direction = complex(1, 0)
    track_actions = []
    while True:
        if pos + direction not in chars:
            direction *= next(
                rotate
                for rotate in rotations
                if pos + direction * rotate in chars
            )
        pos += direction
        track_actions.append(chars[pos])
        if chars[pos] == "S":
            return track_actions


def race(actions: collections.abc.Iterable[str]) -> int:
    """Return the power collected by executing a sequence of actions."""
    collected = 0
    power = 10
    for action in actions:
        if action == "+":
            power += 1
        elif action == "-" and power:
            power -= 1
        collected += power
    return collected


def combine_actions(actions: collections.abc.Iterable[tuple[str, str]]) -> collections.abc.Iterable[str]:
    """Combine track and device actions."""
    for track_action, device_action in actions:
        yield track_action if track_action in "+-" else device_action


def solve(part: int, data: str, testing: bool) -> int:
    if part in [1, 2]:
        if part == 1:
            racer = lambda x: race(itertools.islice(itertools.cycle(x.split(",")), 10))
        else:
            track_actions = track(TRACK2[testing])
            racer = lambda x: race(combine_actions(zip(track_actions * 10, itertools.cycle(actions.split(",")))))
        collects = {}
        for line in data.splitlines():
            name, actions = line.split(":")
            collects[name] = racer(actions)
        return "".join(sorted(collects, key=lambda x: collects[x], reverse=True))
    if part == 3:
        # 2024 == 184 * 11
        # Running the track 2024 times would give 184x the result of 11 loops.
        # When testing patterns, 11 loops is sufficient.
        track_actions = track(TRACK3) * 11
        racer = lambda x: race(combine_actions(zip(track_actions, itertools.cycle(x))))
        threshold = racer(data.split(":")[1].split(","))
        return sum(
            racer(actions) > threshold
            for actions in set(itertools.permutations("+" * 5 + "-=" * 3))
        )


TEST_DATA = [
    """\
A:+,-,=,=
B:+,=,-,+
C:=,-,+,+
D:=,=,=,+""",
    """\
A:+,-,=,=
B:+,=,-,+
C:=,-,+,+
D:=,=,=,+""",
]
TESTS = [
    (1, TEST_DATA[0], "BDCA"),
    (2, TEST_DATA[1], "DCBA"),
    # (3, TEST_DATA[2], None),
]
