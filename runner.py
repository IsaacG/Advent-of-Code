#!/bin/python3
"""Run AoC code in various flavors."""
from __future__ import annotations

import dataclasses
import datetime
import importlib
import multiprocessing
import os
import pathlib
import re
import resource
import string
import sys
import time
import traceback
import zoneinfo
from typing import Optional

import click
import dotenv
import inotify_simple  # type: ignore

from pylib import aoc
from pylib import site

EST = zoneinfo.ZoneInfo("America/New_York")
NUMBERS = "zero one two three four five six seven eight nine ten".split()


@dataclasses.dataclass
class ChallengeRunner:
    """Manage the challenge for a single, specific day."""

    year: int
    day: int

    def __post_init__(self) -> None:
        """Initialize."""
        self._module = importlib.import_module(f"{self.day:02}")

    def module(self):
        """Reload and return the module."""
        self._module = importlib.reload(self._module)
        return self._module

    def challenge(self, *args, **kwargs) -> aoc.Challenge:
        """Return a Challenge instance."""
        return getattr(self.module(), f"Day{self.day:02}")(*args, **kwargs)

    def run_code(
        self,
        run_args: dict[str, bool | None],
        input_file: Optional[str],
        part: tuple[int, ...],
        timeout: int,
    ) -> None:
        """Run the challenge code, with a timeout."""
        for mode, run in run_args.items():
            if not run:
                continue

            try:
                target = self.challenge(parts_to_run=part)
            except SyntaxError:
                traceback.print_exc()
                return
            if target.TIMEOUT and target.TIMEOUT > timeout:
                target.debug(f"Challenge overrides timeout {timeout} => {target.TIMEOUT}")
                timeout = target.TIMEOUT
            proc = multiprocessing.Process(
                target=target.run, kwargs={"input_file": input_file, mode: True}
            )

            proc.start()
            proc.join(timeout=timeout)
            if proc.is_alive():
                print(f"{self.year}/{self.day} Timed out waiting for Challenge.")
                proc.terminate()


