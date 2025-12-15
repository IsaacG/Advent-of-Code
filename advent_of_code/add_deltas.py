#!/bin/python

import json
import pathlib
import sys


def seconds(timestr: str) -> int:
    if timestr == ">24h":
        return 0
    parts = timestr.split(":")
    return int(parts[0]) * 60 * 60 + int(parts[1]) * 60 + int(parts[2])


def fmt_time(seconds: int) -> str:
    if seconds == 0:
        return ">24h"
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"


def add_deltas_old():
    txt = pathlib.Path(sys.argv[1]).read_text()
    lines = txt.splitlines()
    print(lines[0] + "   --------Delta---------")
    print(lines[1] + "       Time   Rank  Score")
    for line in lines[2:]:
        d, t1, r1, s1, t2, r2, s2 = line.strip().split()
        td = fmt_time(seconds(t2) - seconds(t1))
        rd = int(r2) - int(r1)
        ss = int(s1) + int(s2)
        print(f"{d:>3}   {t1:>8}  {r1:>5}  {s1:>5}   {t2:>8}  {r2:>5}  {s2:>5}   {td:>8} {rd:>6}  {ss:>5}")


def format_new():
    personal_times = pathlib.Path(sys.argv[1]).read_text()
    ranking_data = json.loads(pathlib.Path(sys.argv[2]).read_text())
    times = {}
    for line in personal_times.strip().splitlines():
        a, b, c = line.strip().split()
        times[a] = seconds(b), seconds(c)
    for day, (one, two) in sorted(times.items(), key=lambda x:int(x[0])):
        for idx, time in enumerate(ranking_data["data"]["2025"][day]["1"]):
            if one < time:
                p1 = idx*10+5
                break
        for idx, time in enumerate(ranking_data["data"]["2025"][day]["2"]):
            if two < time:
                p2 = idx*10+5
                break
        print(f"{day:>2}   {b} {p1:>5}   {c} {p2:>5}   {fmt_time(two-one)}")


format_new()

