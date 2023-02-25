#!/bin/python
"""Advent of Code, Day 4: Repose Record. Calculate which guard is most likely to be asleep."""

from __future__ import annotations

import collections
import heapq
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

InputType = dict[int, list[tuple[int, int]]]


class Day04(aoc.Challenge):
    """Day 4: Repose Record."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE, part=1, want=240),
        aoc.TestCase(inputs=SAMPLE, part=2, want=4455),
    ]

    def max_asleep_time(self, intervals: list[tuple[int, int]]) -> tuple[int, int]:
        """Return the count and time at which there is maximal interval overlap.

        This uses a line sweep algorithm to solve this problem in O(n) time,
        i.e. a single pass.
        """
        count = 0
        max_count = 0
        max_time = 0
        awake: list[int] = []

        for start, end in intervals:
            # End any interval where the guard wakes.
            while awake and awake[0] <= start:
                count -= 1
                heapq.heappop(awake)
            # Add this new interval where the guard falls asleep.
            count += 1
            # Add the wakeup time to the heap.
            heapq.heappush(awake, end)
            if count > max_count:
                max_count, max_time = count, start
        return max_count, max_time

    def part1(self, parsed_input: InputType) -> int:
        """Return which guard sleeps the most overall and at what time."""
        # Compute how many minutes overall each guard sleeps.
        asleep = {
            guard_id: sum(end - start for start, end in v)
            for guard_id, v in parsed_input.items()
        }
        # Find the guard who sleeps the most minutes.
        guard_id, _ = max(asleep.items(), key=lambda i: i[1])
        # Find what time the guard is most likely to be asleep.
        _, max_time = self.max_asleep_time(parsed_input[guard_id])
        return guard_id * max_time

    def part2(self, parsed_input: InputType) -> int:
        """Return the guard who is most likely to be asleep at any given minute."""
        guard_id, (_, max_time) = max(
            (
                (guard_id, self.max_asleep_time(intervals))
                for guard_id, intervals in parsed_input.items()
            ), key=lambda i: i[1][0]
        )
        return guard_id * max_time

    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        lines = sorted(puzzle_input.splitlines())

        log_pattern = re.compile(r"^\[[0-9-]+ (\d\d):(\d\d)\] (.*)$")
        begin_pattern = re.compile(r"^Guard #(\d+) begins shift$")
        sleeping: dict[int, list[tuple[int, int]]] = collections.defaultdict(list)

        guard_id = 0
        start = 0
        awake = False

        for line in lines:
            m = log_pattern.match(line)
            assert m is not None, line
            hh_str, mm_str, rest = m.groups()
            hh, mm = int(hh_str), int(mm_str)
            if hh != 0:
                # assert rest.endswith("begins shift") and hh == 23
                hh, mm = 0, 0

            if rest.endswith("begins shift"):
                m = begin_pattern.match(rest)
                assert m is not None
                if guard_id and not awake:
                    sleeping[guard_id].append((start, 59))
                new_id = int(m.group(1))
                guard_id, start, awake = new_id, mm, True
            elif line.endswith("wakes up"):
                # assert not awake
                awake = True
                sleeping[guard_id].append((start, mm))
            elif line.endswith("falls asleep"):
                # assert awake
                awake = False
                start = mm

        for interval in sleeping.values():
            interval.sort()
        return sleeping


if __name__ == "__main__":
    typer.run(Day04().run)

# vim:expandtab:sw=4:ts=4
