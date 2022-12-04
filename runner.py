#!/bin/python3
"""Run AoC code in various flavors."""

import dataclasses
import datetime
import importlib
import multiprocessing
import os
import pathlib
import string
import sys
import time
import traceback
import zoneinfo
from typing import Optional

import click
import dotenv
import inotify_simple

from pylib import aoc
from pylib import site

EST = zoneinfo.ZoneInfo("America/New_York")


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

    def challenge(self) -> aoc.Challenge:
        """Return a Challenge instance."""
        return getattr(self.module(), f"Day{self.day:02}")()

    def run_code(self, run_args: dict[str, bool | None], timeout: int) -> None:
        """Run the challenge code, with a timeout."""
        proc = multiprocessing.Process(target=self.challenge().run, kwargs=run_args)

        proc.start()
        proc.join(timeout=timeout)
        if proc.is_alive():
            print("Timed out waiting for Challenge.")
            proc.terminate()


@dataclasses.dataclass
class Runner:
    """Code runner."""

    year: int
    day: int
    watch: bool
    timeout: int

    def __post_init__(self) -> None:
        self.day = self.day or self.now().day
        self.year = self.year or self.now().year
        self.base = pathlib.Path(__file__).parent / str(self.year)

        cwd = pathlib.Path(os.getcwd())
        if cwd.name != str(self.year) and (cwd / str(self.year)).exists():
            sys.path.append(str(cwd / str(self.year)))

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
        return datetime.datetime.now(EST)

    def midnight_tomorrow(self) -> datetime.datetime:
        """Return the next midnight."""
        now = self.now()
        one_day = datetime.timedelta(days=1)
        return now.replace(hour=0, minute=0, second=0, microsecond=0) + one_day

    def wait_solve(self) -> None:
        """Wait for the clock to tick down then live solve."""
        now = self.now()
        midnight = self.midnight_tomorrow()
        delay = midnight - now
        print(f"Next exercise starts in {delay.seconds} seconds.")
        while midnight > self.now():
            time.sleep((midnight - self.now()).seconds + 1)
        self.day = self.now().day
        self.live_solve()

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
        solutions = {}
        part = obj.site.part()
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
                puzzle_input = obj.input_parser(raw_data)
                # Run tests for this part.
                obj.testing = True
                tests = [t for t in obj.TESTS if t.part == part and t.want != 0]
                if not tests:
                    print(f"No tests found for part {part}")
                    continue
                tests_pass = True
                for case in tests:
                    assert isinstance(case.inputs, str), "TestCase.inputs must be a string!"
                    data = obj.input_parser(case.inputs.strip())
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
                        resp = obj.site.submit(answer)
                        print(f"Response: {resp}")
                        if "That's the right answer!" in resp:
                            print(f"Solved part {part}!!")
                            part += 1
                        elif m := re.search(r"Please wait (.*) (minute|second)s? before trying again.", resp):
                            amount = m.group(1)
                            units = {"second": 1, "minute": 60}[m.group(2)]
                            seconds = "zero one two three four five six seven eight nine ten".split().index(amount) * units
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
                puzzle_input = obj.input_parser(raw_data)
                # Run tests for this part.
                obj.testing = True
                tests = [t for t in obj.TESTS if t.want != 0]
                for case in tests:
                    data = obj.input_parser(case.inputs.strip())
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
        puzzle_input = obj.input_parser(obj.raw_data(None))
        solutions = {part: obj.funcs[part](puzzle_input) for part in (1, 2)}
        print(solutions)
        solution_line = f"{day:02} {solutions[1]} {solutions[2]}\n"
        solution_file = self.base / "solutions.txt"
        solution_values = solution_file.read_text()
        if solution_line not in solution_values:
            solution_values += f"{day:02} {solutions[1]} {solutions[2]}\n"
            solution_file.write_text(solution_values)


@click.command()
@click.option("--day", type=int, required=False, help="AoC day")
@click.option("--year", type=int, required=False, help="AoC year")
@click.option("--waitlive", is_flag=True, help="Wait for midnight then live solve.")
@click.option("--december", is_flag=True, help="Live solve all days.")
@click.option("--live", is_flag=True, help="Live solve one day: setup, watch, test, submit.")
@click.option("--test", is_flag=True, help="Test if the sample input/solution works.")
@click.option("--solve", is_flag=True, help="Generate the solution.")
@click.option("--check", is_flag=True, help="Check if the results in solution.txt match with the generated solution.")
@click.option("--submit", is_flag=True, help="Submit the next part on AoC website.")
@click.option("--watch", is_flag=True, help="If set, loop and repeat the action when the file is saved.")
@click.option("--benchmark", is_flag=True, help="Time the solution.")
@click.option("--all-days", is_flag=True, help="Run action for all days.")
@click.option("--timeout", type=int, default=30, help="Set the timeout.")
def main(
    day: Optional[int],
    waitlive,
    december,
    live: bool,
    test: bool,
    solve: bool,
    check: bool,
    submit: bool,
    watch: bool,
    benchmark: bool,
    all_days: bool,
    timeout: int,
    year: Optional[int],
):
    """Run the code in some fashion."""
    dotenv.load_dotenv()
    now = datetime.datetime.now(EST).date()
    year = int(year or os.getenv("YEAR") or now.year)
    day = day or now.day
    year_dir = pathlib.Path(__file__).parent / str(year)

    runner = Runner(year, day, watch, timeout)
    if december:
        return runner.december()
    if waitlive:
        return runner.wait_solve()
    if live:
        return runner.live_solve()

    run_args = {"data": None, "test": test, "solve": solve, "submit": submit, "check": check, "benchmark": benchmark}

    if not watch or all_days:
        if all_days:
            days = sorted(p.stem for p in year_dir.glob("[0-2][0-9].py"))
        else:
            days = [day]

        for day in days:
            ChallengeRunner(year, day).run_code(run_args, timeout)
        return

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
        ChallengeRunner(year, day).run_code(run_args, timeout)
        print("Done.")
        print()
    return


if __name__ == "__main__":
    main()

# vim:ts=4:sw=4:expandtab
