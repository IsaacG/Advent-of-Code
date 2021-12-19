#!/bin/python
"""Advent of Code: Day 19."""

import functools
import time

import typer
from lib import aoc
import input_data

SAMPLE = input_data.D19_SAMPLE
InputType = list[int]


class Day19(aoc.Challenge):
    """Merge disperate sensor maps of beacons into one unified map."""

    TESTS = (
        aoc.TestCase(inputs=SAMPLE, part=1, want=79),
        aoc.TestCase(inputs=SAMPLE, part=2, want=3621),
    )

    @functools.cache
    def orientations(self, scanner):
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

        # assert len(options) == 24
        # for i in range(24):
        #     for j in range(24):
        #         if i == j:
        #             continue
        #         assert options[i] != options[j], f"{i}, {j}"
        
        return options

    def test_orientations(self) -> int:
        """Test the orientations work."""
        beacon_maps = self.parse_input(input_data.D19_ORIENTATIONS)
        initial = beacon_maps[0]
        options = self.orientations(initial)
        for scanner in beacon_maps:
            assert scanner in options

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
        # All the beacon_maps need merging.
        to_merge = set(beacon_maps)
        # Pick out one piece to start the "fixed" map.
        merged_map = to_merge.pop()
        # That fixed piece has the scanner at the origin.
        scanners = [(0,0,0)]
        # Expand all the other pieces to the set of all their possible orientations.
        # to_merge = set(self.orientations(p) for p in to_merge)

        start = time.clock_gettime(time.CLOCK_MONOTONIC)
        # Merge beacon maps until all are used.
        while to_merge:
            matched = None
            # For every loose piece, try to fit it in.
            for beacon_map in list(to_merge):
                # Try to fit the loose piece in every possible orientation.
                for orientation in self.orientations(beacon_map):
                    orientation = list(orientation)
                    # Rather than working with the entire set of beacons in the map,
                    # ignore 10 at first. Try to the other beacons match.
                    # If at least two beacons match, then maybe there are 12 that match!
                    # At that point, add back those 10 points and see if there is a full 12.
                    sample_set, rest_of_points = orientation[:-10], orientation[10:]
                    # When checking to see if a piece "fits" into the map, move the beacon map
                    # such that a point on the beacon map aligns with a point on the fixed map.
                    # If 12 points align at any point, this is a "match".
                    # We need to try aligning every point on the beacon map with every point on
                    # the fixed map. Since at least 12 points should line up, there are 12 points
                    # on the beacon map that line up in the same way on the fixed map.
                    # That is 12 translations that are identical. As such, we can trying to translate
                    # 11 points on the beacon map as redundant.
                    for mp in merged_map:
                        for point in orientation[:-11]:
                            # How much this beacon map needs shifting to align.
                            translation = tuple(a - b for a, b in zip(point, mp))
                            # Translate the sample points.
                            translated = set(tuple(p - t for p, t in zip(x, translation)) for x in sample_set)
                            # If only one point lines up, move on.
                            if len(merged_map.intersection(translated)) == 2:
                                continue

                            # Otherwise, go for a full match.
                            translated.update(tuple(p - t for p, t in zip(x, translation)) for x in rest_of_points)
                            overlap = len(merged_map.intersection(translated))
                            if overlap >= 12:
                                matched = True
                                # Fix this loose piece to the overall map.
                                merged_map = merged_map.union(translated)
                                scanners.append(translation)
                                # Remove this piece from the loose pieces.
                                to_merge.remove(beacon_map)
                                end = time.clock_gettime(time.CLOCK_MONOTONIC)
                                delta = int(end - start)
                                self.debug(f"{len(to_merge)=} {len(merged_map)=} time: {delta}")
                                break
                        if matched: break
                    if matched: break
        return merged_map, scanners

    def part1(self, parsed_input: InputType) -> int:
        """Return the number of beacons in the ocean."""
        merged_map, scanners = self.merge(parsed_input)
        return len(merged_map)

    def part2(self, parsed_input: InputType) -> int:
        """Compute the maximum distance between any two sensors."""
        merged_map, scanners = self.merge(parsed_input)
        distances = [sum(abs(i - j) for i, j in zip(a, b)) for a in scanners for b in scanners]
        return max(distances)

    def parse_input(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        scans = []
        for block in puzzle_input.split("\n\n"):
            points = set()
            for line in block.splitlines()[1:]:
                x, y, z = line.strip().split(",")
                points.add(tuple([int(x), int(y), int(z)]))
            scans.append(frozenset(points))
        return frozenset(scans)


if __name__ == "__main__":
    typer.run(Day19().run)

# vim:expandtab:sw=4:ts=4
