import sqlite3
import os
import re
import requests  # type: ignore
import subprocess

import click
from lxml import etree  # type: ignore
from typing import Optional
from urllib import parse


class Website:

    BASE = 'https://adventofcode.com/'

    def __init__(self, year, day, check_login: bool = True):
        self.year = str(year)
        self.day = str(int(day))
        conn = sqlite3.Connection(os.environ['SQL_DB'])
        query = 'SELECT value FROM cookies WHERE key = ?'
        cookie = next(conn.cursor().execute(query, ('aoc',)))[0]
        cookie = cookie.split("=")[-1]

        self.session = requests.Session()
        self.session.headers.update({'cookie': f'session={cookie}'})
        if check_login:
            self.assert_logged_in()
        self._text = None

    def set_cookie(self, cookie: str) -> None:
        cookie = cookie.split("=")[-1]
        conn = sqlite3.Connection(os.environ['SQL_DB'])
        query = 'UPDATE cookies SET value = ? WHERE key = ?'
        print(f"Set cookie to {cookie}")
        conn.cursor().execute(query, (cookie, 'aoc'))

    def text(self) -> str:
        if self._text is None:
            resp = self.session.get(f'https://adventofcode.com/{self.year}/day/{self.day}')
            resp.raise_for_status()
            self._text = resp.text
        assert self._text is not None
        return self._text

    @property
    def uri_day(self) -> str:
        return parse.urljoin(self.BASE, f'{self.year}/day/{self.day}')

    def title(self) -> str:
        et = etree.HTML(self.text())
        return et.xpath("//main/article/h2/text()")[0]

    def codeblocks(self) -> str:
        et = etree.HTML(self.text())
        sample = ['[']
        blocks = [c.strip() for c in et.xpath('//code/text()')]
        for num, block in enumerate(blocks):
            if "\n" in block:
                if "\\" in block:
                    sample.append('    r"""' + block + f'""",  # {num}')
                else:
                    sample.append('    """\\')
                    sample.append(block + f'""",  # {num}')
            else:
                sample.append(f"    {block!r},  # {num}")
        sample.append("]")
        return "\n".join(sample)

    def assert_logged_in(self):
        resp = self.session.get(self.BASE)
        resp.raise_for_status()

        db = os.environ['SQL_DB']
        query = "UPDATE cookies SET value = '$cookie' WHERE key = 'aoc';"

        if "[Log In]" in etree.HTML(resp.content).xpath('//a/text()'):
            print(f"sqlite3 {db}")
            print(query)
            print(self.session.headers["cookie"])
            raise RuntimeError("Did your cookie expire? It does not seem valid!")

    def get_input(self) -> str:
        resp = self.session.get(f"{self.uri_day}/input")
        resp.raise_for_status()
        return resp.text

    def part(self) -> Optional[int]:
        m = re.search(r'name="level" value="([^"]+)"', self.text())
        if m is None:
            return None
        return int(m.group(1))

    def _no_lxml_submit(self, answer) -> str:
        m = re.search(r'name="level" value="(.*)"', self.text())
        assert m, 'Cannot find the submit level'
        level = m.group(1)
        resp = self.session.post(f'{self.uri_day}/answer', data={'answer': answer, 'level': level})
        self._text = None
        resp.raise_for_status()
        cmd = ['pandoc', '--from=html', '--to=markdown']
        p = subprocess.run(cmd, text=True, capture_output=True, input=resp.text)
        return p.stdout

    def submit(self, answer) -> Optional[str]:
        et = etree.HTML(self.text())

        levels = et.xpath('//form/input[@name="level"]/@value')
        if not levels:
            print('No submission box found; is this already completed?')
            return None

        level = levels[0]
        resp = self.session.post(f'{self.uri_day}/answer', data={'answer': answer, 'level': level})
        self._text = None
        resp.raise_for_status()
        et = etree.HTML(resp.content)
        output = ''.join(et.xpath('//main/article//text()'))
        return output


@click.command()
@click.option("--set_cookie", type=str, required=True)
def main(set_cookie: str) -> None:
    Website(0, 0, False).set_cookie(set_cookie)


if __name__ == "__main__":
    main()
