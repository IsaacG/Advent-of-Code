#!/bin/python
"""Advent of Code: Day 10. Solve bracket matching."""
BRACKETS = dict[str, str](["()", "[]", "{}", "<>"])  # type: ignore


def bracket_match(line: str) -> tuple[str | None, list[str]]:
    """Bracket match a line, returning first invalid char and stack."""
    # Map closing bracket to its opening pair.
    open_chars = BRACKETS.keys()  # ([{<
    close_chars = BRACKETS.values()   # )]}>

    stack = []
    for char in line:
        # Open bracket. Add to the stack.
        if char in open_chars:
            stack.append(char)
        # Close bracket. Pop from the stack or error.
        if char in close_chars:
            # AoC input should not allow this to occur.
            # This condition isn't strictly needed.
            if not stack:
                raise ValueError("invalid input")
            if BRACKETS[stack[-1]] == char:
                stack.pop()
            else:
                return char, stack
    return None, stack


def solve(data: list[str], part: int) -> int:
    """Find invalid bracket pairs on a line."""
    bracket_values = {
        "(": 1, "[": 2, "{": 3, "<": 4,
        ")": 3, "]": 57, "}": 1197, ">": 25137,
    }

    def evaluate_stack(stack: list[str]):
        """Assign a score to remaining brackets."""
        value = 0
        for char in reversed(stack):
            value *= 5
            value += bracket_values[char]
        return value

    # Map each line to the bad closing bracket and remaining stack.
    char_and_stacks = [bracket_match(line) for line in data]
    if part == 1:
        # Sum up the value of the bad chars.
        return sum(bracket_values[char] for char, _ in char_and_stacks if char)
    # Score the required closing brackets for each line to make it valid.
    scores = [evaluate_stack(stack) for char, stack in char_and_stacks if not char]
    # Return the middle score.
    return sorted(scores)[len(scores)//2]


SAMPLE = """\
[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]
"""
TESTS = [(1, SAMPLE, 26397), (2, SAMPLE, 288957)]