@dataclasses.dataclass(frozen=True)
class Runner:
    """Code runner."""

    year: int
    day: int
    watch: bool
    timeout: int

    def __post_init__(self) -> None:
        cwd = pathlib.Path(os.getcwd())
        if cwd.name != str(self.year) and (cwd / str(self.year)).exists():
            sys.path.append(str(cwd / str(self.year)))

    @classmethod
    def build(klass, year: Optional[int], day: Optional[int], watch: bool, timeout: int) -> Runner:
        day = day or klass.now().day
        year = year or klass.now().year
        return klass(year, day, watch, timeout)

    @property
    def base(self):
        return pathlib.Path(__file__).parent / str(self.year)

    def from_template(self, day: int) -> None:
        """Create a new exercise file from template."""
        filename = self.base / f"{day:02}.py"
        if filename.exists():
            print(f"{filename.name} already exists")
            return
        template_file = self.base / "../shared/tmpl.py"
        template = string.Template(template_file.read_text())
        website = site.Website(self.year, day)
        out = template.substitute(
            day=f"{day:02}",
            sample=website.codeblocks(),
            title=website.title().strip("- "),
        )
        filename = self.base / f"{day:02}.py"
        filename.write_text(out)
        filename.chmod(0o700)

    def december(self, timeout: int) -> None:
        """Run live wait-solve for all of December."""
        year = self.now().year
        start = datetime.datetime(year, 11, 30, tzinfo=EST)
        end = datetime.datetime(year, 12, 25, 1, tzinfo=EST)
        while start < self.now() < end:
            solved = [int(line.split()[0]) for line in (self.base / "solutions.txt").read_text().splitlines()]
            if self.now().day in solved:
                print("Wait for tomorrow's problem to start and solve it.")
                self.wait_solve(timeout)
            else:
                print("Today's problem is not yet solved. Solve it now.")
                self.live_solve()

    @staticmethod
    def now() -> datetime.datetime:
        """Return datetime now."""
        return datetime.datetime.now(EST)

    @classmethod
    def midnight_tomorrow(klass) -> datetime.datetime:
        """Return the next midnight."""
        now = klass.now()
        one_day = datetime.timedelta(days=1)
        return now.replace(hour=0, minute=0, second=0, microsecond=0) + one_day

    @classmethod
    def wait_solve(klass, timeout: int) -> None:
        """Wait for the clock to tick down then live solve."""
        now = klass.now()
        midnight = klass.midnight_tomorrow()
        print(f"Next exercise starts in {(midnight - now).seconds} seconds.")

        stops = (60, 30, 15, 10, 5, 4, 3, 2, 1, 0)
        for offset, nxt in zip(stops, stops[1:]):
            delay: float = (midnight - klass.now()).seconds - offset
            if delay <= 0:
                continue
            print(f"{delay + offset} seconds to go!")
            time.sleep(delay)
        while midnight >= klass.now():
            delay = (midnight - klass.now()).seconds + 0.1
            time.sleep(delay)
        print("Solve!!!")
        return klass.build(year=None, day=None, watch=False, timeout=timeout).live_solve()

    def live_solve(self) -> None:
        """Solve a day live.

        Build from template, watch for test to pass, submit, repeat, exit.
        """
        day = self.day or self.now().day
        # Set up the file from template.
        self.from_template(day)
        # Import once to set up.
        module = importlib.import_module(f"{day:02}")
        obj = getattr(module, f"Day{day:02}")()
        raw_data = obj.raw_data(None)
        submitted = {1: False, 2: False}
        solutions: dict[int, int | str] = {}
        part = obj.site.part()
        if part is None:
            print("It looks like you completed this day.")
            self.update_solutions(day)
        else:
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
                    # Run tests for this part.
                    obj.testing = True
                    tests = [t for t in obj.TESTS if t.part == part and t.want != 0]
                    if not tests:
                        print(f"No tests found for part {part}")
                        continue
                    tests_pass = True
                    for case in tests:
                        if case.want == aoc.TEST_SKIP:
                            continue
                        assert isinstance(case.inputs, str), "TestCase.inputs must be a string!"
                        if len(case.inputs) <= 1:
                            print('WARNING TestCase.inputs is less than two chars.')
                        got = obj.run_solver(part, case.inputs.rstrip())
                        if case.want != got:
                            print(f"FAILED! {case.part}: want({case.want}) != got({got})")
                            tests_pass = False
                    obj.testing = False
                    # If tests pass, try to submit.
                    if not tests_pass:
                        print("Test failed")
                        continue
                    if obj.SUBMIT[part] and not submitted[part]:
                        if answer := obj.run_solver(part, raw_data):
                            assert not isinstance(answer, float)
                            print("Submitting answer:", answer)
                            resp = obj.site.submit(answer)
                            print(f"Response: {resp}")
                            if "That's the right answer!" in resp:
                                print(f"Solved part {part}!!")
                                self.update_solutions(day, {part: answer})
                                submitted[part] = True
                                part += 1
                            elif m := re.search(r"Please wait (.*) (minute|second)s? before trying again.", resp):
                                amount = m.group(1)
                                units = {"second": 1, "minute": 60}[m.group(2)]
                                seconds = NUMBERS.index(amount) * units
                                print(f"Waiting {seconds} seconds.")
                                time.sleep(seconds)
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

        print("Watch and run test/check.")
        if not solutions:
            solutions = {part: obj.run_solver(part, raw_data) for part in (1, 2)}
        inotify = inotify_simple.INotify()
        inotify.add_watch(self.base, inotify_simple.flags.CLOSE_WRITE)

        stop_at = self.now() + datetime.timedelta(hours=6)
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
                obj.test()
                obj.check()
            except Exception:
                traceback.print_exc()
        print("Done for the day.")

    def read_solutions(self) -> dict[int, dict[int, int | str]]:
        """Return solutions from file."""
        solutions: dict[int, dict[int, int | str]] = {}
        for line in (self.base / "solutions.txt").read_text().splitlines():
            if not line:
                continue
            parts = line.split()
            solutions[int(parts[0])] = {
                part: int(val) if val.isdigit() else val
                for part, val in enumerate(parts[1:], start=1)
            }
        return solutions

    def update_solutions(self, day: int, solutions: Optional[dict[int, int | str]] = None) -> None:
        """Update the solution file."""
        existing = self.read_solutions()
        if day not in existing:
            existing[day] = {}

        solutions = existing[day]
        if len(solutions) == 2:
            return
        stored = solutions.copy()

        # Reload code and get the Challenge.
        module = importlib.import_module(f"{day:02}")
        obj = getattr(module, f"Day{day:02}")()
        parts = [1] if day == 25 else [1, 2]
        for part in parts:
            if part not in solutions:
                if got := obj.run_solver(part, obj.raw_data(None)):
                    solutions[part] = got

        if solutions == stored:
            print("Existing solutions up to date.")
            return

        print(f"Writing solutions to file. {solutions[day]}")
        lines = [
            " ".join(
                [f"{line_day:02}"]
                + [str(existing[line_day][p]) for p in (1, 2) if p in existing[line_day]]
            )
            for line_day in sorted(existing)
        ]

        solution_file = self.base / "solutions.txt"
        solution_file.write_text("\n".join(lines))


