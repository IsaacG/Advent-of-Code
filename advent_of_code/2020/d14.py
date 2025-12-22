#!/usr/bin/env python
"""Day 14. Write data to memory?"""


def solve(data: list[tuple[str, ...]], part: int) -> int:
    """Read input. Track mask. Apply writes with the mem_writer.

    Both parts do similar read, track mask, apply write.
    They only differ in how a "write" is applied.
    """
    mem = dict[int, int]()
    mem_writer = write1 if part == 1 else write2
    mask = ''
    for (op, val) in data:
        if op == 'mask':
            mask = val
        else:
            mem_writer(mem, mask, int(op[4:-1]), int(val))
    return sum(mem.values())


def write1(mem: dict[int, int], mask: str, address: int, value: int):
    """Use the mask to modify the value then write it to memory.

    Replace X=>0 then do a bool-OR to apply 1's
    Replace X=>0 then do a bool-OR to apply 1's
    """
    m0 = int(mask.replace('X', '0'), 2)
    m1 = int(mask.replace('X', '1'), 2)
    mem[address] = (value | m0) & m1


def write2(mem: dict[int, int], mask: str, address: int, value: int):
    """Use the mask to generate multiple addresses to write the value to."""
    # 36-bit binary string of the address.
    padded_addr = f'{address:036b}'

    # Pass through address on mask=0, otherwise apply mask value.
    masked_addr = [b if a == '0' else a for a, b in zip(mask, padded_addr)]

    # If there are 3 X's, we need to write to 2^3 addresses, i.e.
    # there are 2^3 possible sunstitutes for those X's.
    # For each possible substitute for the X's,
    # make a binary string and replace the X's with the 0|1.
    count = sum(True for i in masked_addr if i == 'X')
    for i in range(2**count):
        # count-length binary string. 0 => 000 => [0, 0, 0]
        substitute = list(format(i, ('0%db' % count)))
        # Rebuild the address, replacing 'X' with a char from substitute.
        final_addr = [substitute.pop(0) if a == 'X' else a for a in masked_addr]
        addr = int("".join(final_addr), 2)
        mem[addr] = value


def input_parser(puzzle_input: str) -> list[tuple[str, ...]]:
    """Parse the input."""
    return [tuple(line.split(' = ')) for line in puzzle_input.split('\n')]


SAMPLE = ["""\
mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0""", """\
mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1"""]
TESTS = [
    (1, SAMPLE[0], 165),
    (2, SAMPLE[1], 208),
]
