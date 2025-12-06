#!/bin/python
import base64
import pathlib


def get_data(n: int) -> bytes:
    path = pathlib.Path(f"payload.{n}.txt")
    if not path.exists():
        PARTS[n - 1]()
    return base64.a85decode(path.read_text().strip(), adobe=True)


def get_instructions(n: int) -> str:
    path = pathlib.Path(f"payload.{n}.instructions.txt")
    if not path.exists():
        PARTS[n - 1]()
    return path.read_text()


def write(out, n):
    parts = out.strip().split("\n\n")
    path = pathlib.Path(f"payload.{n}.instructions.txt")
    if not path.exists():
        pathlib.Path(f"payload.{n}.instructions.txt").write_text("\n\n".join(parts[:-1]))
    path = pathlib.Path(f"payload.{n}.txt")
    if not path.exists():
        path.write_text(parts[-1])


def p0():
    out = get_data(0).decode().strip()
    write(out, 1)


def p1():

    def transform(x):
        x ^= 0b01010101
        low = x & 1
        return (x >> 1) | (low << 7)

    out = bytearray([transform(x) for x in get_data(1)]).decode().strip()
    write(out, 2)


def p2():
    parts = []
    count = 0
    group = 0
    for byte in get_data(2):
        # assert byte < 256
        if byte.bit_count() % 2 == 1:
            continue
        group <<= 7
        group |= (byte >> 1)
        count += 1
        if count == 8:
            nums = []
            count = 0
            for _ in range(7):
                num = group & ((1 << 8) - 1)
                # assert num < 256
                nums.append(num)
                group >>= 8
            # assert group == 0
            parts.extend(nums[::-1])

    out = bytearray(parts).decode()
    write(out, 3)


PARTS = [p0, p1, p2]

print(get_instructions(3))

