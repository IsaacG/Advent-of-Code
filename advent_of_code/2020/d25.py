#!/usr/bin/env python
"""Brute force solve Diffie Hellman key exchange."""

MODULO = 20201227


def transform(subject: int, loop_counter: int) -> int:
    """Apply the transform function."""
    num = 1
    for _ in range(loop_counter):
        num = (num * subject) % MODULO
    return num


def force(w0, w1):
    """Brute force the loop_counter to "solve" Diffie Hellman."""
    attempt = 0
    num = 1
    while num not in [w0, w1]:
        attempt += 1
        num = (num * 7) % MODULO
    return attempt, 0 if num == w0 else 1


def solve(data: list[str], part: int) -> int:
    """Brute force the key.

    Brute force both public keys to find the smaller loop counter.
    Use the loop counter to transform the *other* public key.
    """
    del part
    loop_counter, key_index = force(*data)
    return transform(data[1 - key_index], loop_counter)


TESTS = [(1, "5764801\n17807724\n", 14897079)]
