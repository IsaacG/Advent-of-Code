#!/bin/python

import os
import pathlib
import sys

import click
import requests
from lxml import etree
from lib import running


class Runner(running.Runner):

    def session(self):
        cookie = (pathlib.Path(os.getenv("XDG_DATA_HOME")) / "cookies/aoc").read_text().strip()
        session = requests.Session()
        session.cookies.set("session", cookie.removeprefix("session="))
        return session

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
        url = f"https://adventofcode.com/{year}/day/{day}/input"
        resp = self.session().get(url)
        resp.raise_for_status()
        return resp.text

    def submit_solution(self, year: int, day: int, solutions: list[int | str]) -> str:
        session = self.session()
        resp = session.get(f'https://adventofcode.com/{self.year}/day/{self.day}')
        resp.raise_for_status()
        et = etree.HTML(resp.text)

        levels = et.xpath('//form/input[@name="level"]/@value')
        if not levels:
            print('No submission box found; is this already completed?')
            return None

        level = levels[0]
        resp = session.post(f'https://adventofcode.com/{self.year}/day/{self.day}/answer', data={'answer': solutions[-1], 'level': str(level)})
        resp.raise_for_status()
        et = etree.HTML(resp.content)
        output = ''.join(et.xpath('//main/article//text()'))
        return f"Submitted solution {solutions[-1]} for level {level}.\n\nResponse:\n" + output


@click.command()
@click.option("--day", "-d", type=int, required=True)
@click.option("--year", "-y", type=int, default=2025)
@click.option("--check", "-c", is_flag=True)
@click.option("--solve", "-s", is_flag=True)
@click.option("--test", "-t", is_flag=True)
@click.option("--submit", "-x", is_flag=True)
@click.option("--part", "-p", "parts", type=int, multiple=True, default=(1, 2))
@click.option("--live", "-l", is_flag=True)
@click.option("--verbose", "-v", count=True)
def main(day: int, year: int, check: bool, solve: bool, test: bool, submit: bool, live: bool, parts: tuple[int], verbose: int) -> None:
    if day > 100:
        year, day = divmod(day, 100)
    if year < 2000:
        year += 2000
    got = Runner(
        year=year, day=day, data=None, parts=parts, verbose=verbose,
    ).run(check, solve, test, submit, live)
    if not got:
        sys.exit(1)


if __name__ == "__main__":
    main()

# vim:ts=4:sw=4:expandtab
