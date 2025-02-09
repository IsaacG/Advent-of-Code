"""Everyone Codes Day N."""

import collections
import itertools
import functools
import math


def solve(part: int, data: str) -> int:
    """Solve the parts."""
    blocks = data.split("\n\n")
    lines = blocks[1].splitlines()
    distances = [int(i) for i in blocks[0].split(",")]
    count = (len(lines[1]) + 1) // 4
    wheels = []
    for i in range(count):
        faces = []
        start = i * 4
        for line in lines:
            if len(line) < start or line[start] == " ":
                break
            faces.append(line[start:start + 3])
        wheels.append(faces)

    if part == 1:
        return " ".join(wheel[(100 * distance) % len(wheel)] for wheel, distance in zip(wheels, distances))

    eye_wheels = [[face[0] + face[2] for face in wheel] for wheel in wheels]

    @functools.cache
    def points_for_positions(positions: list[int]) -> int:
        return sum(
            count - 2
            for count in collections.Counter(
                "".join(eyes[position]) for eyes, position in zip(eye_wheels, positions)
            ).values()
            if count > 2
        )

    if part == 2:
        wheel_lens = [len(wheel) for wheel in wheels]
        wheel_steps = [wheel_len // math.gcd(wheel_len, distance) for wheel_len, distance in zip(wheel_lens, distances)]
        # print(f"{wheel_steps=}")
        assert len(eye_wheels) == len(wheel_lens) == len(distances)
        # print(eye_wheels)
        # print(list(zip(eye_wheels, wheel_lens, distances)))
        combined_cycle = math.lcm(*wheel_steps)
        # print(f"{combined_cycle=}")
        ic = [
                [
                    eyes[step % wheel_len]
                    for step in range(distance, math.lcm(wheel_len, distance) + 1, distance)
                ]
                for eyes, wheel_len, distance in zip(eye_wheels, wheel_lens, distances)
        ]
        pulls = 202420242024
        eye_gen = zip(*[itertools.cycle(i) for i in ic])
        cycles, remainder = divmod(pulls, combined_cycle)
        total = 0
        remainder_points = 0
        for step in range(combined_cycle):
            eyes = list(next(eye_gen))
            counts = collections.Counter(a for b in eyes for a in b)
            # print(eyes, counts)
            for count in counts.values():
                if count > 2:
                    total += count - 2
            # print(f"{step} -> {total}")
            if step == remainder - 1:
                remainder_points = total
                # print(f"{step=} remainder {remainder_points}")
        got = cycles * total + remainder_points
        assert got in [280014668134, 109992786835]
        return got

    @functools.cache
    def min_max(positions, steps):
        if steps == 0:
            return 0, 0

        for offset in [0, -1, 1]:
            counts = collections.Counter(a for b in eyes for a in b)
            # print(eyes, counts)
            for count in counts.values():
                if count > 2:
                    total += count - 2



TEST_DATA = """\
1,2,3

^_^ -.- ^,-
>.- ^_^ >.<
-_- -.- >.<
    -.^ ^_^
    >.>"""
TESTS = [
    (1, TEST_DATA, ">.- -.- ^,-"),
    (2, TEST_DATA, 280014668134),
    (3, TEST_DATA, "627 128"),
]
