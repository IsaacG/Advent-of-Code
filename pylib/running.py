#!/bin/python

import collections.abc
import dataclasses
import datetime
import importlib
import logging
import os
import pathlib
import requests
import resource
import shutil
import sys
import time
import typing

import inotify_simple  # type: ignore
from lib import helpers
from lib import parsers


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

    def input_path(self, part: int) -> pathlib.Path:
        """Return the input file."""
        raise NotImplemented

    def module_name(self, year: int, day: int) -> str:
        """Return the module name."""
        raise NotImplemented

    def download_input(self, year: int, day: int, part: int) -> str:
        """Download the input."""
        raise NotImplemented

    def submit_solution(self, year: int, day: int, solutions: list[int | str]) -> str:
        """Submit the solution."""
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

    def input_data(self, part: int) -> str | None:
        """Return the input data."""
        if self.data:
            data_path = pathlib.Path(self.data)
        else:
            data_path = self.input_path(part)
            if not data_path.exists():
                data = self.download_input(self.year, self.day, part)
                if data is None:
                    return None
                data_path.write_text(data)
        if not data_path.exists():
            return None
        return data_path.read_text().rstrip("\n")

    def compare(self, want, data: typing.Any, msg_success: str, msg_fail: str, func: typing.Callable, **kwargs) -> bool:
        time_s, got = helpers.timed(func, data=data, **kwargs)
        if str(got) == str(want):
            print(msg_success % time_s)
            return True
        msg = msg_fail % (time_s, got)
        if str(want).isdigit() and str(got).isdigit():
            delta = int(want) - int(got)
            if delta > 0:
                msg += f" Too low by {delta}."
            else:
                msg += f" Too high by {-delta}."
        print(msg)

    def test(self, module, parser: parsers.BaseParser, formatter) -> bool:
        success = True
        for part in self.parts:
            formatter.set_part(part)
            for test_number, (test_part, test_data, test_want) in enumerate(module.TESTS, 1):
                if test_part != part:
                    continue
                success = success and self.compare(
                    test_want, parser(test_data.rstrip("\n")),
                    f"TEST  {self.year}.{self.day:02}.{part} %s PASS (test {test_number})",
                    f"TEST  {self.year}.{self.day:02}.{part} %s FAIL (test {test_number}). Got %r but wants {test_want!r}.",
                    module.solve,
                    part=part, testing=True, test_number=test_number,
                )
        return success

    def solve(self, module, parser: parsers.BaseParser, formatter) -> list[str | int]:
        solutions = []
        for part in self.parts:
            formatter.set_part(part)
            data = self.input_data(part)
            if data is None:
                print(f"SOLVE No input data found for day {self.day} part {part}")
                continue
            time_s, got = helpers.timed(module.solve, part=part, data=parser(data), testing=False, test_number=None)
            solutions.append(got)
            print(f"SOLVE {self.day:02}.{part} {time_s} ---> {got}")
        return solutions

    def submit(self, module, parser: parsers.BaseParser, formatter) -> None:
        if not self.test(module, parser, formatter):
            print("Tests failed; skip submit.")
            return
        solutions = self.solve(module, parser, formatter)
        self.submit_solution(self.year, self.day, solutions)

    def check(self, module, parser: parsers.BaseParser, formatter) -> None:
        want = self.get_solutions(self.day)
        if want is None:
            print(f"No solutions found for {self.day}")
            return
        for part in self.parts:
            if part > len(want):
                continue
            formatter.set_part(part)
            data = self.input_data(part)
            if data is None:
                print(f"CHECK No input data found for day {self.day} part {part}")
                continue
            self.compare(
                want[part - 1], parser(data),
                f"CHECK {self.year}.{self.day:02}.{part} %s PASS",
                f"CHECK {self.year}.{self.day:02}.{part} %s FAIL. Wanted {want[part -1]} but got %s.",
                module.solve,
                part=part, testing=False, test_number=None,
            )

    def run_day(self, check: bool, solve: bool, test: bool, submit: bool, formatter) -> None:
        solution_file = pathlib.Path(f"{self.year}/{self.module_name()}.py")
        if not solution_file.exists():
            shutil.copyfile("tmpl.py", solution_file)
        module = importlib.import_module(self.module_name())
        module = importlib.reload(module)
        parser_override = getattr(module, "PARSER", None) or getattr(module, "input_parser", None)
        parser = parsers.get_parser(self.input_data(1), parser_override)
        for want, func in [(test, self.test), (solve, self.solve), (check, self.check), (submit, self.submit)]:
            if want:
                func(module, parser, formatter)

    def run(self, check: bool, solve: bool, test: bool, submit: bool, live: bool) -> None:
        formatter = helpers.setup_logging(self.day, self.verbose)
        helpers.setup_resources()
        self.run_day(check, solve, test, submit, formatter)
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
            self.run_day(check, solve, test, submit, formatter)

# vim:ts=4:sw=4:expandtab
