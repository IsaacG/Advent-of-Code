#!/bin/python3
"""Run AoC code in various flavors."""

import datetime
import inotify_simple
import os
import pathlib
import subprocess
from typing import List, Optional
import typer


class Runner:
  """Code runner."""

  def __init__(self, day: int, watch: bool, timeout: int):
    self.day = day
    self.timeout = timeout
    self.watch = watch
    self.base = pathlib.Path(__file__).parent
    if os.getenv('YEAR'):
      self.year = os.getenv('YEAR')
    else:
      self.year = '2020'

  def maybe_watch(self, func):
    """Run the function once or on every CLOSE_WRITE."""
    if not self.watch:
      return func(self.day)
    inotify = inotify_simple.INotify()
    inotify.add_watch(self.base / self.year, inotify_simple.flags.CLOSE_WRITE)
    while e := inotify.read():
      if not e[0].name.endswith('.py'):
        continue
      n = pathlib.Path(e[0].name).stem
      if not n.isnumeric():
        continue
      day = int(pathlib.Path(e[0].name).stem)
      print(datetime.datetime.now().strftime('%H:%M:%S'))
      func(day)
      print('Done.')

  def get_days(self, day):
    """Generate the filenames of the py code."""
    if day:
      day = f'{day:02d}'

    for f in sorted(self.base.glob(f'{self.year}/[0-9][0-9].py')):
      if day and f.stem != day:
        continue
      yield(f)

  def run_with_flags(self, flags: List[str]):
    """Run the .py file with a flag and data."""
    self.maybe_watch(lambda d: self._run_with_flags(flags, d))

  def _run_with_flags(self, flags: List[str], day: Optional[int]):
    for f in self.get_days(day):
      cmd = [f] + flags
      if self.timeout:
        if '--time' in flags and self.timeout == 30:
          self.timeout = 120
        cmd = ['timeout', str(self.timeout)] + cmd
      try:
        p = subprocess.run(cmd)
      except Exception as e:
        print(e)
        break
      if p.returncode == 124:
        print('TIMEOUT!')


def main(
  day: Optional[int],
  test: bool = False,
  solve: bool = False,
  check: bool = False,
  watch: bool = False,
  time: bool = False,
  timeout: int = 30,
):
  r = Runner(day, watch, timeout)
  flags = []
  if test:
    flags.append('--test')
  if solve:
    flags.append('--solve')
  if time:
    flags.append('--time')
  if check:
    flags.append('--check')
  assert flags
  r.run_with_flags(flags)


if __name__ == '__main__':
  typer.run(main)

# vim:ts=2:sw=2:expandtab
