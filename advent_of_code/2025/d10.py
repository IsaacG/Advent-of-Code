#!/bin/python
"""Advent of Code, Day 10: Factory."""
from __future__ import annotations

import collections
import functools
import itertools
import logging

import z3

from lib import aoc

SAMPLE = [
    """\
[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}""",  # 0
]

LineType = int
InputType = list[LineType]
log = logging.info


class Day10(aoc.Challenge):
    """Day 10: Factory."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE[0], want=7),
        aoc.TestCase(part=2, inputs=SAMPLE[0], want=33),
        # aoc.TestCase(part=2, inputs=SAMPLE[0], want=aoc.TEST_SKIP),
    ]

    # INPUT_PARSER = aoc.parse_ints
    # INPUT_PARSER = aoc.parse_one_str
    # INPUT_PARSER = aoc.parse_one_str_per_line
    # INPUT_PARSER = aoc.parse_multi_str_per_line
    # INPUT_PARSER = aoc.parse_one_int
    # INPUT_PARSER = aoc.parse_one_int_per_line
    # INPUT_PARSER = aoc.parse_ints_one_line
    # INPUT_PARSER = aoc.parse_ints_per_line
    # INPUT_PARSER = aoc.parse_re_group_str(r"(a) .* (b) .* (c)")
    # INPUT_PARSER = aoc.parse_re_findall_str(r"(a|b|c)")
    # INPUT_PARSER = aoc.parse_multi_mixed_per_line
    # INPUT_PARSER = aoc.parse_re_group_mixed(r"(foo) .* (\d+)")
    # INPUT_PARSER = aoc.parse_re_findall_mixed(r"\d+|foo|bar")
    # INPUT_PARSER = aoc.ParseBlocks([aoc.parse_one_str_per_line, aoc.parse_re_findall_int(r"\d+")])
    # INPUT_PARSER = aoc.ParseOneWord(aoc.Board.from_int_block)
    # INPUT_PARSER = aoc.CoordinatesParser(chars=None, origin_top_left=True)
    # ---
    # (width, height), start, garden, rocks = puzzle_input
    # max_x, max_y = width - 1, height - 1

    def part1(self, puzzle_input: InputType) -> int:
        # print("\n".join(["==="] + [f"{k}={v!r}" for k, v in locals().items()] + ["==="]))
        vals = []
        for line in puzzle_input:
            want, *buttons_, joltage = line
            target = int(want[1:-1].replace(".", "0").replace("#", "1")[::-1], 2)
            buttons = []
            for b in buttons_:
                buttons.append(sum((1 << int(i)) for i in b[1:-1].split(",")))
            print(f"{line=}, {target=}, {buttons=}")

            def get_steps():
                for i in range(0, len(buttons)):
                    for c in itertools.combinations(buttons, i):
                        result = 0
                        for a in c:
                            result ^= a
                        if result == target:
                            return i

            vals.append(get_steps())
            print(vals[-1])

            """
            q = collections.deque()
            q.append((0, 0))
            seen = {0}
            while q:
                steps, state = q.popleft()
                if not q:
                    print("q empty at", steps, seen, buttons)
                assert steps < 100
                if state == target:
                    vals.append(steps)
                    print(target, steps)
                    break
                steps += 1
                for b in buttons:
                    r = state ^ b
                    if r not in seen:
                        seen.add(r)
                        q.append((steps, state ^ b))
                        """
        print(vals)
        return sum(vals)



    def part2(self, puzzle_input: InputType) -> int:
        # print("\n".join(["==="] + [f"{k}={v!r}" for k, v in locals().items()] + ["==="]))
        vals = []
        for line in puzzle_input:
            want, *buttons_, joltage_ = line
            buttons = []
            for b in buttons_:
                buttons.append([int(i) for i in b[1:-1].split(",")])
            joltage = [int(i) for i in joltage_[1:-1].split(",")]
            # print(f"{line=}, {target=}, {buttons=}")

            zb = [z3.Int(f"b{idx}") for idx, b in enumerate(buttons)]
            ans = z3.Int("ans")
            # zj = [z3.Int(f"j{idx}") for idx in range(len(joltage))]
            s = z3.Optimize()
            for b in zb:
                s.add(b >= 0)
            for jidx, j in enumerate(joltage):
                s.add(z3.Sum([zb[idx] for idx, b in enumerate(buttons) if jidx in b]) == j)
            s.add(ans == z3.Sum(zb))
            s.minimize(ans)
            assert s.check() == z3.sat
            a = s.model()
            print(a)
            vals.append(a[ans].as_long())
            continue
            

            q = collections.deque()
            q.append((0, tuple([0]*len(target))))
            seen = set()
            seen.add(tuple([0]*len(target)))
            print(target, seen)
            while q:
                steps, jolts = q.popleft()
                if jolts == target:
                    vals.append(steps)
                    break
                steps += 1

                for b in buttons:
                    new = list(jolts)
                    for i in b:
                        new[i] += 1
                    if any(i > j for i, j in zip(new, target)):
                        continue
                    new = tuple(new)
                    if new not in seen:
                        seen.add(new)
                        q.append((steps, new))
        print(vals)
        return sum(vals)


    # def solver(self, puzzle_input: InputType, part_one: bool) -> int | str:

    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        return super().input_parser(puzzle_input)
        return puzzle_input.splitlines()
        return puzzle_input
        return [int(i) for i in puzzle_input.splitlines()]
        mutate = lambda x: (x[0], int(x[1])) 
        return [mutate(line.split()) for line in puzzle_input.splitlines()]
        # Words: mixed str and int
        return [
            tuple(
                int(i) if i.isdigit() else i
                for i in line.split()
            )
            for line in puzzle_input.splitlines()
        ]
        # Regex splitting
        patt = re.compile(r"(.*) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds.")
        return [
            tuple(
                int(i) if i.isdigit() else i
                for i in patt.match(line).groups()
            )
            for line in puzzle_input.splitlines()
        ]

# vim:expandtab:sw=4:ts=4
