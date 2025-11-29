"""Everyone Codes Day N."""

import collections
import itertools
import functools
import math


def parse(data: str) -> tuple[list[int], list[list[str]]]:
    """Parse the input."""
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
    return distances, wheels


def solve(part: int, data: str) -> int | str:
    """Solve the parts."""
    distances, wheels = parse(data)
    # Wheels with only the eyes.
    eye_wheels = [[face[0] + face[2] for face in wheel] for wheel in wheels]
    wheel_lens = [len(wheel) for wheel in wheels]

    @functools.cache
    def points_for_positions(positions: tuple[int]) -> int:
        """Return the amount of points won for given wheel positions."""
        return sum(
            count - 2
            for count in collections.Counter(
                "".join(eyes[position] for eyes, position in zip(eye_wheels, positions))
            ).values()
            if count > 2
        )

    def part2() -> int:
        """Find cycle lengths and compute the points for each cycle and for the remainder steps. CRT?"""
        wheel_steps = [wheel_len // math.gcd(wheel_len, distance) for wheel_len, distance in zip(wheel_lens, distances)]
        combined_cycle = math.lcm(*wheel_steps)
        ic = [
                [
                    step % wheel_len
                    for step in range(distance, math.lcm(wheel_len, distance) + 1, distance)
                ]
                for eyes, wheel_len, distance in zip(eye_wheels, wheel_lens, distances)
        ]
        pulls = 202420242024
        eye_gen = zip(*[itertools.cycle(i) for i in ic])
        cycles, remainder = divmod(pulls, combined_cycle)
        total = 0
        remainder_points = 0
        for step in range(min(pulls, combined_cycle)):
            total += points_for_positions(tuple(next(eye_gen)))
            if step == remainder - 1:
                remainder_points = total
        return cycles * total + remainder_points

    @functools.cache
    def max_min(positions: tuple[int, ...], steps: int) -> tuple[int, int]:
        """Return the max and min points given a starting position and using the left lever. Dynamic programming."""
        if steps == 0:
            return 0, 0

        mins, maxes = [], []
        for offset in [0, -1, 1]:
            next_pos = tuple(
                (pos + offset + distance) % wlen
                for pos, distance, wlen in zip(positions, distances, wheel_lens)
            )
            got = points_for_positions(next_pos)
            a, b = max_min(next_pos, steps - 1)
            maxes.append(got + a)
            mins.append(got + b)
        return max(maxes), min(mins)

    if part == 1:
        return " ".join(wheel[(100 * distance) % len(wheel)] for wheel, distance in zip(wheels, distances))

    if part == 2:
        return part2()

    # Part 3
    got = max_min(tuple(0 for _ in wheels), 256)
    return " ".join(str(i) for i in got)


TEST_DATA = [
    """\
1,2,3

^_^ -.- ^,-
>.- ^_^ >.<
-_- -.- >.<
    -.^ ^_^
    >.>""",
    """\
1,2,3

^_^ -.- ^,-
>.- ^_^ >.<
-_- -.- ^.^
    -.^ >.<
    >.>""",
]
TESTS = [
    (1, TEST_DATA[0], ">.- -.- ^,-"),
    (2, TEST_DATA[0], 280014668134),
    (3, TEST_DATA[1], "627 128"),
]
