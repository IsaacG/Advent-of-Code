#!/bin/python
"""Advent of Code: Day 16."""

from __future__ import annotations

import dataclasses
import enum
import io
import math
import operator

import typer
from lib import aoc


class PacketType(enum.IntEnum):
    """Various Packet types."""
    SUM = 0
    PROD = 1
    MIN = 2
    MAX = 3
    LITERAL = 4
    GREATER_THAN = 5
    LESS_THAN = 6
    EQUAL = 7


BINARY_OPERATORS = (PacketType.GREATER_THAN, PacketType.LESS_THAN, PacketType.EQUAL)


@dataclasses.dataclass
class BasePacket:
    """A base transmission packet."""

    version: int
    packet_type: PacketType

    def __post_init__(self) -> None:
        """Validate inputs."""

    def eval(self) -> int:
        """Evaluate the packet to an int."""
        raise NotImplementedError

    def sum_versions(self) -> int:
        """Return the version sum value."""
        return self.version

    def __str__(self) -> str:
        return self.packet_type.name


@dataclasses.dataclass
class Literal(BasePacket):
    """A Literal transmission packet. This contains a single value."""

    value: int

    def __post_init__(self) -> None:
        """Validate inputs."""
        super().__post_init__()
        if self.packet_type != PacketType.LITERAL:
            raise ValueError("invalid packet")

    def eval(self) -> int:
        """Evaluate the packet to an int."""
        return self.value

    def __str__(self) -> str:
        return f"{self.packet_type.name}({self.value})"


@dataclasses.dataclass
class Operator(BasePacket):
    """An Operator transmission packet. This contains an operator and operands."""

    operands: list[BasePacket]

    def __post_init__(self) -> None:
        """Validate inputs and initialize."""
        super().__post_init__()
        if self.packet_type == PacketType.LITERAL:
            raise ValueError("invalid packet")
        if self.packet_type in BINARY_OPERATORS and len(self.operands) != 2:
            raise ValueError("invalid number of subpackets")

    def sum_versions(self) -> int:
        """Return the version sum value."""
        operands_versions = sum(p.sum_versions() for p in self.operands)
        return self.version + operands_versions

    def eval(self) -> int:
        """Evaluate the packet to an int."""
        operation = {
            0: sum,
            1: math.prod,
            2: min,
            3: max,
            5: operator.gt,
            6: operator.lt,
            7: operator.eq,
        }[self.packet_type]
        if self.packet_type in BINARY_OPERATORS:
            a, b = [p.eval() for p in self.operands]
            return 1 if operation(a, b) else 0
        else:
            return operation(p.eval() for p in self.operands)

    def __str__(self) -> str:
        sub_packets = ", ".join(str(p) for p in self.operands)
        return f"{self.packet_type.name}({sub_packets})"


class BitStream(io.StringIO):
    """Bit stream reader."""

    def __init__(self, string: str):
        """Initialize and validate."""
        if any(s not in ("0", "1") for s in string):
            raise ValueError("invalid binary stream")
        super().__init__(string)
        self.length = len(string)

    @classmethod
    def from_hex(cls, string: str) -> BitStream:
        """Construct a BitStream from a hex string."""
        # Convert each hex value => int => padded binary.
        bits = "".join(f"{int(char, 16):04b}" for char in string)
        return cls(bits)

    @property
    def done(self) -> bool:
        """Return if the stream is done."""
        return self.tell() == self.length

    def read_int(self, count: int) -> int:
        """Read n bits and convert from binary to an int."""
        return int(self.read(count), 2)

    def read_literal(self) -> int:
        """Read a literal value.

        Read groups of 5 until the first bit is a 0.
        """
        literal = ""
        more = True
        while more:
            group = self.read(5)
            more = group[:1] == "1"
            literal += group[1:]
        return int(literal, 2)


def packet_parser(bits_io: BitStream) -> BasePacket:
    """Parse a BitStream to a Packet."""
    # Every packet starts with a version and packet_type.
    version = bits_io.read_int(3)
    packet_type = PacketType(bits_io.read_int(3))

    # Literals are easy. Read the literal value and we are done.
    if packet_type == PacketType.LITERAL:
        return Literal(version, packet_type, bits_io.read_literal())

    # Other operators have sub_packets.
    length_type = bits_io.read_int(1)
    sub_packets = []

    # Type 0: 15 bits indicating the body length
    if length_type == 0:
        length = bits_io.read_int(15)
        sub_io = BitStream(bits_io.read(length))
        while not sub_io.done:
            sub_packets.append(packet_parser(sub_io))

    # Type 0: 11 bits indicating a sub_packet count.
    else:
        packet_count = bits_io.read_int(11)
        for _ in range(packet_count):
            sub_packets.append(packet_parser(bits_io))

    return Operator(version, packet_type, sub_packets)


class Day16(aoc.Challenge):
    """Parse and evaluate Packet data."""

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
        """Parse the packets and sum up all the versions."""
        bits_io = BitStream.from_hex(parsed_input)
        return packet_parser(bits_io).sum_versions()

    def part2(self, parsed_input: str) -> int:
        """Parse the packets and evaluate."""
        bits_io = BitStream.from_hex(parsed_input)
        return packet_parser(bits_io).eval()

    def input_parser(self, puzzle_input: str) -> str:
        """Parse the input data."""
        return puzzle_input


if __name__ == "__main__":
    typer.run(Day16().run)

# vim:expandtab:sw=4:ts=4
