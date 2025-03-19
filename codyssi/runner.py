#!/bin/python

import os
import pathlib
from lxml import etree

import click
import requests
from lib import running


class Runner(running.Runner):

    def solutions_path(self) -> pathlib.Path:
        """Return the solution file."""
        return pathlib.Path(f"solutions.txt")

    def input_path(self, year: int, day: int, part: int) -> pathlib.Path:
        """Return the input file."""
        return pathlib.Path(f"inputs/{day:02}.txt")

    def module_name(self, year: int, day: int) -> str:
        """Return the module name."""
        return f"problem{day:02}"

    def download_input(self, year: int, day: int, part: int) -> str:
        """Download the input."""
        cookie = (pathlib.Path(os.getenv("XDG_DATA_HOME")) / "cookies/odyssi").read_text().strip()
        session = requests.Session()
        session.cookies.set("session", cookie)
        response = session.get(f"https://www.codyssi.com/view_problem_{day}_input")
        et = etree.HTML(response.text)
        lines = [i.strip() for i in et.xpath("//body")[0].itertext() if i.strip()]
        return "\n".join(lines)


@click.command()
@click.option("--day", "-d", type=int, required=True)
@click.option("--check", "-c", is_flag=True)
@click.option("--solve", "-s", is_flag=True)
@click.option("--test", "-t", is_flag=True)
@click.option("--part", "-p", "parts", type=int, multiple=True, default=(1, 2, 3))
@click.option("--live", "-l", is_flag=True)
@click.option("--verbose", "-v", count=True)
def main(day: int, check: bool, solve: bool, test: bool, live: bool, parts: tuple[int], verbose: int) -> None:
    Runner().run(day, check, solve, test, live, parts, verbose)


if __name__ == "__main__":
    main()

# vim:ts=4:sw=4:expandtab
