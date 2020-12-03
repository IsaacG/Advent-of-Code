#!/bin/python

import pathlib
import sys
from typing import List


def load_data() -> List[str]:
  datafile = pathlib.Path(sys.argv[1])
  return datafile.read_text().split('\n')[:-1]

