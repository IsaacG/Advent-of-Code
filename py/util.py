#!/bin/python

import pathlib
import sys
from typing import List, Optional


def load_data(sep: str = '\n', text: Optional[str] = None, func=lambda x: x) -> List[str]:
  if text is None:
    datafile = pathlib.Path(sys.argv[1])
    text = datafile.read_text()
  data = text.strip().split(sep)
  return [func(i) for i in data]

