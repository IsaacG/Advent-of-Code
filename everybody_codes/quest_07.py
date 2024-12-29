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
    rotations = [1j, -1j]
    chars = {}
    for y, line in enumerate(diagram.splitlines()):
        for x, char in enumerate(line):
            if char == " ":
                continue
            chars[complex(x, y)] = char
            if char == "S":
                pos = complex(x, y)
    direction = complex(1, 0)
    track_actions = []
    while True:
        if pos + direction not in chars:
            for rotate in rotations:
                if pos + direction * rotate in chars:
                    direction *= rotate
                    break
            else:
                raise RuntimeError()
        pos += direction
        track_actions.append(chars[pos])
        if chars[pos] == "S":
            return track_actions


def solve(part: int, data: str, testing: bool) -> int:
    collects = {}
    if part == 1:
        for line in data.splitlines():
            name, actions = line.split(":")
            collected = 0
            power = 10
            for _, action in zip(range(10), itertools.cycle(actions.split(","))):
                if action == "+":
                    power += 1
                elif action == "-" and power:
                    power -= 1
                collected += power
            collects[name] = collected
        return "".join(sorted(collects, key=lambda x: collects[x], reverse=True))
    if part == 2:
        track_actions = track(TRACK2[testing])
        for line in data.splitlines():
            name, actions = line.split(":")
            collected = 0
            power = 10
            for track_action, device_action in zip(track_actions * 10, itertools.cycle(actions.split(","))):
                if track_action in "+-":
                    action = track_action
                else:
                    action = device_action
                if action == "+":
                    power += 1
                elif action == "-" and power:
                    power -= 1
                collected += power
            collects[name] = collected
        return "".join(sorted(collects, key=lambda x: collects[x], reverse=True))
    if part == 3:
        track_actions = track(TRACK3) * 2024
        for line in data.splitlines():
            name, actions = line.split(":")
            collected = 0
            power = 10
            for track_action, device_action in zip(track_actions, itertools.cycle(actions.split(","))):
                if track_action in "+-":
                    action = track_action
                else:
                    action = device_action
                if action == "+":
                    power += 1
                elif action == "-" and power:
                    power -= 1
                collected += power
            collects[name] = collected
        assert set(collects) == {"A"}
        threshold = collects["A"]
        options = set(itertools.permutations("+" * 5 + "-=" * 3))
        count = 0
        for actions in options:
            collected = 0
            power = 10
            for track_action, device_action in zip(track_actions, itertools.cycle(actions)):
                if track_action in "+-":
                    action = track_action
                else:
                    action = device_action
                if action == "+":
                    power += 1
                elif action == "-" and power:
                    power -= 1
                collected += power
            if collected > threshold:
                count += 1
        return count


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
