"""i18n puzzle day N."""

import datetime
import zoneinfo
import logging

log = logging.info

def solve(part: int, data: str) -> int:
    """Solve the parts."""
    times = []
    for block in data.split("\n\n"):
        for line in block.splitlines():
            _, tz, dts = line.split(maxsplit=2)
            dt = datetime.datetime.strptime(dts, "%b %d, %Y, %H:%M")
            times.append(dt.replace(tzinfo=zoneinfo.ZoneInfo(tz)))
    seconds = sum((b - a).total_seconds() for a, b in zip(times[::2], times[1::2]))
    return int(seconds // 60)




TEST_DATA = """\
Departure: Europe/London                  Mar 04, 2020, 10:00
Arrival:   Europe/Paris                   Mar 04, 2020, 11:59

Departure: Europe/Paris                   Mar 05, 2020, 10:42
Arrival:   Australia/Adelaide             Mar 06, 2020, 16:09

Departure: Australia/Adelaide             Mar 06, 2020, 19:54
Arrival:   America/Argentina/Buenos_Aires Mar 06, 2020, 19:10

Departure: America/Argentina/Buenos_Aires Mar 07, 2020, 06:06
Arrival:   America/Toronto                Mar 07, 2020, 14:43

Departure: America/Toronto                Mar 08, 2020, 04:48
Arrival:   Europe/London                  Mar 08, 2020, 16:52
"""
TESTS = [
    (1, TEST_DATA, 3143),
]
