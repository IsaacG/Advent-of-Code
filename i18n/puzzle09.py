"""i18n puzzle day N."""

import collections
import itertools
import datetime
import logging

log = logging.info


def build_date(order: tuple[int, int, int], date: tuple[int, int, int]) -> datetime.date:
    y, m, d = order
    yr, mn, dy = date[y], date[m], date[d]
    yr += 1900
    if yr < 1920:
        yr += 100
    return datetime.date(yr, mn, dy)


def valid_formats(dates: set[str]) -> set[str]:
    valid = set()
    for ymd in itertools.permutations(range(3)):
        # Exercise reads: (Note that the year can never be in the middle).
        if ymd[0] == 1:
            continue
        for date in dates:
            try:
                build_date(ymd, date)
            except ValueError:
                break
        else:
            valid.add(ymd)
    return valid


def solve(part: int, data: str) -> int:
    """Solve the parts."""
    entries = collections.defaultdict(set)
    for line in data.splitlines():
        date, people = line.split(": ")
        for person in people.split(", "):
            entries[person].add(tuple(int(i) for i in date.split("-")))
            # entries[person].add(date)

    upper = datetime.date(1920, 1, 1)
    lower = datetime.date(2020, 1, 1)
    target = datetime.date(2001, 9, 11)
    found = set()
    for person, dates in entries.items():
        ymds = valid_formats(dates)
        if len(ymds) > 1:
            print(person, dates, ymds)
        for ymd in ymds:
            if target in {build_date(ymd, date) for date in dates}:
                found.add(person)
                break

    return " ".join(sorted(found))



TEST_DATA = """\
16-05-18: Margot, Frank
02-17-04: Peter, Elise
06-02-29: Peter, Margot
31-09-11: Elise, Frank
09-11-01: Peter, Frank, Elise
11-09-01: Margot, Frank
"""
TESTS = [
    (1, TEST_DATA, "Margot Peter"),
]
