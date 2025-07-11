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

    def input_path(self, part: int) -> pathlib.Path:
        """Return the input file."""
        return pathlib.Path(f"inputs/{self.day:02}.txt")

    def module_path(self) -> str:
        return "."

    def module_name(self) -> str:
        """Return the module name."""
        return f"problem{self.day:02}"

    def download_input(self, year: int, day: int, part: int) -> str:
        """Download the input."""
        cookie = (pathlib.Path(os.getenv("XDG_DATA_HOME")) / "cookies/codyssi").read_text()
        cookie = cookie.strip().removeprefix("session=")
        session = requests.Session()
        session.cookies.set("session", cookie)
        response = session.get(f"https://www.codyssi.com/view_problem_{day}_input")
        et = etree.HTML(response.text)
        lines = [i.strip() for i in et.xpath("//body")[0].itertext() if i.strip()]
        content = "\n".join(lines)
        if "Codyssi - Error Page!" in content:
            raise LookupError("Unable to fetch input. Do you need a cookie refresh?")
        return content


@click.command()
@click.option("--day", "-d", type=int, required=True)
@click.option("--check", "-c", is_flag=True)
@click.option("--solve", "-s", is_flag=True)
@click.option("--test", "-t", is_flag=True)
@click.option("--part", "-p", "parts", type=int, multiple=True, default=(1, 2, 3))
@click.option("--live", "-l", is_flag=True)
@click.option("--verbose", "-v", count=True)
@click.option("--data", "--file", "data", type=str, required=False)
def main(day: int, check: bool, solve: bool, test: bool, live: bool, parts: tuple[int], verbose: int, data: str | None) -> None:
    Runner(year=2025, day=day, data=data, parts=parts, verbose=verbose).run(check, solve, test, live)


if __name__ == "__main__":
    main()

# vim:ts=4:sw=4:expandtab
