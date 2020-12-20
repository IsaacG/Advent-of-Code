#!/bin/python3
"""Run AoC code in various flavors.

TODO: Add a timeout flag.
"""

import click
import datetime
import inotify_simple
import pathlib
import subprocess
from typing import List

@click.group()
def cli():
  pass


@cli.command()
@click.argument('days', type=int, nargs=-1)
@click.option('-w', '--watch', type=bool, default=False)
def test(days: List[int], watch: bool):
  """Run the unit tests/sample inputs."""
  Runner(days, watch).run_with_flag('-v')
  print('All unit tests good!')


@cli.command()
@click.argument('days', type=int, nargs=-1)
@click.option('-w', '--watch', type=bool, default=False)
def solve(days: List[int], watch: bool):
  """Spit out the solutions."""
  Runner(days, watch).run_with_flag('-r')


@cli.command()
@click.argument('days', type=int, nargs=-1)
@click.option('-w', '--watch', type=bool, default=False)
def time(days: List[int], watch: bool):
  """Generate runtimes."""
  Runner(days, watch).run_with_flag('-t')


@cli.command()
@click.option('-w', '--watch', type=bool, default=False)
@click.argument('days', type=int, nargs=-1)
def check(days: List[int], watch: bool):
  """Check the solution matches data/solutions."""
  Runner(days, watch).check()


class Runner:
  """Code runner."""

  def __init__(self, days: List[int], watch: bool):
    self.days = days
    self.watch = watch
    self.base = pathlib.Path(__file__).parent

  def maybe_watch(self, func):
    """Run the function once or on every CLOSE_WRITE."""
    if not self.watch:
      return func()
    inotify = inotify_simple.INotify()
    inotify.add_watch(self.base / 'py', inotify_simple.flags.CLOSE_WRITE)
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

  def get_days(self, day=None):
    """Generate the filenames of the py code and matching data.txt"""
    if day:
      days = [day]
    else:
      days = self.days
    days = [f"{i:02d}" for i in days]

    for f in sorted(self.base.glob('py/[0-9][0-9].py')):
      if days and f.stem not in days:
        continue
      data = (self.base / 'data' / f.stem).with_suffix('.txt')
      yield((f, data))

  def check(self):
    """Check the solutions match data/solutions."""
    self.maybe_watch(self._check)

  def _check(self, day=None):
    if day:
      days = [day]
    else:
      days = self.days

    for line in (self.base / 'data/solutions').read_text().strip().split('\n'):
      day, want1, want2 = line.split()
      day = int(day)
      if days and day not in days:
        continue
      f = (self.base / 'py' / f'{day:02d}').with_suffix('.py')
      d = (self.base / 'data' / f'{day:02d}').with_suffix('.txt')
      cmd = [f, d]
      p = subprocess.run(cmd, text=True, capture_output=True)
      output = p.stdout.strip()
      if len(output.split()) != 2:
        print(f'Day {day:02d}: FAILED')
        print('> ', output)
        continue
      got1, got2 = output.split()
      if want1 == got1 and want2 == got2:
        print(f'Day {day:02d}: PASS')
      else:
        print(f'Day {day:02d}: FAILED')
        print(f'1: want[{want1}] got[{got1}]. 2: want[{want2}] got[{got2}].')

  def run_with_flag(self, flag: str):
    """Run the .py file with a flag and data."""
    self.maybe_watch(lambda x=None: self._run_with_flag(flag, x))

  def _run_with_flag(self, flag: str, day=None):
    for (f, d) in self.get_days(day):
      # cmd = ['timeout', '2', f, flag, d]
      cmd = [f, flag, d]
      try:
        p = subprocess.run(cmd)
      except Exception as e:
        print(e)
        break
      if p.returncode == 124:
        print('TIMEOUT!')


if __name__ == '__main__':
  cli()

# vim:ts=2:sw=2:expandtab
