#!/bin/python
"""Advent of Code, Day 15: Lens Library."""
import collections


def lense_hash(word: str) -> int:
    """Compute the HASH of a word."""
    value = 0
    for char in word:
        value = (value + ord(char)) * 17
    return value % 256


def solve(data: str, part: int) -> int:
    """Return which lenses are in the boxes."""
    if part == 1:
        return sum(lense_hash(word) for word in data.split(","))
    boxes = collections.defaultdict[int, dict[int, str]](dict)

    def get_box(label):
        return boxes[lense_hash(label)]

    for word in data.split(","):
        if word.endswith("-"):
            label = word.removesuffix("-")
            get_box(label).pop(label, None)
        else:
            label, length = word.split("=")
            get_box(label)[label] = length

    # Sum up the lenses.
    result = 0
    for idx_box, lenses in boxes.items():
        for idx_lens, length in enumerate(lenses.values(), start=1):
            result += (idx_box + 1) * idx_lens * int(length)
    return result


SAMPLE = "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"
TESTS = [(1, "HASH", 52), (1, SAMPLE, 1320), (2, SAMPLE, 145)]
# vim:expandtab:sw=4:ts=4
