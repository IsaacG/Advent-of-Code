"""Everyone Codes Day N."""

from __future__ import annotations

import collections
import itertools


def rolly_die(data: str) -> collections.abc.Generator[int, None, None]:
    """Generate pseudo-random die rolls."""
    w = data.split()
    faces = [int(a) for a in w[1].removesuffix("]").split("[")[1].split(",")]
    seed = int(w[2].split("=")[1])
    pulse = seed
    roll_number = 1
    cur = 0
    num = len(faces)

    while True:
        spin = roll_number * pulse
        cur = (cur + spin) % num
        pulse = ((pulse + spin) % seed) + 1 + roll_number + seed
        roll_number += 1
        yield faces[cur]


def solve(part: int, data: str) -> int | str:
    """Play games with the pseudo-random dice."""
    # Roll dice until we get 10000 points. Return number of rolls.
    if part == 1:
        dice = [rolly_die(i) for i in data.splitlines()]
        points = 0
        for roll in itertools.count(1):
            points += sum(next(die) for die in dice)
            if points >= 10000:
                return roll

    lines, board = data.split("\n\n")
    dice = [rolly_die(i) for i in lines.splitlines()]

    # Return the order players makes it down a straight board.
    if part == 2:
        # Track player dice and what numbers they need to finish the came.
        todo = {
            player: (die, [int(i) for i in reversed(board)])
            for player, die in enumerate(dice, 1)
        }
        # Keep rolling while players are on the board.
        done = []
        while todo:
            for player, (die, remaining) in list(todo.items()):
                if next(die) == remaining[-1]:
                    remaining.pop()
                    if not remaining:
                        # Record players that get to the end.
                        done.append(player)
                        del todo[player]
        return ",".join(str(i) for i in done)

    # Part 3
    locations = collections.defaultdict(set)
    for y, row in enumerate(board.splitlines()):
        for x, num in enumerate(row):
            locations[int(num)].add(complex(x, y))

    # Valid moves: right left up down stay
    deltas = {complex(0, 0), complex(1, 0), complex(-1, 0), complex(0, 1), complex(0, -1)}
    seen = set()
    # For each die, compute all possible coins that can be collected.
    # Use the rolls to determine valid/useful next positions.
    for die in dice:
        roll = next(die)
        positions = locations[roll]
        while positions:
            seen.update(positions)
            roll = next(die)
            positions = {
                position + delta
                for position in positions
                for delta in deltas
                if position + delta in locations[roll]
            }
    if False:
        height = len(board.splitlines())
        width = len(board.splitlines()[0])
        for y in range(height):
            print("".join("#" if complex(x, y) in seen else " " for x in range(width)))

    return len(seen)


TEST_DATA = [
    """\
1: faces=[1,2,3,4,5,6] seed=7
2: faces=[-1,1,-1,1,-1] seed=13
3: faces=[9,8,7,8,9] seed=17""",
    """\
1: faces=[1,2,3,4,5,6,7,8,9] seed=13
2: faces=[1,2,3,4,5,6,7,8,9] seed=29
3: faces=[1,2,3,4,5,6,7,8,9] seed=37
4: faces=[1,2,3,4,5,6,7,8,9] seed=43

51257284""",
    """\
1: faces=[1,2,3,4,5,6,7,8,9] seed=13

1523758297
4822941583
7627997892
4397697132
1799773472""",
    """\
1: faces=[1,2,3,4,5,6,7,8,9] seed=339211
2: faces=[1,2,3,4,5,6,7,8,9] seed=339517
3: faces=[1,2,3,4,5,6,7,8,9] seed=339769
4: faces=[1,2,3,4,5,6,7,8,9] seed=339049
5: faces=[1,2,3,4,5,6,7,8,9] seed=338959
6: faces=[1,2,3,4,5,6,7,8,9] seed=340111
7: faces=[1,2,3,4,5,6,7,8,9] seed=339679
8: faces=[1,2,3,4,5,6,7,8,9] seed=339121
9: faces=[1,2,3,4,5,6,7,8,9] seed=338851

94129478611916584144567479397512595367821487689499329543245932151
45326719759656232865938673559697851227323497148536117267854241288
44425936468288462848395149959678842215853561564389485413422813386
64558359733811767982282485122488769592428259771817485135798694145
17145764554656647599363636643624443394141749674594439266267914738
89687344812176758317288229174788352467288242171125512646356965953
72436836424726621961424876248346712363842529736689287535527512173
18295771348356417112646514812963612341591986162693455745689374361
56445661964557624561727322332461348422854112571195242864151143533
77537797151985578367895335725777225518396231453691496787716283477
37666899356978497489345173784484282858559847597424967325966961183
26423131974661694562195955939964966722352323745667498767153191712
99821139398463125478734415536932821142852955688669975837535594682
17768265895455681847771319336534851247125295119363323122744953158
25655579913247189643736314385964221584784477663153155222414634387
62881693835262899543396571369125158422922821541597516885389448546
71751114798332662666694134456689735288947441583123159231519473489
94932859392146885633942828174712588132581248183339538341386944937
53828883514868969493559487848248847169557825166338328352792866332
54329673374115668178556175692459528276819221245996289611868492731
97799599164121988455613343238811122469229423272696867686953891233
56249752581283778997317243845187615584225693829653495119532543712
39171354221177772498317826968247939792845866251456175433557619425
56425749216121421458547849142439211299266255482219915528173596421
48679971256541851497913572722857258171788611888347747362797259539
32676924489943265499379145361515824954991343541956993467914114579
45733396847369746189956225365375253819969643711633873473662833395
42291594527499443926636288241672629499242134451937866578992236427
47615394883193571183931424851238451485822477158595936634849167455
16742896921499963113544858716552428241241973653655714294517865841
57496921774277833341488566199458567884285639693339942468585269698
22734249697451127789698862596688824444191118289959746248348491792
28575193613471799766369217455617858422158428235521423695479745656
74234343226976999161289522983885254212712515669681365845434541257
43457237419516813368452247532764649744546181229533942414983335895""",
]
TESTS = [
    (1, TEST_DATA[0], 844),
    (2, TEST_DATA[1], "1,3,4,2"),
    (3, TEST_DATA[2], 33),
    (3, TEST_DATA[3], 1125),
]
