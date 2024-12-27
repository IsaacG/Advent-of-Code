#!/bin/python

import importlib

import pathlib
import resource
import time

import click


def format_ns(ns: float) -> str:
    units = [("ns", 1000), ("µs", 1000), ("ms", 1000), ("s", 60), ("mn", 60)]
    for unit, shift in units:
        if ns < shift:
            break
        ns /= shift
    else:
        unit = "hr"
    return f"{ns:>7.3f} {unit:>2}"


def timed(func, *args, **kwargs):
    start = time.perf_counter_ns()
    got = func(*args, **kwargs)
    end = time.perf_counter_ns()
    return format_ns(end - start), got


@click.command()
@click.option("--day", "-d", type=int, required=True)
@click.option("--check", "-c", is_flag=True)
@click.option("--solve", "-s", is_flag=True)
@click.option("--test", "-t", is_flag=True)
@click.option("--part", "-p", "parts", type=int, multiple=True, default=(1, 2, 3))
def main(day: int, check: bool, solve: bool, test: bool, parts: tuple[int]) -> None:
    module = importlib.import_module(f"quest_{day}")
    if test:
        for part in parts:
            for test_no, (test_part, test_data, test_want) in enumerate(module.TESTS):
                if test_part != part:
                    continue
                time_s, got = timed(module.solve, part=part, data=test_data)
                print(f"TEST  Part {part} {time_s} {'PASS' if got == test_want else 'FAIL'} (test {test_no})")
    if solve:
        for part in parts:
            data_path = pathlib.Path(f"inputs/{day:02}.{part}.txt")
            if not data_path.exists():
                print(f"SOLVE No input data found for day {day} part {part}")
                continue
            data = data_path.read_text().rstrip()
            time_s, got = timed(module.solve, part=part, data=data)
            print(f"SOLVE Part {part} {time_s} ---> {got}")
    if check:
        solutions_path = pathlib.Path(f"solutions/2024.txt")
        want_raw = next((line.split() for line in solutions_path.read_text().splitlines() if line.startswith(f"{day:02} ")), None)
        want = [int(i) for i in want_raw[1:]]
        for part in parts:
            data_path = pathlib.Path(f"inputs/{day:02}.{part}.txt")
            data = data_path.read_text().rstrip()
            time_s, got = timed(module.solve, part=part, data=data)
            if got == want[part - 1]:
                print(f"CHECK Part {part} {time_s} PASS")
            else:
                print(f"CHECK Part {part} {time_s} FAIL. Wanted {want[part -1]} but got {got}.")


if __name__ == "__main__":
    main()

# vim:ts=4:sw=4:expandtab
