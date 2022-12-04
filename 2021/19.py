#!/bin/python
"""Advent of Code: Day 19."""

import collections
import functools
import itertools

import typer
from lib import aoc
import input_data

SAMPLE = input_data.D19_SAMPLE


class Day19(aoc.Challenge):
    """Merge disperate sensor maps of beacons into one unified map."""

    DEBUG = True

    TESTS = (
        aoc.TestCase(inputs=SAMPLE, part=1, want=79),
        aoc.TestCase(inputs=SAMPLE, part=2, want=3621),
    )

    @staticmethod
    @functools.cache
    def orientations(scanner):
        """Return all 24 orientations of a beacon map.

        X: right, left.
        Y: up, down.
        Z: forward, backwards.

        Dice have 6 sides. If you're inside a die ... or room, there are 6 walls
        you can be looking at.
        That can be "folded" into three orientations plus 180 degrees of those.
        Those three orientations are (1) forward, (2) left, (3) up.
        Compute those three orientations.
        Add the 180 degree rotation of those orientations for the 6 walls. This
        is a Y-rotation.

        While looking at any of those six walls, there are four "rotations" that
        you can take on. Think of a person looking at a wall while "standing" on
        the floor, ceiling or either adjacent wall.

        This is a Z-rotation of n*90 degrees for n in [0..4).
        """
        # Primary 3 orientations: forward, left, up.
        options = [scanner]
        rot_left = {(z, y, -x) for x, y, z in scanner}
        options.append(rot_left)
        rot_up = {(x, -z, y) for x, y, z in scanner}
        options.append(rot_up)

        # Reverse each of those, giving backwards, right, down.
        for opt in list(options):
            rot_y_180 = {(-x, y, -z) for x, y, z in opt}
            options.append(rot_y_180)

        # For each orientation/wall, rotate 90 degrees.
        for opt in list(options):
            rot_z_90 = opt.copy()
            for _ in range(3):
                rot_z_90 = {(-y, x, z) for x, y, z in rot_z_90}
                options.append(rot_z_90)

        return options

    @staticmethod
    @functools.cache
    def relative_offsets(beacon_map):
        """Compute the pairwise Manhatten distance of all points in a map.

        The Manhatten distance is orientation independent which allows
        comparing maps for similarities without needing to try multiple orientations.
        """
        # distance(a, b) == distance(b, a) so only take one. Pick a > b.
        pairs = ((a, b) for a in beacon_map for b in beacon_map if a > b)
        distances = [sum(abs(i - j) for i, j in zip(a, b)) for a, b in pairs]
        return distances

    @functools.cache
    def potential_match(self, map_a, map_b) -> bool:
        """Orientation-agnostic check to see if two maps may line up.

        For a rough test, we can check if maps overlap by examining the
        Manhatten distances of all pairwise points in the map.
        This allows to discard a map with only one orientation.
        For 12 matching beacons, there should be sum(0..11) matching distances.
        sum(0..11) = n*(n+1)/2 = 66
        """
        pairs = itertools.product(
            self.relative_offsets(map_a),
            self.relative_offsets(map_b)
        )
        return sum(1 for a, b in pairs if a == b) >= 66

    # This is slow. Cache results so part2 can reuse part1.
    @functools.cache
    def merge(self, beacon_maps):
        """Merge all the sensor maps into a unified map of the beacons.

        Return the unified map as well as the sensor locations.

        Very similar to a jigsaw puzzle, start with a single piece and "fix" it in place.
        Look through all the "loose" pieces.
        With every piece, try to connect it to the "fixed" pieces, attempting every
        possible orientation until something fits. Once a piece fits, "fix" it in place.
        Repeat until all the loose pieces have been fixed.
        """
        #  All the beacon_maps need merging.
        to_merge = set(beacon_maps)
        merged_maps = {to_merge.pop().copy(): (0, 0, 0)}

        # Merge beacon maps until all are used.
        while to_merge:
            to_merge_count = len(to_merge)
            # For every loose piece, try to fit it in.
            for fixed, candidate in itertools.product(reversed(merged_maps.keys()), list(to_merge)):
                if not self.potential_match(candidate, fixed):
                    continue

                # Try to fit the loose piece in every possible orientation.
                for orientation in self.orientations(candidate):
                    # To see if a beacon map matches the fixed beacons,
                    # compute all possible ways to translate a beacon to
                    # fit the fixed beacons.
                    # For every pairwise beacon between the fixed beacons and
                    # candidate beacons, take the difference to get how the map
                    # needs to be translated to match.
                    # If 12 (or more) beacons can match with the same translation,
                    # then that translation generates 12 overlaps and is a "match".
                    translation, count = collections.Counter(
                        tuple(a - b for a, b in zip(point, mp))
                        for mp in fixed
                        for point in orientation
                    ).most_common(1)[0]
                    if count < 12:
                        continue

                    combined_translation = tuple(
                        a + b for a, b in zip(translation, merged_maps[fixed])
                    )

                    # Fix this loose piece to the overall map.
                    merged_maps[frozenset(orientation)] = combined_translation
                    # Remove this piece from the loose pieces.
                    to_merge.remove(candidate)
                    break
                if to_merge_count != len(to_merge):
                    break
            # assert to_merge_count != len(to_merge)
        return merged_maps

    def part1(self, parsed_input: frozenset[frozenset[tuple[int, int, int]]]) -> int:
        """Return the number of beacons in the ocean."""
        merged_map = self.merge(parsed_input)
        merged_beacons = set()
        for beacons, translation in merged_map.items():
            merged_beacons |= {
                tuple(a - b for a, b in zip(point, translation))
                for point in beacons
            }
        return len(merged_beacons)

    def part2(self, parsed_input: frozenset[frozenset[tuple[int, int, int]]]) -> int:
        """Compute the maximum distance between any two sensors."""
        scanners = self.merge(parsed_input).values()
        distances = [sum(abs(i - j) for i, j in zip(a, b)) for a in scanners for b in scanners]
        return max(distances)

    def input_parser(self, puzzle_input: str) -> frozenset[frozenset[tuple[int, ...]]]:
        """Parse the input data."""
        scans = []
        for block in puzzle_input.split("\n\n"):
            points = frozenset(
                tuple([int(i) for i in line.split(",")])
                for line in block.splitlines()[1:]
            )
            scans.append(points)
        return frozenset(scans)


if __name__ == "__main__":
    typer.run(Day19().run)

# vim:expandtab:sw=4:ts=4
