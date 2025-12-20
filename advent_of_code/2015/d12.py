#!/bin/python
"""Advent of Code, Day 12: JSAbacusFramework.io. Count int values in JSON."""

import json
import typing
from lib import parsers


def doc_sum(obj, skip_red: bool) -> int:
    """Sum integers in an object."""
    if isinstance(obj, str):
        return 0
    if isinstance(obj, int):
        return obj
    if isinstance(obj, list):
        return sum(doc_sum(i, skip_red) for i in obj)
    if isinstance(obj, dict):
        if skip_red and "red" in obj.values():
            return 0
        return sum(doc_sum(i, skip_red) for i in obj.values())
    raise ValueError(obj)


def solve(data: typing.Any, part: int) -> int:
    """Return sum ints, possibly excluding red objects."""
    return doc_sum(data, part == 2)


PARSER = parsers.ParseCustom(json.loads)
SAMPLE = ["[1,2,3]", '[1, {"a": "red", "b": 2}, 3]']
TESTS = [
    (1, SAMPLE[0], 6),
    (1, SAMPLE[1], 6),
    (2, SAMPLE[0], 6),
    (2, SAMPLE[1], 4),
]
