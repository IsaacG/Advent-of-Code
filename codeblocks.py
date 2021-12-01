#!/bin/python

import datetime
import os
import pathlib
import requests
import sys
from lxml import etree


def main():
  day = sys.argv[1]
  cookie_file = pathlib.Path(os.getenv('HOME')) / '.xdg/data/cookie/aoc'
  cookie = cookie_file.read_text().split()[1]
  year = os.getenv("YEAR", datetime.datetime.now().year)
  resp = requests.get(f'https://adventofcode.com/{year}/day/{day}', headers={'cookie': cookie})
  et = etree.HTML(resp.content)
  print('SAMPLE = ["""\\')
  print('\n""","""\\\n'.join(c.strip() for c in et.xpath('//pre/code/text()')))
  print('"""]')


if __name__ == '__main__':
  main()
