#!/bin/python

import pathlib
import sys
from typing import List


def load_data(sep='\n') -> List[str]:
  datafile = pathlib.Path(sys.argv[1])
  data = datafile.read_text().split(sep)
  if data[-1] == "":
    del data[-1]
  return data

