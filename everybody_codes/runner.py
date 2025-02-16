#!/bin/python

import datetime
import importlib
import inspect
import logging
import os
import pathlib
import requests
import resource
import time
import typing

import click
import inotify_simple  # type: ignore
from lib import helpers


T = typing.TypeVar("T")


def get_solutions(day: int) -> list[int] | None:
    solutions_path = pathlib.Path(f"solutions/2024.txt")
    want_raw = next((line for line in solutions_path.read_text().splitlines() if line.startswith(f"{day:02} ")), None)
    if want_raw is None or len(want_raw.split("\t")) < 4:
        session = requests.Session()
        cookie_file = pathlib.Path(os.getenv("XDG_DATA_HOME")) / "everyone.codes.cookie"
        cookie = cookie_file.read_text().strip()
        session.cookies.set("everybody-codes", cookie)
        data = session.get(f"https://everybody.codes/api/event/2024/quest/{day}").json()
        want = [f"answer{i}" for i in range(1, 4)]
        if not set(want).issubset(set(data)):
            return None
        new_line = "\t".join([f"{day:02}"] + [data[i] for i in want])
        solutions = [line for line in solutions_path.read_text().splitlines() if line.split("\t")[0] != f"{day:02}"]
        solutions.append(new_line)
        solutions_path.write_text("\n".join(solutions) + "\n")
        want_raw = new_line
    if want_raw is None:
        return None
    return want_raw.split("\t")[1:]


def run_day(day: int, check: bool, solve: bool, test: bool, parts: tuple[int], formatter) -> None:
    module = importlib.import_module(f"quest_{day:02}")
    module = importlib.reload(module)
    if test:
        for part in parts:
            formatter.set_part(part)
            for test_no, (test_part, test_data, test_want) in enumerate(module.TESTS, 1):
                if test_part != part:
                    continue
                time_s, got = helpers.timed(module.solve, part=part, data=test_data, testing=True)
                if got == test_want:
                    print(f"TEST  {day:02}.{part} {time_s} PASS (test {test_no})")
                else:
                    print(f"TEST  {day:02}.{part} {time_s} FAIL (test {test_no}). Got {got} but wants {test_want}.")
    if solve:
        for part in parts:
            formatter.set_part(part)
            data_path = pathlib.Path(f"inputs/{day:02}.{part}.txt")
            download_path = pathlib.Path(os.getenv("HOME")) / "remote"/ "Downloads" / f"everybody_codes_e2024_q{day:02}_p{part}.txt"
            if not data_path.exists() and download_path.exists():
                data_path.write_text(download_path.read_text())
                download_path.unlink()
            if not data_path.exists():
                print(f"SOLVE No input data found for day {day} part {part}")
                continue
            data = data_path.read_text().rstrip()
            time_s, got = helpers.timed(module.solve, part=part, data=data, testing=False)
            print(f"SOLVE {day:02}.{part} {time_s} ---> {got}")
    if check:
        want = get_solutions(day)
        if want is None:
            print(f"No solutions found for {day}")
        else:
            for part in parts:
                formatter.set_part(part)
                data_path = pathlib.Path(f"inputs/{day:02}.{part}.txt")
                data = data_path.read_text().rstrip()
                time_s, got = helpers.timed(module.solve, part=part, data=data, testing=False)
                if str(got) == want[part - 1]:
                    print(f"CHECK {day:02}.{part} {time_s} PASS")
                else:
                    print(f"CHECK {day:02}.{part} {time_s} FAIL. Wanted {want[part -1]} but got {got}.")


@click.command()
@click.option("--day", "-d", type=int, required=True)
@click.option("--check", "-c", is_flag=True)
@click.option("--solve", "-s", is_flag=True)
@click.option("--test", "-t", is_flag=True)
@click.option("--part", "-p", "parts", type=int, multiple=True, default=(1, 2, 3))
@click.option("--live", "-l", is_flag=True)
@click.option("--verbose", "-v", count=True)
def main(day: int, check: bool, solve: bool, test: bool, live: bool, parts: tuple[int], verbose: int) -> None:
    formatter = helpers.setup_logging(day, verbose)
    helpers.setup_resources()
    run_day(day, check, solve, test, parts, formatter)
    if not live:
        return
    inotify = inotify_simple.INotify()
    inotify.add_watch(pathlib.Path(__file__).parent, inotify_simple.flags.CLOSE_WRITE)
    count = 0
    while events := inotify.read():
        if not any(i.name == f"quest_{day:02}.py" for i in events):
            continue
        count += 1
        print(datetime.datetime.now().strftime(f"== {count:02}: %H:%M:%S =="))
        run_day(day, check, solve, test, parts, formatter)


if __name__ == "__main__":
    main()

# vim:ts=4:sw=4:expandtab
