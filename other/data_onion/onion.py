#!/bin/python
import base64
import collections
import io
import itertools
import os
import pathlib
import subprocess
import struct
import sys

from lxml import etree
from Cryptodome.Cipher import AES
from Cryptodome.Util import Counter
import requests


ASCII85 = bytearray(b"!\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuz")


def get_path(n: int, data: bool) -> pathlib.Path:
    return pathlib.Path(f".cache/payload.{n}." + ("data" if data else "instructions") + ".txt")

def load(n: int, data: bool) -> str:
    path = get_path(n, data)
    if not path.exists():
        write(PARTS[n](get_data(n - 1) if n else ""), n)
    return path.read_text()


def get_data(n: int) -> bytes:
    return base64.a85decode(load(n, data=True).strip(), adobe=True)


def get_instructions(n: int) -> str:
    return load(n, data=False)


def write(out, n):
    if not out:
        print("Nothing to write")
        return
    parts = out.strip().split("\n\n")
    for data, output in [(False, "\n\n".join(parts[:-1])), (True, parts[-1])]:
        path = get_path(n, data=data)
        if not path.exists():
            path.write_text(output)


def starting(data: bytes) -> str:
    page = requests.get("https://www.tomdalling.com/toms-data-onion/").text
    return etree.HTML(page).xpath("//pre/text()")[0].strip()


def layer0(data: bytes) -> str:
    """Layer 0/6: ASCII85."""
    return data.decode().strip()


def layer1(data: bytes) -> str:
    """Layer 1/6: Bitwise Operations."""

    def transform(x):
        x ^= 0b01010101
        low = x & 1
        return (x >> 1) | (low << 7)

    return bytearray([transform(x) for x in data]).decode().strip()


def layer2(data: bytes) -> str:
    """Layer 2/6: Parity Bit."""
    parts = []
    count = 0
    group = 0
    for byte in data:
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

    return bytearray(parts).decode()


def layer3(data: bytes) -> str:
    """Layer 3/6: XOR Encryption."""
    key = []
    allowed = bytearray(b"!\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuz\n")
    for idx in range(32):
        options = []
        for byte in range(256):
            if all(i ^ byte in allowed for i in data[idx+500*32:32_000:32]):
                key.append(byte)
                break
    return bytearray([a ^ b for a, b in zip(itertools.cycle(key), data)]).decode()


def layer4(data: bytes) -> str:
    """Layer 4/6: Network Traffic."""
    mask = (1 << 16) - 1

    def ones_complement(x: int) -> int:
        assert x <= mask, x
        return mask - x

    def checksum_ok(block: bytes) -> bool:
        words = [int.from_bytes(block[i:i + 2]) for i in range(0, len(block), 2)]
        checksum = 0
        for word in words:
            checksum += ones_complement(word)
            if checksum > mask:
                checksum = (checksum & mask) + 1
        return ones_complement(checksum) == 0

    want_from = bytes(bytearray([10, 1, 1, 10]))  #  10.1.1.10
    want_to = bytes(bytearray([10, 1, 1, 200]))   # 10.1.1.200
    want_port = 42069

    raw_data_in = io.BytesIO(data)
    data_out = io.BytesIO()
    valid_count = 0
    packets_count = 0

    while raw_data_in.tell() < len(data):
        ipv4_header = raw_data_in.read1(20)
        udp_header = raw_data_in.read1(8)
        udp_length = int.from_bytes(udp_header[4:6])
        udp_data = raw_data_in.read1(udp_length - 8)

        src = ipv4_header[12:16]
        dst = ipv4_header[16:20]
        udp_to_port = int.from_bytes(udp_header[2:4])

        ipv4_length = int.from_bytes(ipv4_header[2:4])
        assert ipv4_length == udp_length + 20

        udp_pseudo_header = src + dst + (17).to_bytes(2) + udp_length.to_bytes(2) + udp_header + udp_data
        # Pad to 16 bits.
        if udp_length % 2:
            udp_pseudo_header += bytes(bytearray([0]))

        packets_count += 1
        if src == want_from and dst == want_to and udp_to_port == want_port and checksum_ok(ipv4_header) and checksum_ok(udp_pseudo_header):
            data_out.write(udp_data)
            valid_count += 1
    print("Valid packets:", valid_count, "out of", packets_count)
    return data_out.getvalue().decode()


def layer5(data: bytes) -> str:
    """Layer 5/6: Advanced Encryption Standard."""
    # - First 32 bytes: The 256-bit key encrypting key (KEK).
    # - Next 8 bytes: The 64-bit initialization vector (IV) for
    #   the wrapped key.
    # - Next 40 bytes: The wrapped (encrypted) key. When
    #   decrypted, this will become the 256-bit encryption key.
    # - Next 16 bytes: The 128-bit initialization vector (IV) for
    #   the encrypted payload.
    # - All remaining bytes: The encrypted payload.

    QUAD = struct.Struct('>Q')

    def aes_unwrap_key_and_iv(kek, wrapped):
        n = len(wrapped)//8 - 1
        #NOTE: R[0] is never accessed, left in for consistency with RFC indices
        R = [None]+[wrapped[i*8:i*8+8] for i in range(1, n+1)]
        A = QUAD.unpack(wrapped[:8])[0]
        decrypt = AES.new(kek, AES.MODE_ECB).decrypt
        for j in range(5,-1,-1): #counting down
            for i in range(n, 0, -1): #(n, n-1, ..., 1)
                ciphertext = QUAD.pack(A^(n*j+i)) + R[i]
                B = decrypt(ciphertext)
                A = QUAD.unpack(B[:8])[0]
                R[i] = B[8:]
        return b"".join(R[1:]), A

    kek = data[0:32]
    kiv = int.from_bytes(data[32:40])
    wrapped_key = data[40:80]
    div = data[80:96]
    encrypted = data[96:]

    decrypted_data_key, got_iv = aes_unwrap_key_and_iv(kek, wrapped_key)
    assert kiv == got_iv
    assert len(decrypted_data_key) == 32

    cmd = ["openssl", "enc", "-aes-256-ctr", "-d"]
    cmd.extend(["-K", decrypted_data_key.hex()])
    cmd.extend(["-iv", div.hex()])
    proc = subprocess.run(cmd, capture_output=True, input=encrypted)
    return proc.stdout.decode()


