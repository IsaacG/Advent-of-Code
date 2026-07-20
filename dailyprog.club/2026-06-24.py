"""Collatz steps

The Collatz conjecture says that repeatedly applying this rule to any positive integer eventually reaches 1: if n is even, divide by 2; if n is odd, multiply by 3 and add 1.
Given a positive integer n, return how many steps it takes to reach 1.
For n = 1, return 0, since you're already there.
"""

def collatzSteps(n):
    count = 0
    while n > 1:
        count += 1
        if n % 2 == 0:
            n //= 2
        else:
            n = n * 3 + 1
    return count

assert collatzSteps(1) == 0
assert collatzSteps(6) == 8
assert collatzSteps(12) == 9

