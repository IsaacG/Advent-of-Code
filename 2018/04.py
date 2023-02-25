#!/bin/python
"""Advent of Code, Day 4: Repose Record."""
from __future__ import annotations

import collections
import datetime
import functools
import itertools
import heapq
import math
import re

import typer
from lib import aoc

SAMPLE = """\
[1518-11-01 00:00] Guard #10 begins shift
[1518-11-01 00:05] falls asleep
[1518-11-01 00:25] wakes up
[1518-11-01 00:30] falls asleep
[1518-11-01 00:55] wakes up
[1518-11-01 23:58] Guard #99 begins shift
[1518-11-02 00:40] falls asleep
[1518-11-02 00:50] wakes up
[1518-11-03 00:05] Guard #10 begins shift
[1518-11-03 00:24] falls asleep
[1518-11-03 00:29] wakes up
[1518-11-04 00:02] Guard #99 begins shift
[1518-11-04 00:36] falls asleep
[1518-11-04 00:46] wakes up
[1518-11-05 00:03] Guard #99 begins shift
[1518-11-05 00:45] falls asleep
[1518-11-05 00:55] wakes up"""

LineType = int
InputType = list[LineType]


class Day04(aoc.Challenge):
    """Day 4: Repose Record."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}
    # PARAMETERIZED_INPUTS = [5, 50]

    TESTS = [
        aoc.TestCase(inputs=SAMPLE, part=1, want=240),
        aoc.TestCase(inputs=SAMPLE, part=2, want=4455),
        # aoc.TestCase(inputs=SAMPLE[0], part=2, want=aoc.TEST_SKIP),
    ]

    def part1(self, parsed_input: InputType) -> int:
        asleep = {
            guard_id: sum(end - start for start, end in v)
            for guard_id, v in parsed_input.items()
        }
        max_sleep = max(asleep.values())
        guards = [k for k, v in asleep.items() if v == max_sleep]
        assert len(guards) == 1
        guard_id = guards[0]

        intervals = sorted(parsed_input[guard_id])
        count = 0
        max_count = 0
        max_time = 0
        awake = []

        for start, end in intervals:
            while awake and awake[0] <= start:
                count -= 1
                heapq.heappop(awake)
            count += 1
            heapq.heappush(awake, end)
            if count > max_count:
                max_count, max_time = count, start
        return guard_id * max_time

    def part2(self, parsed_input: InputType) -> int:
        champion_count, champion_val = 0, 0
        for guard_id, intervals in parsed_input.items():
            intervals.sort()

            count = 0
            max_count = 0
            max_time = 0
            awake = []

            for start, end in intervals:
                while awake and awake[0] <= start:
                    count -= 1
                    heapq.heappop(awake)
                count += 1
                heapq.heappush(awake, end)
                if count > max_count:
                    max_count, max_time = count, start

            if max_count > champion_count:
                champion_count = max_count
                champion_val = guard_id * max_time
        return champion_val

    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        lines = sorted(puzzle_input.splitlines())

        one_day = datetime.timedelta(days=1)
        log_pattern = re.compile(r"^\[([0-9-]+) (\d\d):(\d\d)\] (.*)$")
        begin_pattern = re.compile(r"^Guard #(\d+) begins shift$")
        sleeping: dict[int, list[tuple[int, int]]] = collections.defaultdict(list)

        guard_id = 0
        start = 0
        awake = False
        prev_date = datetime.date.today()

        for line in lines:
            m = log_pattern.match(line)
            assert m is not None, line
            date_str, hh_str, mm_str, rest = m.groups()
            date = datetime.datetime.strptime(date_str, "1518-%m-%d").date()
            hh, mm = int(hh_str), int(mm_str)
            if hh != 0:
                assert rest.endswith("begins shift") and hh == 23
                hh, mm = 0, 0
                date = date + one_day

            if rest.endswith("begins shift"):
                m = begin_pattern.match(rest)
                assert m is not None
                if guard_id and not awake:
                    sleeping[guard_id].append((start, 59))
                new_id = int(m.group(1))
                guard_id, start, awake = new_id, mm, True
            elif line.endswith("wakes up"):
                assert not awake
                awake = True
                sleeping[guard_id].append((start, mm))
            elif line.endswith("falls asleep"):
                assert awake
                awake = False
                start = mm
        return sleeping


"""
[1518-11-01 00:00] Guard #10 begins shift
[1518-11-01 00:05] falls asleep
[1518-11-01 00:25] wakes up
[1518-11-01 00:30] falls asleep
[1518-11-01 00:55] wakes up
[1518-11-01 23:58] Guard #99 begins shift
[1518-11-02 00:40] falls asleep
[1518-11-02 00:50] wakes up
[1518-11-03 00:05] Guard #10 begins shift
[1518-11-03 00:24] falls asleep
[1518-11-03 00:29] wakes up
[1518-11-04 00:02] Guard #99 begins shift
[1518-11-04 00:36] falls asleep
[1518-11-04 00:46] wakes up
[1518-11-05 00:03] Guard #99 begins shift
[1518-11-05 00:45] falls asleep
[1518-11-05 00:55] wakes up"""


if __name__ == "__main__":
    typer.run(Day04().run)

# vim:expandtab:sw=4:ts=4
