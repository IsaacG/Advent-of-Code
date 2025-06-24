#!/bin/python

import os
import pathlib

import click
from lib import running


class Runner(running.Runner):

    def solutions_path(self) -> pathlib.Path:
        """Return the solution file."""
        return pathlib.Path(f"{self.year}/solutions.txt")

    def input_path(self, part: int) -> pathlib.Path:
        """Return the input file."""
        p = pathlib.Path(f"{self.year}/inputs/{self.day:02}.{part}.txt")
        return pathlib.Path(f"{self.year}/inputs/{self.day:02}.{part}.txt")

    def module_path(self) -> str:
        return self.year

    def module_name(self) -> str:
        """Return the module name."""
        return f"quest_{self.day:02}"

    def download_input(self, year: int, day: int, part: int) -> str:
        """Download the input."""
        return (pathlib.Path(os.getenv("HOME")) / "remote/Downloads" / f"everybody_codes_e1_q{day:02}_p{part}.txt").read_text()


@click.command()
@click.option("--day", "-d", type=int, required=True)
@click.option("--event", "-e", type=str, default="story01")
@click.option("--check", "-c", is_flag=True)
@click.option("--solve", "-s", is_flag=True)
@click.option("--test", "-t", is_flag=True)
@click.option("--part", "-p", "parts", type=int, multiple=True, default=(1, 2, 3))
@click.option("--live", "-l", is_flag=True)
@click.option("--verbose", "-v", count=True)
def main(day: int, event: str, check: bool, solve: bool, test: bool, live: bool, parts: tuple[int], verbose: int) -> None:
    Runner(
        year=event, day=day, data=None, parts=parts, verbose=verbose,
    ).run(check, solve, test, live)


if __name__ == "__main__":
    main()

# vim:ts=4:sw=4:expandtab
