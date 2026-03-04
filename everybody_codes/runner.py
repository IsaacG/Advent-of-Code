#!/usr/bin/python

import os
import pathlib

import click
import requests
from lib import running

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad


class Runner(running.Runner):

    def solutions_path(self) -> pathlib.Path:
        """Return the solution file."""
        return pathlib.Path(f"{self.year}/solutions.txt")

    def write_solutions(self, year: int, day: int) -> str:
        """Write the solutions to file."""
        cookie = (pathlib.Path(os.getenv("XDG_DATA_HOME")) / "cookies/ec").read_text().strip()
        session = requests.Session()
        session.cookies.set("everybody-codes", cookie)

        year = year.removeprefix("event").removeprefix("story").removeprefix("0")
        data = session.get(f"https://api.everybody.codes/event/{year}/quest/{day}").json()
        want = [f"answer{i}" for i in range(1, 4)]
        if not set(want).issubset(set(data)):
            return None
        solutions = [line for line in self.solutions_path().read_text().splitlines() if not line.split(maxsplit=1)[0].startswith(f"{day:02}")]
        answers = []
        for part in range(1, 4):
            answers.append(f"{day:02}.{part} {data[f"answer{part}"]}")
        self.solutions_path().write_text("\n".join(solutions + answers) + "\n")
        return answers

    def input_path(self, part: int) -> pathlib.Path:
        """Return the input file."""
        p = pathlib.Path(f"{self.year}/inputs/{self.day:02}.{part}.txt")
        return pathlib.Path(f"{self.year}/inputs/{self.day:02}.{part}.txt")

    def module_path(self) -> str:
        return self.year

    def module_name(self) -> str:
        """Return the module name."""
        return f"quest_{self.day:02}"

    def download_input(self, year: int, day: int, part: int) -> str | None:
        """Download the input."""
        # Hard coded per account, see https://api.everybody.codes/user/me
        seed = 49
        year = year.removeprefix("event").removeprefix("story").removeprefix("0")

        cookie = (pathlib.Path(os.getenv("XDG_DATA_HOME")) / "cookies/ec").read_text().strip()

        session = requests.Session()
        session.cookies.set("everybody-codes", cookie)

        data = session.get(f"https://everybody.codes/assets/{year}/{day}/input/{seed}.json").json()
        metadata = session.get(f"https://api.everybody.codes/event/{year}/quest/{day}").json()

        aes_key = metadata[f"key{part}"].encode()
        cipher = AES.new(aes_key, AES.MODE_CBC, iv=aes_key[:AES.block_size])
        plaintext = cipher.decrypt(bytes.fromhex(data[str(part)]))
        return unpad(plaintext, AES.block_size).decode()


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
