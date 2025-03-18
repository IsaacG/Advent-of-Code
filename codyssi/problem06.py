"""Codyssi Day 6."""


def solve(part: int, data: str) -> int:
    """Solve the parts."""
    lines = data.splitlines()

    numbers = sorted(int(line) for line in lines[3:])
    function_numbers = [int(line.split()[-1]) for line in lines[:3]]

    def compute_cost(quality: int) -> int:
        quality **= function_numbers[2]
        quality *= function_numbers[1]
        quality += function_numbers[0]
        return quality

    if part == 1:
        return compute_cost(numbers[len(numbers) // 2])
    if part == 2:
        return compute_cost(sum(number for number in numbers if number % 2 == 0))

    limit = 15_000_000_000_000
    return max(number for number in numbers if compute_cost(number) <= limit)


TEST_DATA = """\
Function A: ADD 495
Function B: MULTIPLY 55
Function C: RAISE TO THE POWER OF 3
5219
8933
3271
7128
9596
9407
7005
1607
4084
4525
5496"""
TESTS = [
    (1, TEST_DATA, 9130674516975),
    (2, TEST_DATA, 1000986169836015),
    (3, TEST_DATA, 5496),
]
