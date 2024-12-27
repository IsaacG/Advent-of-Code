import re

def solve(part: int, data: str) -> int:
    chunks = data.split("\n\n")
    lines = chunks[1].splitlines()
    if part == 1:
        words = chunks[0].split(":", 1)[1].split(",")
        return sum(len(re.findall(word, chunks[1])) for word in words)
    words = chunks[0].split(":", 1)[1].split(",")
    chars = {complex(x, y): char for y, line in enumerate(lines) for x, char in enumerate(line)}
    width = len(lines[0])
    if part == 2:
        width *= 2  # disable wrapping by making the board wider than it actually is.
    directions = [complex(1), complex(-1), complex(0, 1), complex(0, -1)]
    included = set()
    for pos in chars:
        x = int(pos.real)
        y = complex(0, pos.imag)
        for direction in [1, -1]:
            for word in words:
                if all(chars.get(y + ((x + direction * offset) % width)) == char for offset, char in enumerate(word)):
                    included.update(y + ((x + direction * offset) % width) for offset in range(len(word)))
        if part == 2:
            # No vertical checks for part 2.
            continue
        for direction in [1j, -1j]:
            for word in words:
                if all(chars.get(pos + direction * offset) == char for offset, char in enumerate(word)):
                    included.update(pos + direction * offset for offset in range(len(word)))
    return len(included)


TEST_DATA = [
    """\
WORDS:THE,OWE,MES,ROD,HER

AWAKEN THE POWER ADORNED WITH THE FLAMES BRIGHT IRE""",
    """\
WORDS:THE,OWE,MES,ROD,HER,QAQ

AWAKEN THE POWE ADORNED WITH THE FLAMES BRIGHT IRE
THE FLAME SHIELDED THE HEART OF THE KINGS
POWE PO WER P OWE R
THERE IS THE END
QAQAQ
""",
    """\
WORDS:THE,OWE,MES,ROD,RODEO

HELWORLT
ENIGWDXL
TRODEOAL"""
]
TESTS = [
    (1, TEST_DATA[0], 4),
    (2, TEST_DATA[1], 42),
    (3, TEST_DATA[2], 10),
]
