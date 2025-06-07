"""i18n puzzle day N."""

import bcrypt
import itertools
import logging
import unicodedata

log = logging.info

def solve(part: int, data: str) -> int:
    """Solve the parts."""
    blocks = data.split("\n\n")
    hashes = dict(line.split() for line in blocks[0].splitlines())

    count = 0
    for idx, line in enumerate(blocks[1].splitlines()):
        username, password = line.split()
        normalized = unicodedata.normalize("NFC", password)
        exploded = [{unicodedata.normalize(fmt, char) for fmt in ["NFC", "NFD"]} for char in normalized]
        candidates = ["".join(i).encode() for i in itertools.product(*exploded)]
        if idx and idx % 200:
            print(f"{idx}: {len(candidates)}")
        # assert password.encode() in candidates, f"{password=}, {candidates=}"
        # assert normalized.encode() in candidates
        hashed = hashes[username].encode()
        if any(bcrypt.checkpw(candidate, hashed) for candidate in candidates):
            count += 1
    return count


TEST_DATA = """\
etasche $2b$07$0EBrxS4iHy/aHAhqbX/ao.n7305WlMoEpHd42aGKsG21wlktUQtNu
mpataki $2b$07$bVWtf3J7xLm5KfxMLOFLiu8Mq64jVhBfsAwPf8/xx4oc5aGBIIHxO
ssatterfield $2b$07$MhVCvV3kZFr/Fbr/WCzuFOy./qPTyTVXrba/2XErj4EP3gdihyrum
mvanvliet $2b$07$gf8oQwMqunzdg3aRhktAAeU721ZWgGJ9ZkQToeVw.GbUlJ4rWNBnS
vbakos $2b$07$UYLaM1I0Hy/aHAhqbX/ao.c.VkkUaUYiKdBJW5PMuYyn5DJvn5C.W
ltowne $2b$07$4F7o9sxNeaPe..........l1ZfgXdJdYtpfyyUYXN/HQA1lhpuldO

etasche .pM?XÑ0i7ÈÌ
mpataki 2ö$p3ÄÌgÁüy
ltowne 3+sÍkÜLg._
ltowne 3+sÍkÜLg?_
mvanvliet *íÀŸä3hñ6À
ssatterfield 8É2U53N~Ë
mpataki 2ö$p3ÄÌgÁüy
mvanvliet *íÀŸä3hñ6À
etasche .pM?XÑ0i7ÈÌ
ssatterfield 8É2U53L~Ë
mpataki 2ö$p3ÄÌgÁüy
vbakos 1F2£èÓL
"""
TESTS = [
    (1, TEST_DATA, 4),
]
