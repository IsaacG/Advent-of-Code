#!/bin/python
"""Advent of Code, Day 25: Full of Hot Air. Convert from base 4 to 10 and back again!"""

from lib import aoc

SAMPLE = [
    """\
1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122""",  """\
        1              1
        2              2
        3             1=
        4             1-
        5             10
        6             11
        7             12
        8             2=
        9             2-
       10             20
       15            1=0
       20            1-0
     2022         1=11-2
    12345        1-0---0
314159265  1121-1110-1=0"""
]

LineType = str
InputType = list[LineType]
DECODER = {"2": 2, "1": 1, "0": 0, "-": -1, "=": -2}
ENCODER = {v: k for k, v in DECODER.items()}


class Day25(aoc.Challenge):
    """Day 25: Full of Hot Air."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want="2=-1=0"),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=aoc.TEST_SKIP),
    ]

    def encode(self, dec: int) -> str:
        """Return the SNAFU encoding of a number."""
        out = []
        while dec:
            dec, rem = divmod(dec, 5)
            if rem > 2:
                dec += 1
                rem -= 5
            out.append(ENCODER[rem])
        return "".join(reversed(out))

    def decode(self, snafu: str) -> int:
        """Return the integer value of a SNAFU encoded number."""
        total = 0
        for char in snafu:
            total = total * 5 + DECODER[char]
        return total

    def pre_run(self, _: InputType) -> None:
        """Run some tests."""
        for line in SAMPLE[1].splitlines():
            decimal, snafu = line.strip().split()
            assert int(decimal) == self.decode(snafu)
            msg = f"encode({decimal}) = {self.encode(int(decimal))}, want {snafu}"
            assert snafu == self.encode(int(decimal)), msg

    def part1(self, puzzle_input: InputType) -> str:
        """Return the SNAFU-encoded sum of SNAFU values."""
        return self.encode(sum(self.decode(line) for line in puzzle_input))

    def part2(self, puzzle_input: InputType) -> int:
        """Placeholder."""
        return 1
