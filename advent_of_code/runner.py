#!/bin/python

import os
import pathlib

import click
import requests
from lib import running


class Runner(running.Runner):

    def solutions_path(self) -> pathlib.Path:
        """Return the solution file."""
        return pathlib.Path(f"solutions/{self.year}.txt")

    def input_path(self, part: int) -> pathlib.Path:
        """Return the input file."""
        return pathlib.Path(f"inputs/{self.year}.{self.day:02}.txt")

    def module_path(self) -> str:
        return str(self.year)

    def module_name(self) -> str:
        """Return the module name."""
        return f"d{self.day:02}"

    def download_input(self, year: int, day: int, part: int) -> str | None:
        """Download the input."""
        return None


@click.command()
@click.option("--day", "-d", type=int, required=True)
@click.option("--year", "-y", type=int, default=2025)
@click.option("--check", "-c", is_flag=True)
@click.option("--solve", "-s", is_flag=True)
@click.option("--test", "-t", is_flag=True)
@click.option("--part", "-p", "parts", type=int, multiple=True, default=(1, 2, 3))
@click.option("--live", "-l", is_flag=True)
@click.option("--verbose", "-v", count=True)
def main(day: int, year: int, check: bool, solve: bool, test: bool, live: bool, parts: tuple[int], verbose: int) -> None:
    if day > 100:
        year, day = divmod(day, 100)
    if year < 2000:
        year += 2000
    Runner(
        year=year, day=day, data=None, parts=parts, verbose=verbose,
    ).run(check, solve, test, live)


if __name__ == "__main__":
    main()

# vim:ts=4:sw=4:expandtab
