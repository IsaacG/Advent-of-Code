#!/bin/python

import dataclasses
import os
import pathlib

from typing import Any, Callable, Dict, List, Optional


def load_data(src: str, config: Dict[str, Any]) -> List[str]:
  if os.path.exists(src):
    datafile = pathlib.Path(src)
    text = datafile.read_text()
  else:
    text = src
  data = text.strip().split(config['sep'])
  return [config['tranform'](i) for i in data]


@dataclasses.dataclass
class TestCase:
  inputs: str
  want: int
  part: int


def run_tests(config):
  """Run the tests."""
  for i, case in enumerate(config['tests']):
    debug(config, f"Running test {i + 1} (part{case.part})")
    data = load_data(case.inputs, config)
    args = []
    if 'test_args' in config:
      args = config['test_args']
    got = config['funcs'][case.part](data, *args)
    if case.want == got:
      debug(config, f"PASSED!")
    else:
      print(f'FAILED! want({case.want}) != got({got})')
  debug(config, '=====')


def debug(config, s):
  """Maybe print a message."""
  if config['debug']:
    print(s)
