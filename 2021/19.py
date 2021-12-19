#!/bin/python
"""Advent of Code: Day 19."""

import functools
import time

import typer
from lib import aoc

SAMPLE = """\
--- scanner 0 ---
404,-588,-901
528,-643,409
-838,591,734
390,-675,-793
-537,-823,-458
-485,-357,347
-345,-311,381
-661,-816,-575
-876,649,763
-618,-824,-621
553,345,-567
474,580,667
-447,-329,318
-584,868,-557
544,-627,-890
564,392,-477
455,729,728
-892,524,684
-689,845,-530
423,-701,434
7,-33,-71
630,319,-379
443,580,662
-789,900,-551
459,-707,401

--- scanner 1 ---
686,422,578
605,423,415
515,917,-361
-336,658,858
95,138,22
-476,619,847
-340,-569,-846
567,-361,727
-460,603,-452
669,-402,600
729,430,532
-500,-761,534
-322,571,750
-466,-666,-811
-429,-592,574
-355,545,-477
703,-491,-529
-328,-685,520
413,935,-424
-391,539,-444
586,-435,557
-364,-763,-893
807,-499,-711
755,-354,-619
553,889,-390

--- scanner 2 ---
649,640,665
682,-795,504
-784,533,-524
-644,584,-595
-588,-843,648
-30,6,44
-674,560,763
500,723,-460
609,671,-379
-555,-800,653
-675,-892,-343
697,-426,-610
578,704,681
493,664,-388
-671,-858,530
-667,343,800
571,-461,-707
-138,-166,112
-889,563,-600
646,-828,498
640,759,510
-630,509,768
-681,-892,-333
673,-379,-804
-742,-814,-386
577,-820,562

--- scanner 3 ---
-589,542,597
605,-692,669
-500,565,-823
-660,373,557
-458,-679,-417
-488,449,543
-626,468,-788
338,-750,-386
528,-832,-391
562,-778,733
-938,-730,414
543,643,-506
-524,371,-870
407,773,750
-104,29,83
378,-903,-323
-778,-728,485
426,699,580
-438,-605,-362
-469,-447,-387
509,732,623
647,635,-688
-868,-804,481
614,-800,639
595,780,-596

--- scanner 4 ---
727,592,562
-293,-554,779
441,611,-461
-714,465,-776
-743,427,-804
-660,-479,-426
832,-632,460
927,-485,-438
408,393,-506
466,436,-512
110,16,151
-258,-428,682
-393,719,612
-211,-452,876
808,-476,-593
-575,615,604
-485,667,467
-680,325,-822
-627,-443,-432
872,-547,-609
833,512,582
807,604,487
839,-516,451
891,-625,532
-652,-548,-490
30,-46,-14
"""
InputType = list[int]


class Day19(aoc.Challenge):
    """Merge disperate sensor maps of beacons into one unified map."""

    TESTS = (
        aoc.TestCase(inputs=SAMPLE, part=1, want=79),
        aoc.TestCase(inputs=SAMPLE, part=2, want=3621),
    )

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
        
        # Freeze these sets so they are hashable and can be placed into other sets.
        return frozenset([frozenset(o) for o in options])

    @functools.cache
    def merge(self, parsed_input):
        to_merge = set(parsed_input)
        merged_map = to_merge.pop()
        scanners = [(0,0,0)]
        assert len(merged_map) > 12, merged_map
        start = time.clock_gettime(time.CLOCK_MONOTONIC)
        to_merge = set(self.orientations(p) for p in to_merge)
        while to_merge:
            matched = None
            for options in list(to_merge):
                for option in options:
                    assert isinstance(option, frozenset), options
                    sample_set = list(option)[:-10]
                    for mp in merged_map:
                        for point in list(option)[:-11]:
                            translation = tuple(a - b for a, b in zip(point, mp))
                            translated = set(tuple(p - t for p, t in zip(x, translation)) for x in sample_set)
                            if len(merged_map.intersection(translated)) < 2:
                                continue

                            translated = set(tuple(p - t for p, t in zip(x, translation)) for x in option)
                            overlap = len(merged_map.intersection(translated))
                            if overlap >= 12:
                                matched = options
                                merged_map = merged_map.union(translated)
                                scanners.append(translation)
                                to_merge.remove(matched)
                                end = time.clock_gettime(time.CLOCK_MONOTONIC)
                                delta = int(end - start)
                                self.debug(f"{len(to_merge)=} {len(merged_map)=} time: {delta}")
                                break
                        if matched: break
                    if matched: break
            assert matched
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

    def test_orientations(self, parsed_input: InputType) -> int:
        initial = parsed_input[0]
        options = self.orientations(initial)
        for scanner in parsed_input:
            assert scanner in options
        return 5

    def parse_input(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        scans = []
        for block in puzzle_input.split("\n\n"):
            points = set()
            for line in block.splitlines()[1:]:
                x, y, z = line.split(",")
                points.add(tuple([int(x), int(y), int(z)]))
            scans.append(frozenset(points))
        return frozenset(scans)


if __name__ == "__main__":
    typer.run(Day19().run)

# vim:expandtab:sw=4:ts=4
