"""i18n puzzle day N."""

import logging

log = logging.info

def solve(part: int, data: str) -> int:
    """Solve the parts."""
    lines = data.splitlines()
    width = len(lines[0])
    x = 0
    count = 0
    for line in lines:
        count += line[x % width] == "💩"
        x += 2
    return count


TEST_DATA = """\
 ⚘   ⚘ 
  ⸫   ⸫
🌲   💩  
     ⸫⸫
 🐇    💩
⸫    ⸫ 
⚘🌲 ⸫  🌲
⸫    🐕 
  ⚘  ⸫ 
⚘⸫⸫   ⸫
  ⚘⸫   
 💩  ⸫  
     ⸫⸫
"""
TESTS = [
    (1, TEST_DATA, 2),
]
