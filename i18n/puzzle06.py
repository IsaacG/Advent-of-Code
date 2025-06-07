"""i18n puzzle day N."""

import logging

log = logging.info

def solve(part: int, data: str) -> int:
    """Solve the parts."""
    blocks = data.split("\n\n")
    words = []
    for idx, word in enumerate(blocks[0].splitlines(), 1):
        for m in [3, 5]:
            if idx % m == 0:
                word = word.encode("8859").decode("utf-8")
        words.append(word)

    total = 0
    for line in blocks[1].splitlines():
        line = line.strip()
        found = False
        for idx, word in enumerate(words, 1):
            if len(line) != len(word):
                continue
            for a, b in zip(line, word):
                if a != "." and a == b:
                    found = True
            if found:
                total += idx
                break
    return total


TEST_DATA = """\
geléet
träffs
religiÃ«n
tancées
kÃ¼rst
roekoeÃ«n
skälen
böige
fÃ¤gnar
dardÃ©es
amènent
orquestrÃ¡
imputarão
molières
pugilarÃÂ£o
azeitámos
dagcrème
zÃ¶ger
ondulât
blÃ¶kt

   ...d...
    ..e.....
     .l...
  ....f.
......t..
"""
TESTS = [
    (1, TEST_DATA, 50),
]
