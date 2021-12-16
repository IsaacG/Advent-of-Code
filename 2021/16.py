#!/bin/python
"""Advent of Code: Day 16."""

import dataclasses
import io
import operator
from typing import Optional

import typer
from lib import aoc

InputType = str



def hex_to_bits(string):
    return "".join(bin(int(char, 16))[2:].zfill(4) for char in string)


@dataclasses.dataclass
class BasePacket:
    """A transmission packet."""
    version: int
    packet_type: int

    def __post_init__(self):
        pass

@dataclasses.dataclass
class Literal(BasePacket):
    value: int

    def __post_init__(self):
        super().__post_init__()
        if self.packet_type != 4:
            raise ValueError("invalid packet")

    def eval(self):
        return self.value

    def sum_versions(self):
        return self.version


@dataclasses.dataclass
class Operator(BasePacket):
    sub_packets: list["Packet"]

    def __post_init__(self):
        super().__post_init__()
        if self.packet_type not in (0, 1, 2, 3, 5, 7, 6):
            raise ValueError("invalid packet")
        if self.packet_type in (5, 7, 6) and len(self.sub_packets) != 2:
            raise ValueError("invalid number of subpackets")
        if self.packet_type > 4:
            self.binary_operator = True
        else:
            self.binary_operator = False

    def sum_versions(self):
        ts = sum(p.sum_versions() for p in self.sub_packets)
        return self.version + ts

    def eval(self):
        op = {
            0: sum,
            1: aoc.Helpers().mult,
            2: min,
            3: max,
            5: operator.gt,
            6: operator.lt,
            7: operator.eq,
        }[self.packet_type]
        if self.binary_operator:
            a, b = [p.eval() for p in self.sub_packets]
            return 1 if op(a, b) else 0
        else:
            values = (p.eval() for p in self.sub_packets)
            return op(values)


class BitStream(io.StringIO):

    def __init__(self, string: str):
        if any(s not in ("0", "1") for s in string):
            raise ValueError("invalid binary stream")
        super().__init__(string)
        self.length = len(string)

    @property
    def done(self) -> bool:
        return self.tell() == self.length

    def read_int(self, count: int) -> int:
        return int(self.read(count), 2)


def packet_parser(bits_io):
    version = bits_io.read_int(3)
    packet_type = bits_io.read_int(3)

    if packet_type == 4:  # number
        packet = []
        more = True
        while more:
            group = bits_io.read(5)
            more, num = group[:1] == "1", group[1:]
            packet.append(num)
        num = int("".join(packet), 2)
        # print(f"Packet Literal {version=} {num=}")
        return Literal(version, packet_type, num)

    length_type = bits_io.read_int(1)
    sub_packets = []

    if length_type == 0: # 15 bits => body len
        length = bits_io.read_int(15)
        sub_io = BitStream(bits_io.read(length))

        # Solving this properly would involve:
        # sub_end = sub_io.seek(0, io.SEEK_END)
        # sub_io.seek(0, io.SEEK_SET)
        # while sub_io.tell() != sub_end:
        # But in the interest of simple code, just loop until tell == length

        while sub_io.tell() != length:
            sub_packets.append(packet_parser(sub_io))

    elif length_type == 1: # 11 bits => sub-packet count
        packet_count = bits_io.read_int(11)
        for _ in range(packet_count):
            sub_packets.append(packet_parser(bits_io))

    return Operator(version, packet_type, sub_packets)


class Day16(aoc.Challenge):

    DEBUG = True

    TESTS = (
        aoc.TestCase(inputs="8A004A801A8002F478", part=1, want=16),
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

    def part1(self, parsed_input: str) -> int:
        bits_io = BitStream(hex_to_bits(parsed_input))
        return packet_parser(bits_io).sum_versions()

    def part2(self, parsed_input: str) -> int:
        bits_io = BitStream(hex_to_bits(parsed_input))
        return packet_parser(bits_io).eval()

    def parse_input(self, puzzle_input: str) -> str:
        """Parse the input data."""
        return puzzle_input


if __name__ == "__main__":
    typer.run(Day16().run)

# vim:expandtab:sw=4:ts=4