def layer6(data: bytes) -> str:
    """Layer 6/6: Virtual Machine."""
    memory = dict(enumerate(bytearray(data)))
    print(" ".join(f"{i:08b}" for i in data[:15]))
    print(" ".join(f"{i:08b}" for i in data[15:30]))
    data_out = io.BytesIO()
    reg = {i: 0 for i in "abcdef"} | {f"l{i}": 0 for i in "abcd"} | {i: 0 for i in ["ptr", "pc"]}

    regmap = {
        False: dict(enumerate("abcdef", start=1)), # short
        True: dict(enumerate(["la", "lb", "lc", "ld", "ptr", "pc"], start=1)), # long
    }

    def memread(i: int, long: bool) -> int:
        if 1 <= i <= 6:
            return reg[regmap[long][i]]
        elif i == 7 and not long:
            target = reg["ptr"] + reg["c"]
            if target > len(memory):
                print(reg["ptr"], reg["c"], f"{target=} {len(memory)=}")
            return memory.get(target, 0)
        raise ValueError()

    def memwrite(i: int, long: bool, val: int) -> int:
        if 1 <= i <= 6:
            target = regmap[long][i]
            print(f"memwrite {target} = {val}")
            reg[target] = val
        elif i == 7 and not long:
            memory[reg["ptr"] + reg["c"]] = val
        else:
            raise ValueError(f"Invalid write to destination {i} {long=}")

    OPS = {
        0xC2: "ADD", 0xE1: "APTR", 0xC1: "CMP", 0x01: "HALT",
        0x21: "JEZ", 0x22: "JNZ", 0x02: "OUT", 0xC3: "SUB", 0xC4: "XOR",
    }

    def get_pc(size: int) -> int:
        pc = reg["pc"]
        val = int.from_bytes(bytes(bytearray([memory[i] for i in range(pc, pc + size)])))
        reg["pc"] += size
        if size == 1:
            print(f"@{pc:3} read {val:08b} = {val}")
        else:
            print(f"@{pc:3} read {val:32b} = {val}")
        return val

    for i in range(1000):
        op = get_pc(1)
        print(f"{i + 1}: @{reg["pc"]:4}: {op:3} = {op:02x} = {op:08b}")
        # print(OPS.get(op, "MV"))
        match op:
            case 0xC2:  # (1 byte) ADD a <- b
                reg["a"] = (reg["a"] + reg["b"]) % 256
            case 0xE1:  # 0x__ (2 bytes) APTR imm8
                reg["ptr"] += get_pc(1)
                print(f"APTR {reg["ptr"]=}")
            case 0xC1:  # (1 byte) CMP
                reg["f"] = 0 if reg["a"] == reg["b"] else 1
            case 0x01:  # (1 byte) HALT
                break
            case 0x21:  # 0x__ 0x__ 0x__ 0x__ (5 bytes) JEZ imm32
                imm = get_pc(4)
                if reg["f"] == 0:
                    reg["pc"] = imm
            case 0x22:  # 0x__ 0x__ 0x__ 0x__ (5 bytes) JNZ imm32
                imm = get_pc(4)
                if reg["f"] != 0:
                    reg["pc"] = imm
            case 0x02:  # (1 byte) OUT a
                data_out.write(reg["a"].to_bytes(1))
            case 0xC3:  # (1 byte) SUB a <- b
                reg["a"] = (reg["a"] - reg["b"]) % 256
            case 0xC4:  # (1 byte) XOR a <- b
                reg["a"] = reg["a"] ^ reg["b"]
            case _:
                # 0b01DDDSSS:  # (1 byte) MV {dest} <- {src}
                # 0b10DDDSSS:  # (1 byte) MV32 {dest} <- {src}
                # 0b01DDD000:  # 0x__ (2 bytes) MVI {dest} <- imm8
                # 0b10DDD000:  # 0x__ 0x__ 0x__ 0x__ (5 bytes) MVI32 {dest} <- imm32
                long = (op & 0b11000000) == 0b10000000
                src = op & 0b111
                dst = (op >> 3) & 0b111
                if src != 0:
                    val = memread(src, long)
                    print(f"Read {val} from {src} {long}")
                else:
                    val = get_pc(4 if long else 1)
                memwrite(dst, long, val)

    return data_out.getvalue().decode()



PARTS = [starting, layer0, layer1, layer2, layer3, layer4, layer5, layer6]

if len(sys.argv) > 1:
    print(get_instructions(int(sys.argv[1])))
layer5(get_data(5))

