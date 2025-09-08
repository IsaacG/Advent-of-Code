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
        # cookie = (pathlib.Path(os.getenv("XDG_DATA_HOME")) / "cookies/codyssi").read_text()
        # cookie = cookie.strip().removeprefix("session=")
        session = requests.Session()
        session.cookies.set("session", ".eJw9jbEOgjAURX_FvNlFkWjcJGhRUw3YgK8LKZUISq1SMALh32XR9Z6cczsQUqbGxJW-pw9YwjXTsfO-6LNq2I7ZezxZnsJgpv2j41juK1hMh3U9hzFoUVdZbCpRpbDsYJQMOnWlhRF-qMKGkzA7sNUEo7XNVVBwxhW2RY4MG0qw5e7mTkl448xvDozanAQ59GOoTVpeS10__1XphXlCituPPoQaLmFrhJAE-i9SRkEr.G58KqA.riFYOFgR5PQyV7iAlfEu72tSzas")
        desktop_user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
        session.headers['User-Agent'] = desktop_user_agent
        response = session.get(f"https://challenges.aquaq.co.uk/challenge/{day - 1}/input.txt")
        return response.text


@click.command()
@click.option("--day", "-d", type=int, required=True)
@click.option("--check", "-c", is_flag=True)
@click.option("--solve", "-s", is_flag=True)
@click.option("--test", "-t", is_flag=True)
@click.option("--live", "-l", is_flag=True)
@click.option("--verbose", "-v", count=True)
@click.option("--data", "--file", "data", type=str, required=False)
def main(day: int, check: bool, solve: bool, test: bool, live: bool, verbose: int, data: str | None) -> None:
    Runner(year=2025, day=day, data=data, parts=[1], verbose=verbose).run(check, solve, test, live)


if __name__ == "__main__":
    main()

# vim:ts=4:sw=4:expandtab