@click.command()
@click.option("--date", "-d", type=str, required=False, help="YYYY/dd")
@click.option("--day", type=int, required=False, help="AoC day")
@click.option("--year", type=int, required=False, help="AoC year")
@click.option("--waitlive", is_flag=True, help="Wait for midnight then live solve.")
@click.option("--december", is_flag=True, help="Live solve all days.")
@click.option("--live", is_flag=True, help="Live solve one day: setup, watch, test, submit.")
@click.option("--test", "-t", is_flag=True, help="Test if the sample input/solution works.")
@click.option("--solve", is_flag=True, help="Generate the solution.")
@click.option(
    "--check", "-c", is_flag=True,
    help="Check if the results in solution.txt match with the generated solution.",
)
@click.option("--submit", is_flag=True, help="Submit the next part on AoC website.")
@click.option("--part", type=int, multiple=True, default=(1, 2), help="Which parts to run.")
@click.option("--watch", is_flag=True, help="If set, loop and repeat the action when the file is saved.")
@click.option("--benchmark", is_flag=True, help="Time the solution.")
@click.option("--all-days", is_flag=True, help="Run action for all days.")
@click.option("--timeout", type=int, default=30, help="Set the timeout.")
@click.option("--input-file", "--input", "--file", type=str, default=None, help="Alternative input file.")
@click.option("--cookie", type=str, required=False, help="Set cookie")
def main(
    date: Optional[str],
    day: Optional[int],
    waitlive,
    december,
    live: bool,
    test: bool,
    solve: bool,
    check: bool,
    submit: bool,
    part: tuple[int, ...],
    watch: bool,
    benchmark: bool,
    all_days: bool,
    input_file: Optional[str],
    timeout: int,
    year: Optional[int],
    cookie: Optional[str],
) -> None:
    """Run the code in some fashion."""
    os.nice(19)
    resource.setrlimit(resource.RLIMIT_RSS, (int(10e9), int(100e9)))
    dotenv.load_dotenv()
    if cookie:
        site.Website(0, 0, False).set_cookie(cookie)
        return None
    if date:
        assert year is None and day is None
        m = re.match(r"^(\d{2}|\d{4}).??(\d{1,2})$", date)
        assert m
        year = int(m.group(1))
        if year < 2000:
            year += 2000
        day = int(m.group(2))
    now = datetime.datetime.now(EST).date()
    year = int(year or os.getenv("YEAR") or now.year)
    day = day or now.day
    year_dir = pathlib.Path(__file__).parent / str(year)

    runner = Runner.build(year, day, watch, timeout)
    if december:
        return runner.december(timeout)
    if waitlive:
        return runner.wait_solve(timeout)
    if live:
        return runner.live_solve()

    run_args: dict[str, bool | None] = {
        "test": test,
        "solve": solve,
        "submit": submit,
        "check": check,
        "benchmark": benchmark,
    }

    if not watch or all_days:
        if all_days:
            days = sorted(int(p.stem) for p in year_dir.glob("[0-2][0-9].py"))
        else:
            days = [day]

        for day in days:
            ChallengeRunner(year, day).run_code(run_args, input_file, part, timeout)
        return None

    # Set up inotify watches and run a Challenge in a loop.
    inotify = inotify_simple.INotify()
    inotify.add_watch(year_dir, inotify_simple.flags.CLOSE_WRITE)
    while events := inotify.read():
        if not events[0].name.endswith(".py"):
            continue
        name = pathlib.Path(events[0].name).stem
        if not name.isnumeric():
            continue
        day = int(pathlib.Path(events[0].name).stem)
        print(datetime.datetime.now().strftime("%H:%M:%S"))
        ChallengeRunner(year, day).run_code(run_args, input_file, part, timeout)
        print("Done.")
        print()
    return None


if __name__ == "__main__":
    main()

# vim:ts=4:sw=4:expandtab
