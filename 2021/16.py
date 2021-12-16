#!/bin/python
"""Advent of Code: Day 16."""

import collections
import dataclasses
import functools
import math
import re

import typer
from lib import aoc

SAMPLE = ["EE00D40C823060", "8A004A801A8002F478", "620080001611562C8802118E34", "C0015000016115A2E0802F182340", "A0016C880162017C3686B18A3D4780"]
InputType = str

@dataclasses.dataclass
class Packet:
    version: int
    packet_type: int
    num: int = -1
    length_type: int = -1
    length: int = -1
    packet_count: int = -1
    sub_packets: list["Packet"] = None

    def version_sum(self):
        if self.sub_packets:
            ts = sum(p.version_sum() for p in self.sub_packets)
        else:
            ts = 0
        return self.version + ts

    def eval(self):
        if self.packet_type == 0: # sum
            res = 0
            for p in self.sub_packets:
                res += p.eval()
            return res
        if self.packet_type == 1: # product
            res = 1
            for p in self.sub_packets:
                res *= p.eval()
            return res
        if self.packet_type == 2: # min
            return min(p.eval() for p in self.sub_packets)
        if self.packet_type == 3: # max
            return max(p.eval() for p in self.sub_packets)
        if self.packet_type == 4: # literal
            return self.num
        if self.packet_type == 5: # gt
            a, b = [p.eval() for p in self.sub_packets]
            return 1 if a > b else 0
        if self.packet_type == 6: # lt
            a, b = [p.eval() for p in self.sub_packets]
            return 1 if a < b else 0
        if self.packet_type == 7: # eq
            a, b = [p.eval() for p in self.sub_packets]
            return 1 if a == b else 0


def packet_parser(take_n):
    version = int(take_n(3), 2)
    ptype = int(take_n(3), 2)
    num = None
    length_type = None
    length = None
    packet_count = None
    if ptype == 4:  # number
        packet = []
        more = True
        while more:
            group = take_n(5)
            more, num = group[:1] == "1", group[1:]
            packet.append(num)
        num = int("".join(packet), 2)
        # print(f"Packet Literal {version=} {num=}")
        return Packet(version, ptype, num=num)

    length_type = int(take_n(1))
    if length_type == 0: # 15 bits => body len
        length = int(take_n(15), 2)
        sub_packets = []
        subpackets_str = (take_n(length))
        subpackets_iter = iter(subpackets_str)
        # print(f"{version=} Type 0 - Subpacket length = {length}: {subpackets_str=}")
        while True:
            subpackets_str = "".join(subpackets_iter)
            if not subpackets_str:
                break
            subpackets_iter = iter(subpackets_str)
            take_f = lambda n: "".join(next(subpackets_iter) for _ in range(n))
            sub_packets.append(packet_parser(take_f))
        return Packet(version, ptype, length_type=length_type, length=length, sub_packets=sub_packets)
    elif length_type == 1: # 11 bits => sub-packet count
        packet_count = int(take_n(11), 2)
        # print(f"{version=} Type 1 - Subpacket count = {packet_count}")
        sub_packets = [packet_parser(take_n) for _ in range(packet_count)]
        return Packet(version, ptype, length_type=length_type, packet_count=packet_count, sub_packets=sub_packets)


class Day16(aoc.Challenge):

    DEBUG = True

    TESTS = (
        # aoc.TestCase(inputs=SAMPLE[0], part=1, want=4),
        aoc.TestCase(inputs="8A004A801A8002F478", part=1, want=16),
        aoc.TestCase(inputs="620080001611562C8802118E34", part=1, want=12),
        aoc.TestCase(inputs="C0015000016115A2E0802F182340", part=1, want=23),
        aoc.TestCase("A0016C880162017C3686B18A3D4780", part=1, want=31),
        aoc.TestCase(inputs="C200B40A82", part=2, want=3),
        aoc.TestCase(inputs="04005AC33890", part=2, want=54),
        aoc.TestCase(inputs="880086C3E88112", part=2, want=7),
        aoc.TestCase(inputs="CE00C43D881120", part=2, want=9),
        aoc.TestCase(inputs="D8005AC2A8F0", part=2, want=1),
        aoc.TestCase(inputs="F600BC2D8F", part=2, want=0),
        aoc.TestCase(inputs="9C005AC2F8F0", part=2, want=0),
        aoc.TestCase(inputs="9C0141080250320F1802104A08", part=2, want=1),
    )

    # Convert lines to type:
    INPUT_TYPES = str
    # Split on whitespace and coerce types:
    # INPUT_TYPES = [str, int]
    # Apply a transform function
    # TRANSFORM = lambda _, l: (l[0], int(l[1:]))

    def part1(self, parsed_input: InputType) -> int:
        bits = ''
        for char in parsed_input:
            byte = bin(int(char, 16))[2:].zfill(4)
            bits += byte
        bits_iter = iter(bits)

        def take_n(n):
            return "".join(next(bits_iter) for _ in range(n))

        packet = packet_parser(take_n)
        # print(packet)
        ts = packet.version_sum()
        print(ts)
        return ts

    def part2(self, parsed_input: InputType) -> int:
        bits = ''
        for char in parsed_input:
            byte = bin(int(char, 16))[2:].zfill(4)
            bits += byte
        bits_iter = iter(bits)

        def take_n(n):
            return "".join(next(bits_iter) for _ in range(n))

        packet = packet_parser(take_n)
        return packet.eval()


    def parse_input(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        return super().parse_input(puzzle_input)[0]

        return puzzle_input.splitlines()
        return puzzle_input
        return [int(i) for i in puzzle_input.splitlines()]

        mutate = lambda x: (x[0], int(x[1])) 
        return [mutate(line.split()) for line in puzzle_input.splitlines()]


if __name__ == "__main__":
    typer.run(Day16().run)

# vim:expandtab:sw=4:ts=4
