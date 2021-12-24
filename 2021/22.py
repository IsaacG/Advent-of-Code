#!/bin/python
"""Advent of Code: Day 22."""

import collections
import itertools
import math
import re

import typer
from lib import aoc

SAMPLE = ["""\
on x=10..12,y=10..12,z=10..12
on x=11..13,y=11..13,z=11..13
off x=9..11,y=9..11,z=9..11
on x=10..10,y=10..10,z=10..10
""","""\
on x=-20..26,y=-36..17,z=-47..7
on x=-20..33,y=-21..23,z=-26..28
on x=-22..28,y=-29..23,z=-38..16
on x=-46..7,y=-6..46,z=-50..-1
on x=-49..1,y=-3..46,z=-24..28
on x=2..47,y=-22..22,z=-23..27
on x=-27..23,y=-28..26,z=-21..29
on x=-39..5,y=-6..47,z=-3..44
on x=-30..21,y=-8..43,z=-13..34
on x=-22..26,y=-27..20,z=-29..19
off x=-48..-32,y=26..41,z=-47..-37
on x=-12..35,y=6..50,z=-50..-2
off x=-48..-32,y=-32..-16,z=-15..-5
on x=-18..26,y=-33..15,z=-7..46
off x=-40..-22,y=-38..-28,z=23..41
on x=-16..35,y=-41..10,z=-47..6
off x=-32..-23,y=11..30,z=-14..3
on x=-49..-5,y=-3..45,z=-29..18
off x=18..30,y=-20..-8,z=-3..13
on x=-41..9,y=-7..43,z=-33..15
on x=-54112..-39298,y=-85059..-49293,z=-27449..7877
on x=967..23432,y=45373..81175,z=27513..53682
""","""\
on x=-5..47,y=-31..22,z=-19..33
on x=-44..5,y=-27..21,z=-14..35
on x=-49..-1,y=-11..42,z=-10..38
on x=-20..34,y=-40..6,z=-44..1
off x=26..39,y=40..50,z=-2..11
on x=-41..5,y=-41..6,z=-36..8
off x=-43..-33,y=-45..-28,z=7..25
on x=-33..15,y=-32..19,z=-34..11
off x=35..47,y=-46..-34,z=-11..5
on x=-14..36,y=-6..44,z=-16..29
on x=-57795..-6158,y=29564..72030,z=20435..90618
on x=36731..105352,y=-21140..28532,z=16094..90401
on x=30999..107136,y=-53464..15513,z=8553..71215
on x=13528..83982,y=-99403..-27377,z=-24141..23996
on x=-72682..-12347,y=18159..111354,z=7391..80950
on x=-1060..80757,y=-65301..-20884,z=-103788..-16709
on x=-83015..-9461,y=-72160..-8347,z=-81239..-26856
on x=-52752..22273,y=-49450..9096,z=54442..119054
on x=-29982..40483,y=-108474..-28371,z=-24328..38471
on x=-4958..62750,y=40422..118853,z=-7672..65583
on x=55694..108686,y=-43367..46958,z=-26781..48729
on x=-98497..-18186,y=-63569..3412,z=1232..88485
on x=-726..56291,y=-62629..13224,z=18033..85226
on x=-110886..-34664,y=-81338..-8658,z=8914..63723
on x=-55829..24974,y=-16897..54165,z=-121762..-28058
on x=-65152..-11147,y=22489..91432,z=-58782..1780
on x=-120100..-32970,y=-46592..27473,z=-11695..61039
on x=-18631..37533,y=-124565..-50804,z=-35667..28308
on x=-57817..18248,y=49321..117703,z=5745..55881
on x=14781..98692,y=-1341..70827,z=15753..70151
on x=-34419..55919,y=-19626..40991,z=39015..114138
on x=-60785..11593,y=-56135..2999,z=-95368..-26915
on x=-32178..58085,y=17647..101866,z=-91405..-8878
on x=-53655..12091,y=50097..105568,z=-75335..-4862
on x=-111166..-40997,y=-71714..2688,z=5609..50954
on x=-16602..70118,y=-98693..-44401,z=5197..76897
on x=16383..101554,y=4615..83635,z=-44907..18747
off x=-95822..-15171,y=-19987..48940,z=10804..104439
on x=-89813..-14614,y=16069..88491,z=-3297..45228
on x=41075..99376,y=-20427..49978,z=-52012..13762
on x=-21330..50085,y=-17944..62733,z=-112280..-30197
on x=-16478..35915,y=36008..118594,z=-7885..47086
off x=-98156..-27851,y=-49952..43171,z=-99005..-8456
off x=2032..69770,y=-71013..4824,z=7471..94418
on x=43670..120875,y=-42068..12382,z=-24787..38892
off x=37514..111226,y=-45862..25743,z=-16714..54663
off x=25699..97951,y=-30668..59918,z=-15349..69697
off x=-44271..17935,y=-9516..60759,z=49131..112598
on x=-61695..-5813,y=40978..94975,z=8655..80240
off x=-101086..-9439,y=-7088..67543,z=33935..83858
off x=18020..114017,y=-48931..32606,z=21474..89843
off x=-77139..10506,y=-89994..-18797,z=-80..59318
off x=8476..79288,y=-75520..11602,z=-96624..-24783
on x=-47488..-1262,y=24338..100707,z=16292..72967
off x=-84341..13987,y=2429..92914,z=-90671..-1318
off x=-37810..49457,y=-71013..-7894,z=-105357..-13188
off x=-27365..46395,y=31009..98017,z=15428..76570
off x=-70369..-16548,y=22648..78696,z=-1892..86821
on x=-53470..21291,y=-120233..-33476,z=-44150..38147
off x=-93533..-4276,y=-16170..68771,z=-104985..-24507
"""]
InputType = list[int]


