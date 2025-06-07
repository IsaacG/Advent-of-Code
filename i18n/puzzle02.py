"""i18n puzzle day N."""

import collections
import datetime
import logging

log = logging.info

def solve(part: int, data: str) -> int:
    """Solve the parts."""
    count = collections.defaultdict(int)
    for line in data.splitlines():
        ts = datetime.datetime.fromisoformat(line).astimezone(tz=datetime.timezone.utc)
        count[ts] += 1
        if count[ts] == 4:
            return ts.isoformat()

    


TEST_DATA = """\
2019-06-05T08:15:00-04:00
2019-06-05T14:15:00+02:00
2019-06-05T17:45:00+05:30
2019-06-05T05:15:00-07:00
2011-02-01T09:15:00-03:00
2011-02-01T09:15:00-05:00
"""
TESTS = [
    (1, TEST_DATA, "2019-06-05T12:15:00+00:00"),
]
