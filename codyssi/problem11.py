"""Codyssi Day N."""

def solve(part: int, data: str) -> int:
    """Solve the parts."""
    freqs_r, swaps_r, track_r = [i.splitlines() for i in data.split("\n\n")]
    freqs = [int(i) for i in freqs_r]
    track = int(track_r[0]) - 1
    swaps = [[int(i) - 1 for i in swap.split("-")] for swap in swaps_r]

    if part == 1:
        for a, b in swaps:
            freqs[a], freqs[b] = freqs[b], freqs[a]
    if part == 2:
        for a, b in zip(swaps, swaps[1:] + swaps[:1]):
            x, y, z, _ = a + b
            freqs[x], freqs[y], freqs[z] = freqs[z], freqs[x], freqs[y]
    if part == 3:
        freq_count = len(freqs)
        for swap in swaps:
            a, b = sorted(swap)
            block_len = min(freq_count - b, b - a)
            freqs[a:a + block_len], freqs[b:b + block_len] = freqs[b:b + block_len], freqs[a:a + block_len]
    return freqs[track]


TEST_DATA = """\
159
527
827
596
296
413
45
796
853
778

4-8
5-8
10-1
6-5
2-1
6-5
8-7
3-6
7-8
2-10
6-4
8-10
1-9
3-6
7-10

10"""
TESTS = [
    (1, TEST_DATA, 45),
    (2, TEST_DATA, 796),
    (3, TEST_DATA, 827),
]
