"""FlipFlop Codes: N."""
from lib import parsers


def solve(part: int, data: list[list[int]]) -> int:
    """Solve the parts."""
    size = 1000
    frame_size = 500
    frame_start = (size - frame_size) // 2
    frame_end = frame_start + frame_size - 1

    def counts_at(seconds: int) -> int:
        return sum(
            (
                frame_start <= (dx * seconds) % size <= frame_end
                and frame_start <= (dy * seconds) % size <= frame_end
            )
            for dx, dy in data
        )

    interval = [0, 100, 3600, 31556926][part]
    times = 1 if part == 1 else 1000
    return sum(counts_at(interval * i) for i in range(1, times + 1))


PARSER = parsers.parse_ints
# TEST_DATA = []
# TESTS = [
    # (1, TEST_DATA[0], None),
    # (2, TEST_DATA[1], None),
    # (3, TEST_DATA[2], None),
# ]
