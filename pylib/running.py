#!/bin/python

import collections.abc
import dataclasses
import datetime
import importlib
import inspect
import logging
import os
import pathlib
import requests
import resource
import sys
import time
import typing

import inotify_simple  # type: ignore
from lib import helpers


T = typing.TypeVar("T")


@dataclasses.dataclass
class Runner:
    year: int
    day: int
    data: str | None
    parts: collections.abc.Iterable[int]
    verbose: bool

    def __post_init__(self):
        """Initialize."""
        cwd = pathlib.Path(os.getcwd())
        module_path = cwd / self.module_path()
        if cwd.name != self.module_path() and module_path.exists() and str(module_path) not in sys.path:
            sys.path.append(str(module_path))

    def solutions_path(self) -> pathlib.Path:
        """Return the solution file."""
        raise NotImplemented

    def input_path(self, year: int, day: int, part: int) -> pathlib.Path:
        """Return the input file."""
        raise NotImplemented

    def module_name(self, year: int, day: int) -> str:
        """Return the module name."""
        raise NotImplemented

    def download_input(self, year: int, day: int, part: int) -> str:
        """Download the input."""
        raise NotImplemented

    def get_solutions(self, day: int) -> list[int] | None:
        solutions_path = self.solutions_path()
        want_raw = [line for line in solutions_path.read_text().splitlines() if line.startswith(f"{day:02}.")]
        if not want_raw:
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
        if not want_raw:
            return None
        return [line.split(maxsplit=1)[1] for line in want_raw]

    def input_data(self, part: int) -> str:
        """Return the input data."""
        if self.data:
            data_path = pathlib.Path(self.data)
        else:
            data_path = self.input_path(self.year, self.day, part)
            if not data_path.exists():
                data_path.write_text(self.download_input(self.year, self.day, part))
        if not data_path.exists():
            return None
        return data_path.read_text().rstrip()

    def run_day(self, check: bool, solve: bool, test: bool, formatter) -> None:
        module = importlib.import_module(self.module_name())
        module = importlib.reload(module)
        if test:
            for part in self.parts:
                formatter.set_part(part)
                for test_no, (test_part, test_data, test_want) in enumerate(module.TESTS, 1):
                    if test_part != part:
                        continue
                    time_s, got = helpers.timed(module.solve, part=part, data=test_data, testing=True)
                    if got == test_want:
                        print(f"TEST  {self.day:02}.{part} {time_s} PASS (test {test_no})")
                    else:
                        print(f"TEST  {self.day:02}.{part} {time_s} FAIL (test {test_no}). Got {got} but wants {test_want}.")
        if solve:
            for part in self.parts:
                formatter.set_part(part)
                data = self.input_data(part)
                if data is None:
                    print(f"SOLVE No input data found for day {self.day} part {part}")
                    continue
                time_s, got = helpers.timed(module.solve, part=part, data=data, testing=False)
                print(f"SOLVE {self.day:02}.{part} {time_s} ---> {got}")
        if check:
            want = self.get_solutions(self.day)
            if want is None:
                print(f"No solutions found for {self.day}")
            else:
                for part in self.parts:
                    formatter.set_part(part)
                    data = self.input_data(part)
                    if data is None:
                        print(f"CHECK No input data found for day {day} part {part}")
                        continue
                    time_s, got = helpers.timed(module.solve, part=part, data=data, testing=False)
                    if str(got) == want[part - 1]:
                        print(f"CHECK {self.day:02}.{part} {time_s} PASS")
                    else:
                        print(f"CHECK {self.day:02}.{part} {time_s} FAIL. Wanted {want[part -1]} but got {got}.")


    def run(self, check: bool, solve: bool, test: bool, live: bool) -> None:
        formatter = helpers.setup_logging(self.day, self.verbose)
        helpers.setup_resources()
        self.run_day(check, solve, test, formatter)
        if not live:
            return
        inotify = inotify_simple.INotify()
        inotify.add_watch(pathlib.Path(__file__).parent, inotify_simple.flags.CLOSE_WRITE)
        count = 0
        while events := inotify.read():
            if not any(i.name == self.module_name() + ".py" for i in events):
                continue
            count += 1
            print(datetime.datetime.now().strftime(f"== {count:02}: %H:%M:%S =="))
            self.run_day(check, solve, test, formatter)

# vim:ts=4:sw=4:expandtab
