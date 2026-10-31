#!/usr/bin/python

import itertools
import json
import os
import pathlib

import click
import requests
from lib import running

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from lxml import etree


class CachedSession:

    def __init__(self):
        cookie = (pathlib.Path(os.getenv("XDG_DATA_HOME")) / "cookies/everybody.codes").read_text().strip()
        self.session = requests.Session()
        self.session.cookies.set("everybody-codes", cookie)

    def get(self, url: str) -> str:
        cache = pathlib.Path(os.getenv("XDG_CACHE_HOME")) / "http" / "everybody.codes" / url.replace("/", "_")
        if cache.exists():
            return cache.read_text()
        resp = self.session.get(url)
        resp.raise_for_status()
        cache.write_text(resp.text)
        return resp.text

    def getjson(self, url: str) -> dict:
        return json.loads(self.get(url))

    def post(self, *args, **kwargs):
        return self.session.post(*args, **kwargs)


class Runner(running.Runner):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.session = CachedSession()

    def solutions_path(self) -> pathlib.Path:
        """Return the solution file."""
        return pathlib.Path(f"{self.year}/solutions.txt")

    def write_solutions(self, year: int, day: int) -> str:
        """Write the solutions to file."""
        year = year.removeprefix("event").removeprefix("story").removeprefix("0")
        data = self.session.getjson(f"https://api.everybody.codes/event/{year}/quest/{day}")
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

    def seed(self, year: int, day: int) -> int:
        return self.session.getjson("https://api.everybody.codes/user/me")["seed"]

    def decrypt(self, year: int, day: int, part: int, url: str) -> str | None:
        data = self.session.getjson(url)[f"{part}"]
        metadata = self.session.getjson(f"https://api.everybody.codes/event/{year}/quest/{day}")

        aes_key = metadata[f"key{part}"].encode()
        cipher = AES.new(aes_key, AES.MODE_CBC, iv=aes_key[:AES.block_size])
        plaintext = cipher.decrypt(bytes.fromhex(data))
        return unpad(plaintext, AES.block_size).decode()

    def download_input(self, year: int, day: int, part: int) -> str | None:
        """Download the input."""
        year = year.removeprefix("event").removeprefix("story").removeprefix("0")
        url = f"https://everybody.codes/assets/{year}/{day}/input/{self.seed(year, day)}.json"
        return self.decrypt(year, day, part, url)

    def get_tests(self, part: int, module: types.Module) -> list[tuple]:
        got = super().get_tests(part, module)
        if got:
            return got
        year = self.year.removeprefix("event").removeprefix("story").removeprefix("0")
        day = self.day

        url = f"https://everybody.codes/assets/{year}/{day}/description.json"
        plaintext = self.decrypt(year, day, part, url)
        examples = [i.strip() for i in etree.HTML(plaintext).xpath('//pre[@class="note"]/text()')]
        solutions = [i.strip() for i in etree.HTML(plaintext).xpath('//div[@class="example"]/div[@class="description"]/div[last()]/pre/b/text()')]
        return list(zip(itertools.cycle([part]), examples, solutions))

    def submit_solution(self, year: int, day: int, solutions: list[int | str]) -> str:
        """Submit the solution."""
        year = self.year.removeprefix("event").removeprefix("story").removeprefix("0")
        part = len(solutions)
        solution = str(solutions[-1])
        resp = self.session.post(f"https://api.everybody.codes/event/{year}/quest/{day}/part/{part}/answer", json={"answer": solution})
        resp.raise_for_status()
        print(rest.text)


@click.command()
@click.option("--day", "-d", type=int, required=True)
@click.option("--event", "-e", type=str, default="story01")
@click.option("--check", "-c", is_flag=True)
@click.option("--solve", "-s", is_flag=True)
@click.option("--submit", "-S", is_flag=True)
@click.option("--test", "-t", is_flag=True)
@click.option("--part", "-p", "parts", type=int, multiple=True, default=(1, 2, 3))
@click.option("--live", "-l", is_flag=True)
@click.option("--verbose", "-v", count=True)
def main(day: int, event: str, check: bool, solve: bool, submit: bool, test: bool, live: bool, parts: tuple[int], verbose: int) -> None:
    Runner(
        year=event, day=day, data=None, parts=parts, verbose=verbose
    ).run(check=check, solve=solve, test=test, live=live, submit=submit)


if __name__ == "__main__":
    main()

# vim:ts=4:sw=4:expandtab
