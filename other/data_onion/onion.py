#!/bin/python
import base64
import io
import itertools
import pathlib
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

    def ones_complement(x: int) -> int:
        assert x <= mask, x
        return mask - x

    def checksum_ok(block: bytes) -> bool:
        words = [int.from_bytes(block[i:i + 2]) for i in range(0, len(block), 2)]
        checksum = 0
        for word in words:
            checksum += ones_complement(word)
            if checksum >> 16:
                checksum = (checksum & mask) + 1
        return not ones_complement(checksum)

    mask = (1 << 16) - 1
    want_from = bytes(bytearray([10, 1, 1, 10]))  #  10.1.1.10
    want_to = bytes(bytearray([10, 1, 1, 200]))   # 10.1.1.200
    i = io.BytesIO(data)
    o = io.BytesIO()
    while i.tell() < len(data):
        ip4_header = i.read1(20)
        udp_header = i.read1(8)
        src = ip4_header[12:16]
        dst = ip4_header[16:20]
        udp_length = int.from_bytes(udp_header[4:6])
        ip4_length = int.from_bytes(ip4_header[2:4])
        assert ip4_length == udp_length + 20
        udp_data = i.read1(udp_length - 8)
        udp_pseudo_header = src + dst + (17).to_bytes(2) + udp_length.to_bytes(2) + udp_header + udp_data
        if udp_length % 2:
            udp_pseudo_header += bytes(bytearray([0]))
        if src == want_from and dst == want_to and checksum_ok(ip4_header) and checksum_ok(udp_pseudo_header):
            o.write(udp_data)
    return o.getvalue().decode()


def layer5(data: bytes) -> str:
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

    iv = int.from_bytes(div)
    ctr = Counter.new(AES.block_size * 8, initial_value=iv)

    cipher = AES.new(decrypted_data_key, mode=AES.MODE_CTR, counter=ctr)
    decrypted = cipher.decrypt(encrypted)
    unpad = lambda s: s[:-ord(s[len(s)-1:])]
    decrypted = unpad(decrypted)

    print(decrypted)
    return decrypted.decode()


PARTS = [starting, layer0, layer1, layer2, layer3, layer4, layer5]

print(get_instructions(int(sys.argv[1])))