class Day22(aoc.Challenge):

    DEBUG = True
    SUBMIT = {1: True, 2: False}

    TESTS = (
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=39),
        aoc.TestCase(inputs=SAMPLE[1], part=1, want=590784),
        aoc.TestCase(inputs=SAMPLE[2], part=2, want=2758514936282235),
    )

    # Convert lines to type:
    INPUT_TYPES = int
    # Split on whitespace and coerce types:
    # INPUT_TYPES = [str, int]
    # Apply a transform function
    # TRANSFORM = lambda _, l: (l[0], int(l[1:]))


    def part1(self, parsed_input: InputType) -> int:
        points = set()
        count = 0
        for toggle, x0, x1, y0, y1, z0, z1 in parsed_input:
            if count % 25 == 0:
                print(count)
            count += 1
            for x in range(max(-50,x0), min(x1,50)+1):
                if not -50 <= x <= 50: continue
                for y in range(max(-50,y0), min(50,y1)+1):
                    if not -50 <= y <= 50: continue
                    for z in range(max(-50,z0), min(z1,50)+1):
                        if not -50 <= z <= 50: continue
                        if toggle:
                            points.add((x,y,z))
                        elif (x,y,z) in points:
                            points.remove((x,y,z))
        return len(points)


    def no_intersect(self, a, b):
        return any(
            (a0 > b1 or b0 > a1)
            for (a0, a1), (b0, b1) in zip(a, b)
        )

    def intersect(self, a, b):
        return not self.no_intersect(a, b)

    def merge(self, a, b):
        if sum(1 for i, j in zip(a, b) if i == j) != 2:
            return None
        p = []
        for (a0, a1), (b0, b1) in zip(a, b):
            if a0 == b0 and a1 == b1:
                p.append((a0, a1))
            elif a0 == b1 + 1:
                p.append((b0, a1))
            elif b0 == a1 + 1:
                p.append((a0, b1))
            else:
                return None
        return tuple(p)

    def explode(self, a, b):
        if self.no_intersect(a, b):
            return set([a])
        dims = []
        for (a0, a1), (b0, b1) in zip(a, b):
            ranges = []
            if a0 < b0:  # left overhang
                ranges.append((a0, min(a1, b0)-1))
            ranges.append((max(a0, b0), min(b1, a1)))
            if a1 > b1:  # right overhang
                ranges.append((min(b1, a0)+1, a1))
            dims.append(ranges)
        cuboids = set(itertools.product(*dims))
        return cuboids

    def meld(self, pieces):
        for a in pieces:
            for b in pieces:
                if a >= b:
                    continue
                if combined := self.merge(a, b):
                    pieces.remove(a)
                    pieces.remove(b)
                    pieces.add(combined)
                    return self.meld(pieces)
        return pieces

    def combine(self, a, b):
        a_pieces = Day22().explode(a, b)
        b_pieces = Day22().explode(b, a)
        return self.meld(a_pieces | b_pieces)

    def subtract(self, a, b):
        a_pieces = Day22().explode(a, b)
        b_pieces = Day22().explode(b, a)
        # print(f"{a=} {b=}")
        # print(f"{a_pieces=}")
        # print(f"{b_pieces=}")
        return a_pieces - b_pieces, b_pieces - a_pieces

    def part2(self, parsed_input: InputType) -> int:
        on_cubes = set()
        for line in parsed_input:
            toggle, x0, x1, y0, y1, z0, z1 = line
            print(line, len(on_cubes))
            cur = ((x0, x1), (y0, y1), (z0, z1))
            if toggle:
                to_add = set([cur])
                for other in list(on_cubes):
                    for piece in list(to_add):
                        if self.no_intersect(piece, other):
                            continue
                        to_add.remove(piece)
                        to_add.update(self.subtract(piece, other)[0])
                on_cubes.update(to_add)
            else:
                to_del = set([cur])
                count = 1
                while to_del:
                    count += 1
                    assert count < 1000
                    # print(len(to_del), len(on_cubes))
                    piece = to_del.pop()
                    for other in list(on_cubes):
                        if self.no_intersect(piece, other):
                            continue

                        remain_on, remain_del = self.subtract(other, piece)
                        on_cubes.remove(other)
                        on_cubes.update(remain_on)
                        to_del.update(remain_del)
                        break
        return len(on_cubes)


    def part2_b(self, parsed_input: InputType) -> int:
        count = 0
        on_cubes = []
        for toggle, x0, x1, y0, y1, z0, z1 in parsed_input:
            if toggle:
                on_cubes.append(tuple([(x0, x1), (y0, y1), (z0, z1)]))
        print(f"{len(on_cubes)=}")

        off_cubes = []
        for toggle, x0, x1, y0, y1, z0, z1 in parsed_input:
            if not toggle:
                off_cubes.append(tuple([(x0, x1), (y0, y1), (z0, z1)]))
        print(f"{len(off_cubes)=}")

        on_intersections = []
        for ai, a in enumerate(on_cubes):
            for bi, b in enumerate(on_cubes):
                if a >= b: continue
                overlap = True
                (ax0, ax1), (ay0, ay1), (az0, az1) = a
                (bx0, bx1), (by0, by1), (bz0, bz1) = b
                for p1, p2 in zip(a, b):
                    ap0, ap1 = p1
                    bp0, bp1 = p2
                    if ap0 > bp1 or bp0 > ap1:
                        overlap = False
                if not overlap: continue

                overlap_dim = []
                for p1, p2 in zip(a, b):
                    ap0, ap1 = p1
                    bp0, bp1 = p2
                    overlap_dim.append(tuple([max(ap0, bp0), min(ap1, bp1)]))
                on_intersections.append(tuple(overlap_dim))

        cuts = []
        for ai, a in enumerate(on_cubes):
            for bi, b in enumerate(off_cubes):
                if ai == bi: continue
                overlap = True
                (ax0, ax1), (ay0, ay1), (az0, az1) = a
                (bx0, bx1), (by0, by1), (bz0, bz1) = b
                for p1, p2 in zip(a, b):
                    ap0, ap1 = p1
                    bp0, bp1 = p2
                    if ap0 > bp1 or bp0 > ap1:
                        overlap = False
                if not overlap: continue

                overlap_dim = []
                for p1, p2 in zip(a, b):
                    ap0, ap1 = p1
                    bp0, bp1 = p2
                    overlap_dim.append(tuple([max(ap0, bp0), min(ap1, bp1)]))
                cuts.append(tuple(overlap_dim))

        cut_overlaps = []
        for ai, a in enumerate(cuts):
            for bi, b in enumerate(cuts):
                if ai == bi: continue
                overlap = True
                (ax0, ax1), (ay0, ay1), (az0, az1) = a
                (bx0, bx1), (by0, by1), (bz0, bz1) = b
                for p1, p2 in zip(a, b):
                    ap0, ap1 = p1
                    bp0, bp1 = p2
                    if ap0 > bp1 or bp0 > ap1:
                        overlap = False
                if not overlap: continue

                overlap_dim = []
                for p1, p2 in zip(a, b):
                    ap0, ap1 = p1
                    bp0, bp1 = p2
                    overlap_dim.append(tuple([max(ap0, bp0), min(ap1, bp1)]))
                cut_overlaps.append(tuple(overlap_dim))

        sum_on = sum((x1 - x0) * (y1 - y0) * (z1 - z0) for (x0, x1), (y0, y1), (z0, z1) in on_cubes)
        sum_on_intersections = sum((x1 - x0) * (y1 - y0) * (z1 - z0) for (x0, x1), (y0, y1), (z0, z1) in on_intersections)
        sum_cuts = sum((x1 - x0) * (y1 - y0) * (z1 - z0) for (x0, x1), (y0, y1), (z0, z1) in cuts)
        sum_cut_overlaps = sum((x1 - x0) * (y1 - y0) * (z1 - z0) for (x0, x1), (y0, y1), (z0, z1) in cut_overlaps)

        total = sum_on - sum_on_intersections - sum_cuts + sum_cut_overlaps
        return total


        print(f"{len(on_cubes)=} {len(off_cubes)=}")
        print(f"{len(intersections)=} {len(off_intersections)=}")


        return 0

    def parse_input(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        instructions = []
        for line in puzzle_input.splitlines():
            toggle = line.split()[0] == "on"
            nums = re.findall(r"-?[0-9]+", line)
            assert len(nums) == 6, nums
            instructions.append([toggle] + [int(i) for i in nums])
        return instructions


if __name__ == "__main__":
    # big, small = ((0,2), (0,2), (0,2)), ((1,1), (1,1), (1,3))
    # big, small = ((0,0), (0,0), (0,0)), ((2,2), (2,2), (2,2))
    # res = Day22().combine(big, small)
    # print(len(res))
    # for i in res:
    #     print(i)
    big = ((1, 1), (1, 1), (1, 2))
    small = ((1, 2), (1, 1), (1, 1))

    res = Day22().subtract(big, small)[1]
    print(len(res))
    for i in res:
        print(i)
    print()


    typer.run(Day22().run)

# vim:expandtab:sw=4:ts=4
