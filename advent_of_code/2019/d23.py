#!/bin/python
"""Advent of Code, Category Six."""
import intcode


def solve(data: str, part: int) -> int:
    """Construct a computer network."""
    # Initialize and run computers.
    computers = [intcode.Computer(data) for _ in range(50)]
    for i, c in enumerate(computers):
        c.input.append(i)
        c.run()

    nat = 0, 0
    nat_sent = set()

    while True:
        # Read output packets.
        for i, c in enumerate(computers):
            while len(c.output) >= 3:
                dst, *packet = c.output.popleft(), c.output.popleft(), c.output.popleft()
                if dst == 255:
                    if part == 1:
                        return packet[1]
                    nat = packet
                else:
                    # Route the output packets to the dest input
                    computers[dst].input.extend(packet)
        # Check for no inputs, ie idle network.
        if all(not c.input for c in computers):
            if nat[1] in nat_sent:
                return nat[1]
            computers[0].input.extend(nat)
            nat_sent.add(nat[1])
        # Continue running, providing -1 when there is no input.
        for c in computers:
            if not c.input:
                c.input.append(-1)
            c.run()


TESTS = list[tuple[int, int, int]]()
