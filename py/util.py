#!/bin/python

import pathlib
import sys
from typing import List, Optional


def load_data(sep: str = '\n', text: Optional[str] = None) -> List[str]:
  if text is None:
    datafile = pathlib.Path(sys.argv[1])
    text = datafile.read_text()
  return text.strip().split(sep)

