"""Everyone Codes Day N."""

import logging
from lib import parsers

log = logging.info

def solve(part: int, data: str) -> int:
    """Solve the parts."""
    num_a = complex(*data[0])
    num = complex()
    if part == 1:
        for _ in range(3):
            num *= num
            num = complex(int(num.real) // 10, int(num.imag) // 10) + num_a

    if part == 2 or part == 3:

        def engrave(p):
            num = complex()
            for step in range(100):
                num *= num
                num = complex(int(num.real / 100000), int(num.imag / 100000))
                num += p
                if abs(num.real) > 1000000 or abs(num.imag) > 1000000:
                    return False
            return True
        
        total = 0
        step = 1 if part == 3 else 10
        for y in range(data[0][1], data[0][1] + 1001, step):
            for x in range(data[0][0], data[0][0] + 1001, step):
                total += engrave(complex(x, y))
        return total


    return f"[{int(num.real)},{int(num.imag)}]"


PARSER = parsers.parse_ints
TESTS = [
    (1, "A=[25,9]", "[357,862]"),
    (2, "A=[35300,-64910]", 4076),
    (3, "A=[35300,-64910]", 406954),
]
