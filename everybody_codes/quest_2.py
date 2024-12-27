import itertools
import re
import pathlib

DAY = 2
TEST_TWO = """\
WORDS:THE,OWE,MES,ROD,HER,QAQ

AWAKEN THE POWE ADORNED WITH THE FLAMES BRIGHT IRE
THE FLAME SHIELDED THE HEART OF THE KINGS
POWE PO WER P OWE R
THERE IS THE END
QAQAQ
"""
TEST_THREE = """\
WORDS:THE,OWE,MES,ROD,RODEO

HELWORLT
ENIGWDXL
TRODEOAL"""
TESTS = [
    (1, "WORDS:THE,OWE,MES,ROD,HER\n\nAWAKEN THE POWER ADORNED WITH THE FLAMES BRIGHT IRE", 4),
    (2, TEST_TWO, 42),
    (3, TEST_THREE, 10),
]

def solve(part: int, data: str) -> int:
    chunks = data.split("\n\n")
    lines = chunks[1].splitlines()
    if part == 1:
        words = chunks[0].split(":", 1)[1].split(",")
        return sum(len(re.findall(word, chunks[1])) for word in words)
    if part == 2:
        words = [(i, len(i)) for i in chunks[0].split(":", 1)[1].split(",")]
        total = 0
        for line in lines:
            indexes = set()
            line_len = len(line)
            rev_line = line[::-1]
            for idx in range(line_len):
                for word, size in words:
                    if line[idx:idx + size] == word:
                        indexes.update(range(idx, idx + size))
                    if rev_line[idx:idx + size] == word:
                        indexes.update(line_len - 1 - i for i in range(idx, idx + size))
            total += len(indexes)
        return total
    if part == 3:
        words = chunks[0].split(":", 1)[1].split(",")
        chars = {complex(x, y): char for y, line in enumerate(lines) for x, char in enumerate(line)}
        width = len(lines[0])
        directions = [complex(1), complex(-1), complex(0, 1), complex(0, -1)]
        included = set()
        for pos in chars:
            x = int(pos.real)
            y = complex(0, pos.imag)
            for direction in [1, -1]:
                for word in words:
                    if all(chars.get(y + ((x + direction * offset) % width)) == char for offset, char in enumerate(word)):
                        included.update(y + ((x + direction * offset) % width) for offset in range(len(word)))
            for direction in [1j, -1j]:
                for word in words:
                    if all(chars.get(pos + direction * offset) == char for offset, char in enumerate(word)):
                        included.update(pos + direction * offset for offset in range(len(word)))
        return len(included)



solutions_path = pathlib.Path(f"solutions/2024.{DAY:02}.txt")
if solutions_path.exists():
    want_raw = next((line.split() for line in solutions_path.read_text().splitlines() if line.startswith(f"{DAY:02} ")), None)
    want = [int(i) for i in want_raw[1:]]

got = []
for part in range(1, 4):
    data_path = pathlib.Path(f"inputs/{DAY:02}.{part}.txt")
    if not data_path.exists():
        continue
    data = data_path.read_text().rstrip()
    for test_part, test_data, test_want in TESTS:
        if test_part == part:
            assert solve(test_part, test_data) == test_want
    got.append(solve(part, data))

if solutions_path.exists():
    assert want == got, f"{want=}, {got=}"
print(got)
