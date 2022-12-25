#!/bin/python

import pathlib
import sys


def time_to_sec(timestr: str) -> int:
    parts = timestr.split(":")
    return int(parts[0]) * 60 * 60 + int(parts[1]) * 60 + int(parts[2])


def fmt_time(seconds: int) -> str:
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"


txt = pathlib.Path(sys.argv[1]).read_text()
lines = txt.splitlines()
print(lines[0] + "   --------Delta---------")
print(lines[1] + "       Time   Rank  Score")
for line in lines[2:]:
    d, t1, r1, s1, t2, r2, s2 = line.strip().split()
    td = fmt_time(time_to_sec(t2) - time_to_sec(t1))
    rd = int(r2) - int(r1)
    ss = int(s1) + int(s2)
    print(f"{d:>3}   {t1}  {r1:>5}  {s1:>5}   {t2}  {r2:>5}  {s2:>5}   {td}  {rd:>5}  {ss:>5}")


