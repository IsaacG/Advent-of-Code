#!/bin/python

import requests
import pathlib
import os
import sys
from lxml import etree


def main():
  day = sys.argv[1]
  cookie_file = pathlib.Path(os.getenv('HOME')) / '.xdg/data/aoc.2020.cookie'
  cookie = cookie_file.read_text().split()[1]
  resp = requests.get(f'https://adventofcode.com/2020/day/{day}', headers={'cookie': cookie})
  et = etree.HTML(resp.content)
  print('SAMPLE = ["""\\')
  print('\n""","""\\\n'.join(c.strip() for c in et.xpath('//pre/code/text()')))
  print('"""]')


if __name__ == '__main__':
  main()
