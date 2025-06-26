#!/bin/python
"""Advent of Code, Day 5: If You Give A Seed A Fertilizer."""

import collections

from lib import aoc

SAMPLE = """\
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"""

InputType = tuple[list[int], list[list[list[int]]]]

class Day05(aoc.Challenge):
    """Day 5: If You Give A Seed A Fertilizer. Work a set of seeds through a number of range-translations."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE, part=1, want=35),
        aoc.TestCase(inputs=SAMPLE, part=2, want=46),
    ]

    def solver(self, puzzle_input: InputType, part_one: bool) -> int:
        """Map ranges of seeds to a final value and return the min."""
        seeds, translation_layers = puzzle_input

        # Convert p1 into p2 by changing each seed into a range of length 1.
        # [5, 6, 7] => [5, 1, 6, 1, 7, 1]
        if part_one:
            seeds = [i for seed in seeds for i in [seed, 1]]

        # Convert [seed, length, seed, length] into [(start, end), (start, end)] inclusive intervals.
        values = []
        for i in range(0, len(seeds), 2):
            values.append((seeds[i], seeds[i] + seeds[i + 1] - 1))

        # For each mapping, go through all value ranges and translate them to the next layer.
        for block in translation_layers:
            # Load the rules into a deque for easy access.
            block.sort()
            block_q = collections.deque(block)
            src_start, src_end, distance = block_q.popleft()

            # Copy the values into a queue and reset the list.
            ranges = collections.deque(sorted(values))
            values = []

            # Process ranges in order, splitting if needed, to create new ranges.
            while ranges:
                start, end = ranges.popleft()
                # Cycle through rules until a rule is relevant.
                while block_q and start > src_end:
                    src_start, src_end, distance = block_q.popleft()
                pre, overlap, post = aoc.interval_overlap((start, end), (src_start, src_end))
                if overlap is None:
                    values.append((start, end))
                else:
                    # Pre-overlap is copied without change. Overlap is translated.
                    # Post-overlap is put back into the queue as a later rule may apply.
                    if pre is not None:
                        values.append(pre)
                    values.append((overlap[0] + distance, overlap[1] + distance))
                    if post is not None:
                        ranges.appendleft(post)

        return min(values)[0]

    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        parser = aoc.ParseBlocks([aoc.parse_re_findall_int(r"\d+")])
        (seeds,), *translation_layers = parser.parse(puzzle_input)
        # Convert translation layers from `dest, src, length` to `start, end, distance`
        # while dropping the header.
        translation_layers = [
            [
                (src_start, src_start + length - 1, dst_start - src_start)
                for dst_start, src_start, length in block[1:]
            ]
            for block in translation_layers
        ]
        return seeds, translation_layers


# vim:expandtab:sw=4:ts=4
