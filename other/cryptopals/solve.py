#!/bin/python

import base64
import itertools
import pathlib
import string
import sys

LETTER_FREQUENCY_PERCENT = [
    812, 149, 271, 432, 1202, 230, 203, 592, 731, 10, 69, 398, 261,
    695, 768, 182, 11, 602, 628, 910, 288, 111, 209, 17, 211, 7,
]
LETTER_FREQUENCY = dict(zip(string.ascii_letters.encode(), LETTER_FREQUENCY_PERCENT * 2))


# Set 1, Challenge 1
def hex_to_base64(data: str) -> str:
    """Return the base64 version of a hex string.

    >>> hex_to_base64("49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d")
    'SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t'
    """
    return base64.b64encode(bytes.fromhex(data)).decode()


# Set 1, Challenge 2
def xor(one: str, two: str) -> str:
    """Return the XOR of two hex strings.

    >>> xor('1c0111001f010100061a024b53535009181c', '686974207468652062756c6c277320657965')
    '746865206b696420646f6e277420706c6179'
    """
    data = bytearray(a ^ b for a, b in zip(bytes.fromhex(one), bytes.fromhex(two)))
    return data.hex()


# Set 1, Challenge 3
def xor_one_byte_decipher(data: str) -> str | None:
    """Return a string XOR'ed with one value.

    >>> xor_one_byte_decipher("1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736")
    "Cooking MC's like a pound of bacon"
    """
    b_data = bytes.fromhex(data)
    accept = set(string.ascii_letters + string.digits + ", '")
    for j in range(256):
        out = bytearray(i ^ j for i in b_data)
        try:
            text = out.decode()
        except UnicodeDecodeError:
            continue
        if False and text.isprintable():
            print(text)
        if set(text) <= accept:
            return out.decode()


# Set 1, Challenge 4
def xor_one_byte_detect(data: str) -> str:
    """Decrypt a one-byte XOR with a computed key.

    >>> xor_one_byte_detect(pathlib.Path("data/1.4.txt").read_text())
    ''
    """
    for line in data.splitlines():
        if (got := xor_one_byte_decipher(line)) is not None:
            return got.decode()


# Set 1, Challenge 5
def xor_multi_byte(data: str, key: str) -> str:
    """Return an XOR encrypted string with multiple bytes.

    >>> xor_multi_byte("Burning 'em, if you ain't quick and nimble I go crazy when I hear a cymbal", "ICE")
    '0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f'
    """
    return "".join(
        bytearray(a ^ b for a, b in zip(line.encode(), itertools.cycle(key.encode()))).hex()
        for line in data.splitlines()
    )


if __name__ == "__main__":
    import doctest
    doctest.testmod()

