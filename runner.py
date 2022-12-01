#!/bin/python3
"""Run AoC code in various flavors."""

import datetime
import importlib
import os
import pathlib
import string
import subprocess
import time
import traceback
from typing import List, Optional

import dotenv
import inotify_simple
import pytz
import typer

from pylib import site

EST = pytz.timezone("EST")


class Runner:
    """Code runner."""

    def __init__(self, year: int, day: int, watch: bool, timeout: int):
        self.day = day or self.now().day
        self.year = year or self.now().year
        self.timeout = timeout
        self.watch = watch
        self.base = pathlib.Path(__file__).parent / str(self.year)

    def from_template(self, day: int) -> None:
        """Create a new exercise file from template."""
        filename = self.base / f"{day:02}.py"
        if filename.exists():
            print(f"{filename.name} already exists")
            return
        template_file = self.base / "tmpl.py"
        template = string.Template(template_file.read_text())
        out = template.substitute(
            day=f"{day:02}",
            sample=site.Website(self.year, day).codeblocks(),
        )
        filename = self.base / f"{day:02}.py"
        filename.write_text(out)
        filename.chmod(0o700)

    def december(self):
        """Run live wait-solve for all of December."""
        year = self.now().year
        start = datetime.datetime(year, 11, 30, tzinfo=EST)
        end = datetime.datetime(year, 12, 25, 1, tzinfo=EST)
        while start < self.now() < end:
            solved = [int(line.split()[0]) for line in (self.base / "solutions.txt").read_text().splitlines()]
            if self.now().day in solved:
                print("Wait for tomorrow's problem to start and solve it.")
                self.wait_solve()
            else:
                print("Today's problem is not yet solved. Solve it now.")
                self.live_solve()

    @staticmethod
    def now() -> datetime.datetime:
        """Return datetime now."""
        return datetime.datetime.now(pytz.timezone("EST"))

    def wait_solve(self):
        """Wait for the clock to tick down then live solve."""
        now = self.now()
        day = datetime.timedelta(days=1)
        midnight = now.replace(hour=0, minute=0, second=0, microsecond=0) + day
        delay = midnight - now
        print(f"Next exercise starts in {delay.seconds} seconds.")
        while midnight > self.now():
            time.sleep((midnight - self.now()).seconds + 1)
        self.live_solve()

    def live_solve(self):
        """Solve a day live.

        Build from template, watch for test to pass, submit, repeat, exit.
        """
        if not self.day:
            day = self.now().day
        # Set up the file from template.
        self.from_template(day)
        # Import once to set up.
        module = importlib.import_module(f"{day:02}")
        obj = getattr(module, f"Day{day:02}")()
        raw_data = obj.raw_data(None)
        submitted = {1: False, 2: False}
        solutions = {}
        part = obj.site().part()
        if part is None:
            print("It looks like you completed this day.")
            self.update_solutions(day)
            return

        # Watch the file.
        inotify = inotify_simple.INotify()
        inotify.add_watch(self.base, inotify_simple.flags.CLOSE_WRITE)
        while events := inotify.read():
            if not any(i.name == f"{day:02}.py" for i in events):
                continue
            print(datetime.datetime.now().strftime("%H:%M:%S"))
            try:
                # Reload code and get the Challenge.
                module = importlib.reload(module)
                obj = getattr(module, f"Day{day:02}")()
                puzzle_input = obj.parse_input(raw_data)
                # Run tests for this part.
                obj.testing = True
                tests = [t for t in obj.TESTS if t.part == part and t.want != 0]
                if not tests:
                    print(f"No tests found for part {part}")
                    continue
                tests_pass = True
                for case in tests:
                    assert isinstance(case.inputs, str), "TestCase.inputs must be a string!"
                    data = obj.parse_input(case.inputs.strip())
                    got = obj.funcs[case.part](data)
                    if case.want != got:
                        print(f"FAILED! {case.part}: want({case.want}) != got({got})")
                        tests_pass = False
                obj.testing = False
                # If tests pass, try to submit.
                if not tests_pass:
                    print("Test failed")
                    continue
                if obj.SUBMIT[part] and not submitted[part]:
                    if answer := obj.funcs[part](puzzle_input):
                        submitted[part] = True
                        print("Submitting answer:", answer)
                        resp = obj.site().submit(answer)
                        print(f"Response: {resp}")
                        if "That's the right answer!" in resp:
                            print(f"Solved part {part}!!")
                            part += 1
                        else:
                            print(f"Incorrect answer for part {part}. You're on your own :(")
                            break
                    else:
                        print("No answer found")
                if part == 3:
                    print("Congrats!")
                    break
            except Exception:
                traceback.print_exc()

        self.update_solutions(day)
        print("Updated Solutions. Watch and run test/check.")

        if not solutions:
          solutions = {part: obj.funcs[part](puzzle_input) for part in (1, 2)}

        stop_at = self.now().replace(hour=4, minute=0, second=0, microsecond=0)
        while self.now() < stop_at:
            timeout = (stop_at - self.now()).seconds
            events = inotify.read(timeout=timeout)
            if not any(i.name == f"{day:02}.py" for i in events):
                continue
            print(datetime.datetime.now().strftime("%H:%M:%S"))
            try:
                # Reload code and get the Challenge.
                module = importlib.reload(module)
                obj = getattr(module, f"Day{day:02}")()
                puzzle_input = obj.parse_input(raw_data)
                # Run tests for this part.
                obj.testing = True
                tests = [t for t in obj.TESTS if t.want != 0]
                for case in tests:
                    data = obj.parse_input(case.inputs.strip())
                    got = obj.funcs[case.part](data)
                    if case.want == got:
                        print(f"TEST PASSED! {case.part}")
                    else:
                        print(f"TEST FAILED! {case.part}: want({case.want}) != got({got})")
                obj.testing = False
                # If tests pass, try to submit.
                for part in (1, 2):
                    got = obj.funcs[part](puzzle_input)
                    if solutions[part] == got:
                        print(f"CHECK PASSED! {part}")
                    else:
                        print(f"CHECK FAILED! {part}: want({solutions[part]}) != got({got})")
            except Exception:
                traceback.print_exc()
        print("Done for the day.")

    def update_solutions(self, day):
        # Reload code and get the Challenge.
        module = importlib.import_module(f"{day:02}")
        obj = getattr(module, f"Day{day:02}")()
        puzzle_input = obj.parse_input(obj.raw_data(None))
        solutions = {part: obj.funcs[part](puzzle_input) for part in (1, 2)}
        print(solutions)
        solution_line = f"{day:02} {solutions[1]} {solutions[2]}\n"
        solution_file = self.base / "solutions.txt"
        solution_values = solution_file.read_text()
        if solution_line not in solution_values:
            solution_values += f"{day:02} {solutions[1]} {solutions[2]}\n"
            solution_file.write_text(solution_values)

    def maybe_watch(self, func):
        """Run the function once or on every CLOSE_WRITE."""
        if not self.watch:
            return func(self.day)
        inotify = inotify_simple.INotify()
        inotify.add_watch(self.base, inotify_simple.flags.CLOSE_WRITE)
        while events := inotify.read():
            if not events[0].name.endswith(".py"):
                continue
            name = pathlib.Path(events[0].name).stem
            if not name.isnumeric():
                continue
            day = int(pathlib.Path(events[0].name).stem)
            print(datetime.datetime.now().strftime("%H:%M:%S"))
            func(day)
            print("Done.")

    def get_days(self, day):
        """Generate the filenames of the py code."""
        if day:
            day = f"{day:02d}"

        for file in sorted(self.base.glob(f"[0-9][0-9].py")):
            if day and file.stem != day:
                continue
            yield file

    def run_with_flags(self, flags: List[str]):
        """Run the .py file with a flag and data."""
        self.maybe_watch(lambda d: self._run_with_flags(flags, d))

    def _run_with_flags(self, flags: List[str], day: Optional[int]):
        for file in self.get_days(day):
            cmd = [file] + flags
            if self.timeout:
                if "--time" in flags and self.timeout == 30:
                    self.timeout = 120
                cmd = ["timeout", str(self.timeout)] + cmd
            try:
                process = subprocess.run(cmd)
            except Exception:
                traceback.print_exc()
                break
            if process.returncode == 124:
                print("TIMEOUT!")


def main(
    day: Optional[int] = None,
    waitlive: bool = False,
    december: bool = False,
    live: bool = False,
    test: bool = False,
    solve: bool = False,
    check: bool = False,
    submit: bool = False,
    watch: bool = False,
    timeit: bool = False,
    timeout: int = 30,
    year: Optional[int] = None,
):
    """Run the code in some fashion."""
    dotenv.load_dotenv()
    if year is None and os.getenv("YEAR"):
        year = os.getenv("YEAR")

    runner = Runner(year, day, watch, timeout)
    if december:
        return runner.december()
    if waitlive:
        return runner.wait_solve()
    if live:
        return runner.live_solve()
    flags = []
    if test:
        flags.append("--test")
    if solve:
        flags.append("--solve")
    if submit:
        flags.append("--submit")
    if timeit:
        flags.append("--timeit")
    if check:
        flags.append("--check")
    assert flags
    return runner.run_with_flags(flags)


if __name__ == "__main__":
    typer.run(main)

# vim:ts=2:sw=2:expandtab
