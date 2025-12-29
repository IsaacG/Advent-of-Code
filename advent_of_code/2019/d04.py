#!/usr/bin/env python
"""2019 Day 4: Secure Container. Count valid passwords (incrementing, double num, in range)."""
import collections
LEN = 6


def has_a_repeat(num: int) -> bool:
    """Must contain a doubled digit."""
    digits = [int(i) for i in str(num)]
    return any(digits[i + 1] == digits[i] for i in range(LEN - 1))


def has_a_double(num: int) -> bool:
    """Must contain a doubled - not tripled or more - digit."""
    digits = collections.Counter(str(num))
    return 2 in digits.values()


def solve(data: list[int], part: int) -> int:
    """Count the number of "valid" passwords in a range.

    Build the number one digit at a time, bounds checking each time.
    If the bounds are 200 <= n <= 350,
    then we can check 2 <= 3 <= 3 at len=1 and 20 <= 36 <= 35 at len=2.
    """
    valid = has_a_repeat if part == 1 else has_a_double
    part_bounds = [[0] + [int(str(num)[:i]) for i in range(1, LEN + 1)] for num in data]
    c = 20

    def sum_valid(num: int, length: int) -> int:
        """Recursively count sum valid passwords for a given prefix."""
        # Check early at each length for bounds.
        nonlocal c
        if not part_bounds[0][length] <= num <= part_bounds[1][length]:
            if c:
                c -= 1
            return 0
        if length == LEN:
            return 1 if valid(num) else 0

        # Next digit to add must be >= prior digit.
        prior_digit = num % 10
        num *= 10
        length += 1
        return sum(sum_valid(num + i, length) for i in range(prior_digit, 10))

    # The first digit cannot be 0 or it won't be a "6 digit number".
    # Or at least, it won't be in the range given by my input.
    return sum(sum_valid(num, 1) for num in range(1, 10))


TESTS = [(1, '100000-111111', 1), (1, '100000-111115', 5), (2, '100000-111123', 1)]
